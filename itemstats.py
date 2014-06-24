import json

class ItemStats(object):
    
    def __init__(self, path, charname):
        self.items_url = 'http://www.pathofexile.com/character-window/get-items?character='+charname
        
        self.item_info = {}
        
        # Item slots
        self.item_slots = set(['Helm', 'BodyArmour', 'Weapon', 'Weapon2', 'Offhand', 'Gloves', 'Boots', 'Amulet', 'Ring', 'Ring2', 'Belt'])
        
        # Retrieve a dictionary that contains all the items that are on the character
        self.items_dict = self.load_items_file(path)
    
    def handle_properties(self, properties):
        propdict = {}
        for prop in properties:
            if not prop['values']:
                propdict[prop['name']] = None
            else:
                propdict[prop['name']] = prop['values'][0][0]
        return propdict
    
    def handle_explicitmods(self, explicit_mods):
        explicit_moddict = {}
        for idx, mod in enumerate(explicit_mods):
            explicit_moddict[str(idx)] = mod
        return explicit_moddict
    
    def handle_implicitmods(self, implicit_mods):
        implicit_moddict = {}
        for idx, mod in enumerate(implicit_mods):
            implicit_moddict[str(idx)] = mod
        return implicit_moddict
    
    def get_item_info(self):
        
        # Loop over the items in the inventory
        for i in self.items_dict['items']:
            print i.keys()
            # Retrieve the inventory ID so we can filter only for equipped gear
            inv_id = i['inventoryId']
            
            # If it's an actual equipped item slot
            if inv_id in self.item_slots:
                
                # Create a dictionary for socket groups with the links for each group
                socket_groups = {}
                
                # Loop over the socket attribute of the items JSON
                for group in i['sockets']:
                    if group['group'] in socket_groups.keys():
                        # Add the socket color to the list value, this is used to calculate the number of links/bonuses
                        socket_groups[group['group']].append(group['attr'])
                    else:
                        # Add a new list value
                        socket_groups[group['group']] = [group['attr']]
                
                # Retrieve the gems that are equipped in the item
                slotted_gems = self.get_equipped_skill_gems(i)
                
                # Create a dictionary entry for the current equipment slot
                self.item_info[inv_id] = {}
                if 'properties' in i.keys():
                    self.item_info[inv_id]['properties'] = self.handle_properties(i['properties'])
                if 'explicitMods' in i.keys():
                    self.item_info[inv_id]['explicitMods'] = self.handle_explicitmods(i['explicitMods'])
                if 'implicitMods' in i.keys():
                    self.item_info[inv_id]['implicitMods'] = self.handle_implicitmods(i['implicitMods'])
                self.item_info[inv_id]['name'] = i['name']
                
                # Counter to put the correct skillgems in the correct link group
                counter = 0
                
                # Loop over the socket groups
                for group in sorted(socket_groups.keys()):
                    # Create an entry for the current socket group
                    self.item_info[inv_id][str(group)] = {}
                    
                    # Get the number of links for the current socket group
                    link_counter = len(socket_groups[group])
                    
                    # Add the socketed gems in the current link group
                    self.item_info[inv_id][str(group)]['slotted_gems'] = slotted_gems[counter:counter+link_counter]
                    
                    # Update the counter so we know which skill gem in the list to take next.
                    counter += link_counter
                    
        # Loop over the equipped items
        #for item in self.item_info:
            # Loop over the socket groups
        #    for socket_group in self.item_info[item]:
                # Print the socketed gems for each socket group of each item
        #        print item, socket_group, self.item_info[item][socket_group]
        return self.item_info
    
    def load_items_file(self, path):
        # Open the file in the given path, read the file and convert the JSON to a dictionary.
        with open(path, 'r') as itemsfile:
            return json.loads(str(itemsfile.read()))
    
    def extract_offensive_bonuses(self):
        pass
    
    def extract_defensive_bonuses(self):
        pass
    
    def get_equipped_skill_gems(self, item):
        # List of the skills equipped in the item
        equipped_skills = []
        
        # Socketed items attribute in the item JSON
        socketed_items = item['socketedItems']
        
        # If there are no socketed items this should be empty
        if not socketed_items:
            return
        # If there are socketed gems, loop over the socketed gems
        for i in socketed_items:
            
            # Get the skill name
            skill_name = i['typeLine']
            
            # Create the skill list
            skill_list = [skill_name]
            
            # Loop over the gem properties
            for prop in i['properties']:
                
                # If there's a value
                if prop['values']:
                    # Add the value and name to the skill list
                    skill_list.append([prop['values'][0][0], prop['name']])
                else:
                    # If these are the keywords, add a list of keywords
                    skill_list.append(prop['name'].split(', '))
            
            # Add the skill to the equipped skills list for this item
            equipped_skills.append(skill_list)
        return equipped_skills
    