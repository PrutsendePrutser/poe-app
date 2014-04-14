import base64
import json

class PassiveCalculator(object):
    
    def __init__(self, build_url):
        """Initialize class instance"""
        # Set the build url that the user entered
        self.build_url = build_url
        
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
            print ((i-6) / 2), (build[i+1] + build[i+0])
                
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
        with open("skilltree.txt", "r") as sfile:
            return json.loads(sfile.read())

