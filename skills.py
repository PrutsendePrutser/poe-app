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
        # Dictionary to store the active skills along with the data
        self.active_skills = {}
        
        # Dictionary to store support skills along with the data
        self.support_skills = {}
        
        # Dictionary that is currently used for testing with the skilldata
        self.skilldata = {"notfound":[]}
        
        # Counter
        self.counter = 0
        
    def readskillpage(self, skillname, activeskillfile):
        # Create HTML parser object
        parser = MyHTMLParser()
        # Unescape dashes
        parser.unescape('&ndash; &#8211;')
        
        # Format skillname for retrieval from website, replace spaces
        skillname = "/{}".format(skillname.replace(" ", "_"))
        
        # Create a connection to the wiki
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        
        # Print the URL
        print "http://pathofexile.gamepedia.com%s" % skillname
        
        # Make a get request to the skillpage
        conn.request("GET", skillname)
        
        # Get the response
        response = conn.getresponse()
        
        # Get the data
        data = response.read()
        
        # If we get an OK response
        if response.status == 200:
            # Feed the data to the parser
            parser.feed(data)
            
            # Remove forward slash from skillname and replace underscores
            skilln = skillname.replace('/', '').replace('_', ' ')
            
            # Add the skilldata to the dictionary
            self.skilldata[skilln] = [l for l in parser.d.split('\n') if l.strip()]
        # In case we get some sort of error
        else:
            # Add the skillname to the notfound entry, so we know that this one needs to be retrieved manually
            self.skilldata['notfound'].append(skillname)
            return
        # Increment counter
        self.counter += 1
        
        # Close the connection
        conn.close()
        # Wait 1 second to avoid flooding the wiki with requests in a short time
        # The wiki does not like that!
        time.sleep(1)
        
        # Write the data of the current skill to the active skillfile
        self.writeskillfile(skilln, activeskillfile)
    
    def writeskillfile(self, skill, activeskillfile):
        # Write the skillname + headers to the skillfile
        activeskillfile.write(skill.replace('/', '').replace('_', ' ') + '\t' + self.skilldata[skill][0] + '\n')
        # Loop over the leveldata
        for level in self.skilldata[skill][1:]:
            # Ensure we only go to lvl 20
            if int(level.split('\t')[0]) > 20:
                break
            # Add the level data for the current skillgems to the file
            activeskillfile.write('\t' + str(level) + '\n')
        
class MyHTMLParser(HTMLParser.HTMLParser):
    # Boolean to determine if we are in the table that contains the skillgem level data
    inskilltable = False
    
    # Var to store the data
    d = ""
    
    # previous tag, used to handle <br /> tags within a <td></td> tag pair
    prev_tag = ""
    
    append_data = False
    
    def handle_starttag(self, tag, attrs):
        # If we hit a table that contains gemlevel data
        if tag == "table" and ("class", "wikitable GemLevelTable") in attrs:
            # Set the inskilltable boolean to true
            self.inskilltable = True
        # If we meet a tr tag in the skilltable, add a newline to the data
        if tag == "tr" and self.inskilltable:
            self.d += '\n'
        # If we hit a td tag
        if tag == 'td':
            # Set the previous tag var to td
            self.prev_tag = "td"


    def handle_endtag(self, tag):
        # If we hit the table endtag of the skilltable
        if tag == "table" and self.inskilltable:
            # Set the inskilltable boolean to False
            self.inskilltable = False
            # Add a newline character to the data
            self.d +='\n'
        if tag == "tr" and self.d:
            pass


    def handle_startendtag(self, tag, attrs):
        # If we are in a skilltable
        if self.inskilltable:
            
            # If we hit a break tag in a td tag, remove the last trailing tab and add a space instead
            if tag == 'br' and self.prev_tag == "td":
                self.d = self.d.rstrip('\t') + " "
            # If we hit an img tag
            if tag == 'img':
                # Add placeholder for the required level icon
                if 'Level_up_icon_small' in attrs[1][1]:
                    self.d += 'Required level\t'
                # Add placeholder for the required strength
                elif "StrengthIcon" in attrs[1][1]:
                    self.d += 'Strength\t'
                # Add placeholder for the required dexterity
                elif "DexterityIcon" in attrs[1][1]:
                    self.d += "Dexterity\t"
                # Add placeholder for the required intelligence
                elif "IntelligenceIcon" in attrs[1][1]:
                    self.d += "Intelligence\t"


    def handle_data(self, data):
        # Only handle data if we are in the skilltable
        if self.inskilltable:
            # Replace whitespace with empty string, replace break tags, and replace the dash character
            val = data.replace('\n','').replace('\r','').replace('\t','').replace('<br />','').replace('&#8211;', '-').strip()
            # If there is still a val left after removing whitespace, add the value to the data and add a trailing tab
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
#gems.readskillpage("Arc", "f")
print gems.skilldata['notfound']