'''
Created on Apr 15, 2014

@author: Prutser
'''

import json

FILENAME = "Skilltree.txt"

def readfile(FILENAME):
    # Open the skilltree nodes file in read mode
    with open(FILENAME, 'r') as f:
        # Read the contents, parse to JSON object and return
        return json.loads(f.read())

def parsenodes(nodeinfo):
    # Raw text that contains node info
    textblob = ""
    # Loop over each node
    for node in nodeinfo:
        # Make empty line
        line = ""
        # Add node id
        line += str(node["id"]) + "\t"
        # Add node name
        line += str(node['dn']) + "\t"
        # Add node bonuses
        for desc in node['sd']:
            # If there are multiple descriptions, separate them with a semicolon
            line += desc + ';'
        # Add the line to the textblob and add a newline character
        textblob += line + "\n"
    # Return the blob of text
    return textblob

def writenodefile(textblob):
    # Open the skillnodes file in write modus
    with open("skillnodes.csv", 'w') as skillnodef:
        # Write the textblob to the file
        skillnodef.write(textblob)

data = readfile(FILENAME)
parsed_nodes = parsenodes(data["nodes"])
writenodefile(parsed_nodes)