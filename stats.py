# Parsing inventory/items
import json


class items(object):
    """This class contains functions related to equipment"""
    
    def __init__(self):
        
        # Dictionary to store item stats
        self.itemstats = \
        {'minphysdmg': 0,
         'maxphysdmg': 0,
         'minlightningdmg': 0,
         'maxlightningdmg': 0,
         'mincolddmg': 0,
         'maxcolddmg': 0,
         'minfiredmg': 0,
         'maxfiredmg': 0,
         'minchaosdmg': 0,
         'maxchaosdmg': 0,
         'addedatkspeed': 0,
         'addedcritchance': 0,
         'addedcritmulti': 0,
         'addedlife': 0,
         'addedcoldres': 0,
         'addedfireres': 0,
         'addedlightningres': 0}
        
        # Dictionary that contains the complete inventory including equipped gear
        self.inventory = self.importItems()["items"]
        
        # List that contains the itemslots
        self.itemslots = ['Weapon', 'Amulet', 'Gloves', 'Ring2', 'Boots', 'Belt', 'Helm', 'Ring', 'Offhand', 'BodyArmour']
        
        # Dictionary that contains the items that are actually equipped
        self.equipped_items_dict = self.createItemDict()

        # Extract damage increases from gear
        self.extractdamageincreases()
        
    def extractdamageincreases(self):
        """This function extracts mods that increase the damage from an attack from items"""
        
        # Loop over the equipped items
        for equipped_item in self.equipped_items_dict.keys():
            
            # If there are any implicit mods on this item
            if 'implicitMods' in self.equipped_items_dict[equipped_item].keys():
                # Loop over the implicit mods
                for implicit_mod in self.equipped_items_dict[equipped_item]['implicitMods']:
                    pass
            # If there are any explicit mods on the item
            if 'explicitMods' in self.equipped_items_dict[equipped_item].keys():
                
                # Loop over the explicit mods
                for explicit_mod in self.equipped_items_dict[equipped_item]['explicitMods']:
                    
                    # Add lightning resistance
                    if explicit_mod.endswith('Lightning Resistance'):
                        lightningres = int(explicit_mod.split('%')[0].lstrip('+'))
                        self.itemstats['addedlightningres'] += lightningres
                        
                    # Add cold resistance
                    elif explicit_mod.endswith('Cold Resistance'):
                        coldres = int(explicit_mod.split('%')[0].lstrip('+'))
                        self.itemstats['addedcoldres'] += coldres
                    
                    # Add fire resistance
                    elif explicit_mod.endswith('Fire Resistance'):
                        fireres = int(explicit_mod.split('%')[0].lstrip('+'))
                        self.itemstats['addedfireres'] += fireres
                        
                    # Add resist for all elemental resistances
                    elif explicit_mod.endswith('Elemental Resistances'):
                        
                        # Retrieve the amount of elemental resistances added by the item
                        eleres = int(explicit_mod.split('%')[0].lstrip('+'))
                        
                        # Add the resistance bonus to all elemental resistances
                        self.itemstats['addedcoldres'] += eleres
                        self.itemstats['addedfireres'] += eleres
                        self.itemstats['addedlightningres'] += eleres
                    
                    # Add the added lightning damage
                    elif explicit_mod.endswith('Lightning Damage'):
                        
                        # Get the minimum added lightning damage
                        minlightningdamage = int(explicit_mod.split('-')[0].split(' ')[1])
                        
                        # Get the maximum added lightning damage
                        maxlightningdamage = int(explicit_mod.split('-')[1].split(' ')[0])
                        
                        # Add the lightning damage
                        self.itemstats['minlightningdmg'] += minlightningdamage
                        self.itemstats['maxlightningdmg'] += maxlightningdamage
                    
                    # Add the added cold damage
                    elif explicit_mod.endswith('Cold Damage'):
                        
                        # Get the minimum added cold damage
                        mincolddamage = int(explicit_mod.split('-')[0].split(' ')[1])
                        
                        # Get the maximum added cold damage
                        maxcolddamage = int(explicit_mod.split('-')[1].split(' ')[0])
                        
                        # Add the cold damage
                        self.itemstats['mincolddmg'] += mincolddamage
                        self.itemstats['maxcolddmg'] += maxcolddamage
                        
                    # Add the added fire damage
                    elif explicit_mod.endswith('Fire Damage'):
                        
                        # Get the minimum added fire damage
                        minfiredamage = int(explicit_mod.split('-')[0].split(' ')[1])
                        
                        # Get the maximum added fire damage
                        maxfiredamage = int(explicit_mod.split('-')[1].split(' ')[0])
                        
                        # Add the fire damage
                        self.itemstats['minfiredmg'] += minfiredamage
                        self.itemstats['maxfiredmg'] += maxfiredamage
                        
                    # Add the added life from gear
                    elif explicit_mod.endswith('maximum Life'):
                        
                        # Retrieve the life and add it to the added life parameter
                        self.itemstats['addedlife'] += int(explicit_mod.split(' to')[0].lstrip('+'))
                        
                    # Add global crit multiplier
                    elif explicit_mod.endswith('Global Critical Strike Multiplier'):
                        
                        # Extract the value
                        critmulti = explicit_mod.split('%')[0].strip()
                        
                        # Add the crit multiplier
                        self.itemstats['addedcritmulti'] += int(critmulti)
                    
                    # Add global crit chance
                    elif explicit_mod.endswith('GLobal Critical Strike Chance'):
                        
                        # Extract the value
                        critchance = explicit_mod.split('%')[0].strip()
                        
                        # Add the crit chance
                        self.itemstats['addedcritchance'] += int(critchance)
                        
                    
                    # Add added the following stats only when they're not on the weapon
                    if not equipped_item == 'Weapon' and not equipped_item == 'Weapon2':
                    
                        # Add attack speed mods
                        if explicit_mod.endswith('Attack Speed'):
                            
                            # Retrieve the attack speed and add it
                            self.itemstats['addedatkspeed'] += int(explicit_mod.split('%')[0])
                        
                        # Add added phys damage
                        elif explicit_mod.endswith('Physical Damage'):
                            
                            # Extract values
                            minphysdmg = explicit_mod.split('-')[0].split(' ')[1]
                            maxphysdmg = explicit_mod.split('-')[1].split(' ')[0]
                            
                            # Add the values
                            self.itemstats['minphysdmg'] = int(minphysdmg)
                            self.itemstats['maxphysdmg'] = int(maxphysdmg)
                        
                    # Print the mod
             #       print "Explicit Mod: " + explicit_mod
        
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
            print item['sockets']
            for k in item:
                #print k + '\t' + str(item[k])
                if k == 'socketedItems':
                    #print item[k]
                    for l in item[k]:
                        print str(l['properties'])
                        print str(l['additionalProperties'])
                        print str(l['typeLine'])
                        print str(l['socket'])
            
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