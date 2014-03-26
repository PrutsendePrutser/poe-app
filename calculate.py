"""This module contains function to calculate PoE related stuff, such as dps, crit chance, life, resists etcetera

@author: B.M.T.C. Aarts
"""

# Complex calculations
import math

class Calculations(object):
    """This class contains the functions to do the required calculations for the PoE related stuff"""
    def __init__(self):
        pass
    
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
    
    def calculate_damage_per_second(self, damage_per_hit, weapon_atk_speed=None, inc_atk_speed=None, base_cast_time=None, increased_cast_speed=None):
        # If it's not a spell
        if not base_cast_time:
            print (float(weapon_atk_speed) * math.floor(float(1 + (inc_atk_speed / 100.0))))
            # Return the damage per second
            return damage_per_hit * (math.floor(float(weapon_atk_speed) * float(1 + (inc_atk_speed / 100.0)) * 100) / 100)
    
    def calculate_crit_chance(self, increased_critical_strike_chance, weapon_crit_chance, base_crit_chance=None):
        if base_crit_chance:
            return base_crit_chance * (1 + (increased_critical_strike_chance / 100.0))
        else:
            return weapon_crit_chance * (1 + (increased_critical_strike_chance / 100.0))
    
    def calculate_crit_multiplier(self, base_crit_multiplier, increased_crit_multiplier):
        pass
    
    def calculate_resistances_per_difficulty(self, gear_resist, passives_resist, max_resist_increase):
        pass
    
    def calculate_maximum_life(self, class_, level, life_on_gear, life_from_passives, increased_max_life):
        pass

calc = Calculations()
print calc.calculate_mana_cost(11, [205, 150, 130, 150])
print calc.calculate_damage_per_second(351, 1.89, 47)
print calc.calculate_crit_chance(575, 9.1)
print "Bram z'n char"
print calc.calculate_damage_per_second(100, 1.2, 16)