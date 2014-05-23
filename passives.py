import base64
import re

class PassiveCalculator(object):
    
    def __init__(self, build_url):
        """Initialize class instance"""
        # Set the build url that the user entered
        self.build_url = build_url.split("passive-skill-tree/")[1]
        self.selected_node_ids = self.convert_to_node_ids(self.load_from_url())
        self.node_data = self.load_nodes_data()
    
    def set_build_url(self, url):
        self.build_url = url.split("passive-skill-tree/")[1]
        self.selected_node_ids = self.convert_to_node_ids(self.load_from_url())
        
    def load_from_url(self):
        # Make a local build URL so we don't change the original one
        local_build_url = self.build_url.replace("-", "+").replace("_", "/")
        
        # Base 64 decode the build URL and return it
        return base64.b64decode(local_build_url)
    
    def convert_to_node_ids(self, build):
        # Make a list to store the node IDs
        node_ids = []
        
        # The actual build nodes start at the seventh index
        # Loop over the build from the first node, in steps of 2
        for i in range(6, len(build), 2):
            # In the base64 decoded string, each node ID is created out of 2 decoded characters
            # Where i+1 is the first one of the two and i is the second of the two
            # Combine the two characters, and decode them using utf-16 decoding
            # Cast to an ord so we have the 16 bit int value
            # Add to the node_ids list
                
            try:
                # Decode the next two characters from the string
                c = (build[i+1] + build[i+0]).decode("utf-16")
                if c == "":
                    c = "  "
                # Add the ord code to the node_ids list
                node_ids.append(ord(c))
            except UnicodeDecodeError:
                # If we get a UnicodeDecodeError we got an invalid char
                # Print the erroneous characters
                print "Error: ", (build[i+1] + build[i+0])
            # If we get a TypeError it's not a utf-16 character
            except TypeError:
                print "C: ", repr(c)
            
            
        # When we have parsed the full build url, return the node_ids
        return node_ids
    
    def load_nodes_data(self):
        # Open the skillnodes file
        with open("files/skillnodes.csv", "r") as sfile:
            
            # Read the contents
            lines = sfile.readlines()
            
            # Dictionary to store the different nodes
            node_dict = {}
            
            # Loop over the file contents
            for line in lines:
                # Split each line on tabs
                split = line.split('\t')
                # Get nodeid and node name
                nodeid = split[0]
                name = split[1]
                # Get the description of the bonuses
                desc = [d.replace(';', '').strip() for d in split[2].split(';') if d.strip()]
                
                # Add an entry to the node_dict
                node_dict[nodeid] = {'name': name,
                                     'desc': desc}
            # Return the nodes dictionary
            return node_dict

    def is_numeric(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    def get_bonus_for_selected_nodes(self):
        # Loop over the selected node ids
        # Dictionary to store all the node bonuses with the total value
        self.node_bonus_dict = {}
        
        # Regexp to find non-numeric characters
        non_decimal = re.compile(r'[^\d.]+')
        for idx, n in enumerate(sorted(self.selected_node_ids)):
            # Retrieve the name
            node_name = self.node_data[str(n)]['name']
            # Retrieve the descriptions
            node_desc = self.node_data[str(n)]['desc']
            # Print the index and data
            for desc in node_desc:
                splitted_description = desc.split(' ')
                stringvalue = non_decimal.sub('', splitted_description[0])
                if self.is_numeric(stringvalue):
                    value = float(stringvalue)
                    description = ' '.join(splitted_description[1:])
                else:
                    description = ' '.join(splitted_description)
                    value = "Keystone"

                if description not in self.node_bonus_dict.keys():
                    self.node_bonus_dict[description] = value
                else:
                    self.node_bonus_dict[description] += value
                    
        for bonus in self.node_bonus_dict:
            print bonus + '\t' + str(self.node_bonus_dict[bonus])
        #print self.node_bonus_dict
            