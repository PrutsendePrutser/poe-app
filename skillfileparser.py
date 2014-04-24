'''
Created on Apr 10, 2014

@author: Prutser
'''

class SkillFileParser(object):
    '''
    classdocs
    '''


    def __init__(self, fpath):
        '''
        Constructor
        '''
        # Set filepath
        self.fpath = fpath
        # Set dictionary to store all the skills in the skillfile
        self.skills = {}
        # Parse the file
        self.parse_file()
        
    def parse_file(self):
        # Open the file with filepath in read modus
        with open(self.fpath, 'r') as skillfile:
            
            # Retrieve the file contents
            content = skillfile.readlines()
            
            # Split the different skills out, 1 line for header, 20 lines for each level
            skill_content = [content[i:i+21] for i in range(0, len(content), 21)]
        # Loop over the skills and parse each skill entry
        for skill in skill_content:
            self.parse_skill(skill)

    def parse_skill(self, skill):
        # Get the header line
        header = skill[0].split('\t')
        # If the skillname is not in the skills dictionary
        if header[0] not in self.skills.keys():
            # Add a nested dictionary for the current skill
            self.skills[header[0]] = {}
        # Loop over the different header entries, add them to the nested dictionary and add an empty string as value
        for head in header[1:]:
            self.skills[header[0]][head] = ""
        # Loop over each level of the skill
        for entry in skill[1:]:
            # Split each line on tabs
            entry = entry.split('\t')
            print entry
            # Loop over each column of the header
            for idx, head in enumerate(header[1:]):
                print idx, head
                # Add the data of the current column to the column entry for the current skill
                # 1 is added to the index to make up for the first column of each level which is empty
                self.skills[header[0]][head] = entry[idx+1]
                    
parser = SkillFileParser('active_skill_levels.csv')
print parser.skills