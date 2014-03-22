# Parsing inventory/items
import json


class items(object):
    """This class contains functions related to equipment"""
    
    def __init__(self):
        # List that contains the itemslots
        self.itemslots = []
        
        # Total added physical damage from gear for the current character
        self.addedphysicaldamage = 0
        
        # Total added lightning damage from gear for the current character
        self.addedlightningdamage = 0
        
        # Total added cold damage from gear for the current character
        self.addedcolddamage = 0
        
        # Total added fire damage from gear for the current character
        self.addedfiredamage = 0
        
        # Total added chaos damage from gear
        self.addedchaosdamage = 0
        
        # Total added attack speed from gear
        self.addedatkspeed = 0
        
        # Total added critical strike chance from gear
        self.addedcritchance = 0
        
        # Total added critical strike multiplier from gear
        self.addedcritmulti = 0

    def importItems(self):
        """The importItems function loads a file that contains equipment/inventory of a character.
        Put the contents of the download link in a file called items.txt
        
        @return inventory_dict: Dictionary that contains the inventory/equipment information as listed on the PoE website
        @rtype: dict
        """
        
        with open('items.txt', 'r') as itemsfile:
            return json.loads(itemsfile.read())
