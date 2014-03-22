"""
This class contains all the active skill gems and support skill gems in Path of Exile
with their stats and information
"""

class Skillgems(object):
    
    # Initialize class vars
    def __init__(self):
        self.active_skills = {}
        self.support_skills = {}