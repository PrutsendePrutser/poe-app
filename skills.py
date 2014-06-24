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
        
        self.retrieve_skill_info()
        self.retrieve_support_skill_info()
        
    def retrieve_skill_info(self):
        skill_links = self.get_active_skill_gems_from_wiki()
        with open('files/active_skill_levels.csv', 'a') as activeskillfile:
            for link in skill_links:
                self.readskillpage(link, activeskillfile)
                
    def retrieve_support_skill_info(self):
        skill_links = self.get_support_skill_gems_from_wiki()
        with open('files/support_skill_levels.csv', 'a') as supportskillfile:
            for link in skill_links:
                self.readskillpage(link, supportskillfile)
        
    def readskillpage(self, skillname, activeskillfile):
        # Create HTML parser object
        parser = MyHTMLParser()
        # Unescape dashes
        parser.unescape('&ndash; &#8211;')
        
        # Create a connection to the wiki
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        
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
            print dict(zip(parser.infodescription, parser.infodescvalue))
           # print dict(zip(parser.infodescription, parser.infodescvalue))
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
        if skill == "/Portal":
            return
        try:
            activeskillfile.write(skill.replace('/', '').replace('_', ' ') + '\t' + self.skilldata[skill][0] + '\n')
        except IndexError:
            pass
        # Loop over the leveldata
        for level in self.skilldata[skill][1:]:
            # Ensure we only go to lvl 20
            try:
                if int(level.split('\t')[0]) > 20:
                    break
            except ValueError:
                try: 
                    int(level.split('\t')[0].split()[0])
                except:
                    print 'Error', level
                    continue
                    
            # Add the level data for the current skillgems to the file
            activeskillfile.write('\t' + str(level) + '\n')

    def get_active_skill_gems_from_wiki(self):
    
        # Make an instance of the skillpage parser
        skillpage_parser = SkillpageParser()
        # Setup a http connection object
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        
        # Make a get request to the skillpage
        conn.request("GET", '/Skills')
        
        # Get the response
        response = conn.getresponse()
        
        # Get the data
        data = response.read()
        
        # If we get an OK response
        if response.status == 200:
            # Feed the data to the parser
            skillpage_parser.feed(data)
        return skillpage_parser.link_list
    
    def get_support_skill_gems_from_wiki(self):
    
        # Make an instance of the skillpage parser
        skillpage_parser = SupportSkillpageParser()
        # Setup a http connection object
        conn = httplib.HTTPConnection("pathofexile.gamepedia.com")
        
        # Make a get request to the skillpage
        conn.request("GET", '/Skills')
        
        # Get the response
        response = conn.getresponse()
        
        # Get the data
        data = response.read()
        
        # If we get an OK response
        if response.status == 200:
            # Feed the data to the parser
            skillpage_parser.feed(data)
        return skillpage_parser.link_list


class SkillpageParser(HTMLParser.HTMLParser):
    
    handle_table_tag = False
    handle_td = False
    handle_links = False
    link_list = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'span' and ('id', "Active_Skills") in attrs:
            self.handle_table_tag = True
        elif tag == 'table' and ('class', 'wikitable sortable') and self.handle_table_tag:
            self.handle_td = True
        elif tag == 'td' and self.handle_td:
            self.handle_links = True
        elif tag == 'a' and self.handle_links:
            for at in attrs:
                if at[0] == 'href' and at[1]:
                    self.link_list.append(at[1])
    
    def handle_end_tag(self, tag):
        # If a closing table tag is encountered, reset all the values to False
        if tag == 'table' and self.handle_table_tag:
            self.handle_table_tag = False
            self.handle_td = False
            self.handle_links = False\
    
class SupportSkillpageParser(HTMLParser.HTMLParser):
    
    handle_table_tag = False
    handle_td = False
    handle_links = False
    link_list = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'span' and ('id', "Support_Gems_2") in attrs:
            self.handle_table_tag = True
        elif tag == 'table' and ('class', 'wikitable sortable') and self.handle_table_tag:
            self.handle_td = True
        elif tag == 'td' and self.handle_td and self.handle_table_tag:
            self.handle_links = True
        elif tag == 'a' and self.handle_links and self.handle_td and self.handle_table_tag:
            for at in attrs:
                if at[0] == 'href' and at[1]:
                    self.link_list.append(at[1])
    
    def handle_end_tag(self, tag):
        # If a closing table tag is encountered, reset all the values to False
        if tag == 'table' and self.handle_table_tag:
            self.handle_table_tag = False
            self.handle_td = False
            self.handle_links = False

class MyHTMLParser(HTMLParser.HTMLParser):
    # Boolean to determine if we are in the table that contains the skillgem level data
    inskilltable = False
    write_tr = False
    
    # Var to store the data
    d = ""
    
    trdata = {}
    trstring = ""
    infodescription = []
    infodescvalue = []
    val = ""
    
    # previous tag, used to handle <br /> tags within a <td></td> tag pair
    prev_tag = ""
    
    append_data = False
    
    def handle_starttag(self, tag, attrs):
        # If we hit a table that contains gemlevel data
        if tag == "table" and ("class", "wikitable GemLevelTable") in attrs:
            # Set the inskilltable boolean to true
            self.inskilltable = True
        if tag == "table" and ("class", "GemInfoboxInfo") in attrs:
            self.infodescription = []
            self.infodescvalue = []
            self.write_tr = True
        # If we meet a tr tag in the skilltable, add a newline to the data
        if tag == "tr" and self.inskilltable:
            if not self.write_tr:
                self.d += '\n'
        if tag == "tr" and self.write_tr:
            self.trstring = ""
            self.val = ""
            
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
        if tag == "table" and self.write_tr:
            self.write_tr = False
        if tag == "tr" and self.d:
            pass
        if tag == "tr" and self.write_tr:
            self.infodescvalue.append(self.val)

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
            val = data.replace('\n','').replace('\r','').replace('\t','').replace('<br />','').strip()
            # If there is still a val left after removing whitespace, add the value to the data and add a trailing tab
            if val:
                self.d += val.strip() + '\t'
        if self.write_tr:
            data = data.replace('\n','').replace('\r','').replace('\t','').replace('<br />','').strip()
            if data:
                if self.trstring:
                    #print "Value: ", data
                    self.val += data
                    self.trstring += data
                else:
                    #print "Description: ", data
                    self.infodescription.append(data)
                    self.trstring += data
        

gems = Skillgems()
