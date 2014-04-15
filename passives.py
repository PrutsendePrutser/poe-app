import base64

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
                c = (build[i+1] + build[i+0]).decode("utf-16")
                if c == "":
                    c = "  "
                node_ids.append(ord(c))
            except UnicodeDecodeError:
                print "Error: ", (build[i+1] + build[i+0])
            except TypeError:
                print "C: ", repr(c)
            
            
        # When we have parsed the full build url, return the node_ids
        return node_ids
    
    def load_nodes_data(self):
        with open("skillnodes.csv", "r") as sfile:
            lines = sfile.readlines()
            node_dict = {}
            for line in lines:
                split = line.split('\t')
                nodeid = split[0]
                name = split[1]
                desc = [d.replace(';', '').strip() for d in split[2].split(';') if d.strip()]
                node_dict[nodeid] = {'name': name,
                                     'desc': desc}
            return node_dict

    def get_bonus_for_selected_nodes(self):
        for idx, n in enumerate(sorted(self.selected_node_ids)):
            node_name = self.node_data[str(n)]['name']
            node_desc = self.node_data[str(n)]['desc']
            print idx, node_name, node_desc
            
calc = PassiveCalculator('http://www.pathofexile.com/passive-skill-tree/AAAAAgEAxthYYz38jM_2SF8_8wbBBOOfoLRBdCcv-6p2K-8O5FH3TbyfgIqkrCSb8i8B51RJqBinMDboah4UcRQgZKOvoliv0iEOPN-_UEcaVRDwRmn3vlcNn8sYkWEhkc6E77vtm4N07fcyU99673KpWNusr2BLfNmE2QUtbmllTUCgvqdHfiFgnrnSTavFdPHBB8APGNvUUtd-W68G7jQ1TirdDZdwKaWQCvzFYxdW-megzme3F-4Oh3YPODiWGtsj9kp918vv8LfTWkg94kjuG61yu7nNoW0=')
calc.get_bonus_for_selected_nodes()