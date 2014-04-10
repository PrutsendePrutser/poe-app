"""
This class contains all the active skill gems and support skill gems in Path of Exile
with their stats and information
"""

import httplib
import HTMLParser
import time

class Skillgems(object):
    
    # Initialize class vars
    def __init__(self):
        self.active_skills = {}
        self.support_skills = {}
        self.skilldata = {}
        self.counter = 0
        
    def readskillpage(self, skillname, activeskillfile):
        parser = MyHTMLParser()
        skillname = "/{}".format(skillname.replace(" ", "_"))
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        print "http://pathofexile.gamepedia.com%s" % skillname
        conn.request("GET", skillname)
        response = conn.getresponse()
        if response.status == 200:
            parser.feed(response.read())
            print parser.d
            skilln = skillname.replace('/', '').replace('_', ' ')
            print skilln, self.skilldata.keys()
            self.skilldata[skilln] = [l for l in parser.d.split('\n') if l.strip()]
        else:
            print response.status, response.reason
        print self.counter
        self.counter += 1
        conn.close()
        time.sleep(30)
        self.writeskillfile(skilln, activeskillfile)
    
    def writeskillfile(self, skill, activeskillfile):
        activeskillfile.write(skill.replace('/', '').replace('_', ' ') + '\t' + self.skilldata[skill][0] + '\n')
        for level in self.skilldata[skill][1:]:
            # Ensure we only go to lvl 20
            if int(level.split('\t')[0]) > 20:
                break
            activeskillfile.write('\t' + str(level) + '\n')
        
class MyHTMLParser(HTMLParser.HTMLParser):
    inskilltable = False
    d = ""
    prev_tag = ""
    append_data = False
    def handle_starttag(self, tag, attrs):
        if tag == "table" and ("class", "wikitable GemLevelTable") in attrs:
            self.inskilltable = True
        if tag == "tr":
            self.d += '\n'
        if tag == 'td':
            self.prev_tag = "td"
            
    def handle_endtag(self, tag):
        if tag == "table" and self.inskilltable:
            self.inskilltable = False
            self.d +='\n'
        if tag == "tr" and self.d:
            pass
    def handle_startendtag(self, tag, attrs):
        if self.inskilltable:
            if tag == 'br' and self.prev_tag == "td":
                self.d = self.d.rstrip('\t') + " "
            if tag == 'img':
                if 'Level_up_icon_small' in attrs[1][1]:
                    self.d += 'Required level\t'
                elif "StrengthIcon" in attrs[1][1]:
                    self.d += 'Strength\t'
                elif "DexterityIcon" in attrs[1][1]:
                    self.d += "Dexterity\t"
                elif "IntelligenceIcon" in attrs[1][1]:
                    self.d += "Intelligence\t"
    def handle_data(self, data):
        if self.inskilltable:
            val = data.replace('\n','').replace('\r','').replace('\t','').replace('<br />','').strip()
            if val:
                self.d += val.strip() + '\t'

gems = Skillgems()
skillist = []
skillfiles = ['skills.txt', 'skills2.txt', 'skills3.txt', 'skills4.txt', 'skills5.txt', 'skills6.txt']
for f in skillfiles:
    with open(f, 'r') as skillfile:
        skilllist = skillfile.readlines()
    skilllist = [skill.replace('\r', '').strip() for skill in skilllist]
    with open('active_skill_levels.csv', 'a') as activeskillfile:
        for skill in skilllist:
            gems.readskillpage(skill, activeskillfile)