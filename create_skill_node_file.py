'''
Created on Apr 15, 2014

@author: Prutser
'''

import json

FILENAME = "Skilltree.txt"

def readfile(FILENAME):
    with open(FILENAME, 'r') as f:
        return json.loads(f.read())

def parsenodes(nodeinfo):
    textblob = ""
    for node in nodeinfo:
        line = ""
        line += str(node["id"]) + "\t"
        line += str(node['dn']) + "\t"
        for desc in node['sd']:
            line += desc + ';'
        line += '\t'
        textblob += line + "\n"
    return textblob

def writenodefile(textblob):
    with open("skillnodes.csv", 'w') as skillnodef:
        skillnodef.write(textblob)

data = readfile(FILENAME)
parsed_nodes = parsenodes(data["nodes"])
writenodefile(parsed_nodes)