"""This module contains function to calculate PoE related stuff, such as dps, crit chance, life, resists etcetera

@author: B.M.T.C. Aarts
"""

# Complex calculations
import math

class Calculations(object):
    """This class contains the functions to do the required calculations for the PoE related stuff"""
    def __init__(self):
        self.class_ = {"Scion":self.create_class_dict("Scion", 20, 20, 20, 40),
                       "Witch": self.create_class_dict("Witch", 14, 32, 14, 28),
                       "Shadow": self.create_class_dict("Shadow", 23, 23, 14, 44),
                       "Ranger": self.create_class_dict("Ranger", 32, 14, 14, 56),
                       "Duelist": self.create_class_dict("Duelist", 23, 14, 23, 44),
                       "Marauder": self.create_class_dict("Marauder", 14, 14, 32, 28),
                       "Templar": self.create_class_dict("Templar", 14, 23, 23, 28)}
        print self.class_
        self.life_per_level = 8
        self.mana_per_level = 4
        self.evasion_per_level = 3
        self.accuracy_per_level = 2
        self.starting_life = 50
        self.starting_mana = 40
        self.starting_evasion = 53
        
    def create_class_dict(self, class_, dex, intelligence, strength, accuracy):
        # Create a dictionary with the variable starting stats for each class
        class_dict = {"class": class_,
                      "dex": dex,
                      "int": intelligence,
                      "str": strength,
                      "accuracy_rating": accuracy}
        
        # Return the dictionary
        return class_dict
    
    def calculate_mana_cost(self, base_manacost, mana_multipliers):
        """This function calculates the mana cost for a spell or attack, based on the mana multipliers of the attached
        support gems
        
        @param base_manacost: The base manacost of the spell or attack
        @type base_manacost: int
        
        @param mana_multipliers: List that contains the mana multipliers of the attached support skill gems
        @type mana_multiplier: list
        
        @return: The mana cost of the active skill with the selected support gems linked
        @rtype: integer"""
        
        # Set the manacost to the base manacost of the skill before doing calculations with the support gems
        manacost = int(base_manacost)
        
        # Loop through the multipliers
        for multiplier in mana_multipliers:
            
            # Multiply the currency manacost by the multiplier / 100, to use the value multiplier
            # Use 100.0 to get a floating-point number as result from the calculation
            manacost *= (multiplier / 100.0)
        
        # Round the decimal value up and return the value
        return math.floor(manacost)
    
    def calculate_damage_per_hit(self, active_skill, weapon_phys_dmg, weapon_ele_dmg, added_gear_damage, passive_bonuses, *support_gems):
        """This function calculates the damage per hit of a given skill, with the selected equipment, support gems and passive bonuses etcetera
        
        @param active_skill: A dictionary that contains the active skill along with attributes of the skill, such as damage effectiveness,
        level, quality bonus, quality percentage etcetera
        @type active_skill: dictionary
        
        @param weapon_phys_dmg: The base physical damage of the weapon as displayed on the weapon. First element in the list contains the minimum
        damage, the second element contains the maximum physical damage
        @type weapon_phys_dmg: list
        
        @param weapon_ele_dmg: Dictionary that contains a list with the min and max damage value for each element
        @type weapon_ele_dmg: dict
        
        @param added_gear_damage: Dictionary that contains the minimum and maximum added damage from gear, except for weapon, for each type of damage
        @type added_gear_damage: dict
        
        @param passive_bonuses: Dictionary that contains all the damage modifiers (except for attack speed maybe)
        @type passive bonuses: dict
        
        @param *support_gems: One or more dictionaries that represent a support skill along with damage modifiers and skill level etcetera
        @type support_gem: dict"""
        
        pass
    
    def calculate_damage_per_second(self, damage_per_hit, chance_to_hit, crit_multiplier=150, crit_chance=0, weapon_atk_speed=None, inc_atk_speed=None, base_cast_time=None, increased_cast_speed=None):
        # If it's not a spell
        if not base_cast_time:
            # Calculate the attacks per second
            aps = float(weapon_atk_speed) * float(1 + (inc_atk_speed / 100.0))
            
            # Calculate the rounded attacks per second, down to two decimals
            rounded_aps = math.floor(aps * 100) / 100.0
            
            # Set chance_to_crit to zero to avoid DivisionByZero errors
            chance_to_crit = 0
            
            # If the user can actually crit
            if crit_chance > 0:
                # Calculate the crit chance using 1 as max instead of 100
                chance_to_crit = crit_chance / 100.0
            
            # Calculate non-crit chance of attack
            chance_to_not_crit = 1 - chance_to_crit
            
            # Calculate crit damage
            crit_dps = damage_per_hit * chance_to_crit * (crit_multiplier / 100.0)
            
            # Calculate non_crit damage
            non_crit_dps = damage_per_hit * chance_to_not_crit
            
            # Add non-crit and crit damage, multiply by the rounded_aps and factor in accuracy
            return chance_to_hit * (crit_dps + non_crit_dps) * rounded_aps
    
    def calculate_crit_chance(self, increased_critical_strike_chance, weapon_crit_chance, base_crit_chance=None):
        # Calculate crit chance if it's a spell
        if base_crit_chance:
            return base_crit_chance * (1 + (increased_critical_strike_chance / 100.0))
        # Use weapon crit for non-spells
        else:
            return weapon_crit_chance * (1 + (increased_critical_strike_chance / 100.0))
    
    def calculate_crit_multiplier(self, base_crit_multiplier, increased_crit_multiplier):
        return base_crit_multiplier * (1 + (increased_crit_multiplier / 100.0))
    
    def calculate_resistances_per_difficulty(self, resist_dict, max_resist_increase):
        # Difficulties with resist penalties
        DIFFICULTIES = [("Normal", 0), ("Cruel", 20), ("Merciless", 60)]
        
        # Dictionary to store resists per difficulty
        res_per_difficulty = {}
        
        # Initialize dictionary that's used to calculate total resist
        total_res_dict = {'lightning_res': 0,
                          'cold_res': 0,
                          'fire_res': 0,
                          'chaos_res': 0}
        
        #TODO: Add support for +max resist from items
        # Calculate max resist
        max_resist = 75 + int(max_resist_increase)
        
        # Loop over the dictionaries in the resist dict
        for dic in resist_dict:
            # Add the resistances
            total_res_dict["lightning_res"] += resist_dict[dic]["lightning_res"]
            total_res_dict["cold_res"] += resist_dict[dic]["cold_res"]
            total_res_dict["fire_res"] += resist_dict[dic]["fire_res"]
            total_res_dict["chaos_res"] += resist_dict[dic]["chaos_res"]
        
        # Loop over the difficulties
        for difficulty in DIFFICULTIES:
            
            # Retrieve the actual difficulty value
            difficulty_string = difficulty[0]
            
            # Add a nested dict for the current difficulty
            res_per_difficulty[difficulty_string] = {}
            
            # Loop over the total resistances
            for res in total_res_dict:
                
                # Add a nested dict for the current resistance item
                res_per_difficulty[difficulty_string][res] = {}
                
                # Retrieve the uncapped resistance
                uncapped_res = total_res_dict[res]
                
                # Calculate resist at given difficulty
                resist_on_difficulty = uncapped_res - difficulty[1]
                
                # If the resist on this difficulty exceeds the max resist, set it to be the max resist
                if resist_on_difficulty >= max_resist:
                    resist_on_difficulty = max_resist
                
                # Add the uncapped res and capped res
                res_per_difficulty[difficulty_string][res]["uncapped_res"] = uncapped_res
                res_per_difficulty[difficulty_string][res]["capped_res"] = resist_on_difficulty
        
        # Return a dictionary that contains all the resistances per difficulty
        return res_per_difficulty
                
    
    def calculate_maximum_life(self, class_, level, life_on_gear, life_from_passives, increased_max_life):
        pass

res_dict = {"gear": {"lightning_res": 75,
                     "cold_res": 75,
                     "fire_res": 75,
                     "chaos_res": 75},
            "passives": {"lightning_res": 0,
                         "fire_res": 0,
                         "cold_res": 0,
                         "chaos_res": 16}}

calc = Calculations()
print calc.calculate_resistances_per_difficulty(res_dict, 0)
print calc.calculate_mana_cost(11, [205, 150, 130, 150])
print calc.calculate_damage_per_second(351, 1, 0, 0, 1.89, 47)
print calc.calculate_damage_per_second(351, 0.9, 0, 0, 1.89, 47)
print calc.calculate_crit_chance(575, 9.1)
print "Bram z'n char"
print calc.calculate_damage_per_second(100, 1, 200, 50, 1.0, 100)