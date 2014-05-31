import json

class ItemStats(object):
    
    def __init__(self, path):
        # Item slots
        self.item_slots = set(['Helm', 'BodyArmour', 'Weapon', 'Weapon2', 'Offhand', 'Gloves', 'Boots', 'Amulet', 'Ring', 'Ring2', 'Belt'])
        
        # Retrieve a dictionary that contains all the items that are on the character
        self.items_dict = self.load_items_file(path)
        
    def load_items_file(self, path):
        # Open the file in the given path, read the file and convert the JSON to a dictionary.
        with open(path, 'r') as itemsfile:
            return json.loads(itemsfile.read())
    
    def extract_offensive_bonuses(self):
        pass
    
    def extract_defensive_bonuses(self):
        pass
    
    def get_equipped_skill_gems(self):
        pass
    
ItemStats('files/items.txt')