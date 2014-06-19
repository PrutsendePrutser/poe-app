import json

class ItemStats(object):
    
    def __init__(self, path, charname):
        self.items_url = 'http://www.pathofexile.com/character-window/get-items?character='+charname
        
        self.item_info = {}
        
        # Item slots
        self.item_slots = set(['Helm', 'BodyArmour', 'Weapon', 'Weapon2', 'Offhand', 'Gloves', 'Boots', 'Amulet', 'Ring', 'Ring2', 'Belt'])
        
        # Retrieve a dictionary that contains all the items that are on the character
        self.items_dict = self.load_items_file(path)
        
        self.get_item_info()
    
    def get_item_info(self):
        for i in self.items_dict['items']:
            inv_id = i['inventoryId']
            if inv_id in self.item_slots:
                #for k in i.keys():
                #    print k
                self.item_info[inv_id] = {}
                self.item_info[inv_id]['slotted_gems'] = self.get_equipped_skill_gems(i)
        print self.item_info
        
        for c in self.items_dict['character']:
            print self.items_dict['character'][c]
        
    
    def load_items_file(self, path):
        # Open the file in the given path, read the file and convert the JSON to a dictionary.
        with open(path, 'r') as itemsfile:
            return json.loads(str(itemsfile.read()))
    
    def extract_offensive_bonuses(self):
        pass
    
    def extract_defensive_bonuses(self):
        pass
    
    def get_equipped_skill_gems(self, item):
        equipped_skills = {}
        #print self.items_dict['items']
        socketed_items = item['socketedItems']
        if not socketed_items:
            return
        for i in socketed_items:
            skill_name = i['typeLine']
            equipped_skills[skill_name] = {}
            #print skill_name
            for prop in i['properties']:
                if prop['values']:
                    equipped_skills[skill_name][prop['name']] = prop['values'][0][0]
                else:
                    equipped_skills[skill_name]['keywords'] = prop['name'].split(', ')
            #print '\n'
        return equipped_skills
            
        
        #for socketedItem in self.items_dict['items'][0][item_slot]['socketedItems']:
            #print socketedItem
    
ItemStats('files/items.txt', 'PrutsMarauder')