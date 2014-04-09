"""
This class contains all the active skill gems and support skill gems in Path of Exile
with their stats and information
"""

import httplib
import HTMLParser

class Skillgems(object):
    
    # Initialize class vars
    def __init__(self):
        self.active_skills = {}
        self.support_skills = {}
        
    def readskillpage(self, skillname):
        parser = MyHTMLParser()
        skillname = "/{}".format(skillname.replace(" ", "_"))
        print skillname
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        conn.request("GET", skillname)
        response = conn.getresponse()
        print response.status, response.reason
        if response.status == 200:
            print "200"
            parser.feed(response.read())
            
class MyHTMLParser(HTMLParser.HTMLParser):
    inskilltable = False
    d = ""
    append_data = False
    def handle_starttag(self, tag, attrs):
        if tag == "table" and ("class", "wikitable GemLevelTable") in attrs:
            self.inskilltable = True
        if tag == "tr":
            self.d += '\n'
            
    def handle_endtag(self, tag):
        if tag == "table" and self.inskilltable:
            self.inskilltable = False
            print self.d
        if tag == "tr" and self.d:
            pass
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_data(self, data):
        if self.inskilltable:
            val = data.replace('\n','').replace('\r','').replace('\t','').replace('<br />','').rstrip()
            self.d += val + '\t'

gems = Skillgems()
skillist = []
with open('skills.txt', 'r') as skillfile:
    skilllist = skillfile.readlines()
skilllist = [skill.replace('\r', '').strip() for skill in skilllist]
print skilllist
for skill in skilllist:
    gems.readskillpage(skill)