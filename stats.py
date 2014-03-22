# Parsing inventory/items
import json


class items(object):
    """This class contains functions related to equipment"""
    
    def __init__(self):
        
        # Dictionary that contains the complete inventory including equipped gear
        self.inventory = self.importItems()["items"]
        
        # List that contains the itemslots
        self.itemslots = ['Weapon', 'Amulet', 'Weapon2', 'Gloves', 'Ring2', 'Boots', 'Belt', 'Helm', 'Ring', 'Offhand', 'BodyArmour']
        
        # Dictionary that contains the items that are actually equipped
        self.equipped_items_dict = self.createItemDict()
        print self.equipped_items_dict
        
        # Extract damage increases from gear
        self.extractdamageincreases()
        
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
        
    def extractdamageincreases(self):
        """This function extracts mods that increase the damage from an attack from items"""
        
        # Loop over the equipped items
        for equipped_item in self.equipped_items_dict.keys():
            
            # Print the itemslot
            print '\n\n{}\n'.format(equipped_item)
            
            # If there are any implicit mods on this item
            if 'implicitMods' in self.equipped_items_dict[equipped_item].keys():
                # Loop over the implicit mods
                for implicit_mod in self.equipped_items_dict[equipped_item]['implicitMods']:
                    
                    # Print the mod
                    print "Implicit Mod: " + implicit_mod
            
            # If there are any explicit mods on the item
            if 'explicitMods' in self.equipped_items_dict[equipped_item].keys():
                
                # Loop over the explicit mods
                for explicit_mod in self.equipped_items_dict[equipped_item]['explicitMods']:
                    
                    # Print the mod
                    print "Explicit Mod: " + explicit_mod
        
    def createItemDict(self):
        """This function creates a dictionary of equipped items with their implicit and explicit mods
        
        @return: Dictionary that contains the equipped items with separately the explicit and implicit mods
        @rtype: dict
        """
        # Dictionary to stoe the items in
        item_dict = {}
        
        # Loop over the itemslots
        for slot in self.itemslots:
            
            # Retrieve the mods for each equipped item
            item_dict[slot] = self.getitemstats(slot)
            
        return item_dict

    def importItems(self):
        """The importItems function loads a file that contains equipment/inventory of a character.
        Put the contents of the download link in a file called items.txt
        
        @return inventory_dict: Dictionary that contains the inventory/equipment information as listed on the PoE website
        @rtype: dict
        """
        
        with open('items.txt', 'r') as itemsfile:
            return json.loads(itemsfile.read())
    
    def getitemstats(self, slot):
        """This function retrieves the explicit and implict mods of an item
        
        @return: a dictionary that contains a list of implicit mods and a list of explicit mods of an item
        @rtype: dict"""
        
        # Loop through the inventory items
        for item in self.inventory:
            
            # Create lists to store explicit and implicit properties
            implicitproperties = []
            explicitproperties = []
            
            # If we have the data from the current slot
            if item['inventoryId'] == slot:
                
                # Retrieve the explicit and implicit mods separately
                if "explicitMods" in item.keys():
                    explicitproperties = item['explicitMods']
                if "implicitMods" in item.keys():
                    implicitproperties = item["implicitMods"]
                
                # Return a dictionary containing the explicit and implicit mods
                return {'explicitMods': explicitproperties,
                        'implicitMods': implicitproperties}

items()