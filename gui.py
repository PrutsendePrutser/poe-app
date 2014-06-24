import sys
import passives
import itemstats
from PyQt4 import QtGui, QtCore

class PoEGUI(QtGui.QWidget):
    
    def __init__(self):
        super(PoEGUI, self).__init__()
        
        # Var to store all the support skills
        self.passive_skills = ['Multistrike', 'Faster Casting', 'Elemental Proliferation', 'Melee Physical Damage', 'Chain', "Faster Attacks"]
        
        # Var to store all the active skills
        self.active_skills = ["Arc", "Spectral Throw", "Flameblast"]
        
        self.initUI()
        
        self.add_gear_to_UI()
        
    def add_gear_to_UI(self):
        
        # Dictionary that contains the mapping from inventory ID to GUI element
        gearslot_mapping = {'Helm': self.helm_name_box,
                            'BodyArmour': self.chest_name_box,
                            'Weapon': self.mh_name_box,
                            'Offhand': self.oh_name_box,
                            'Gloves': self.gloves_name_box,
                            'Boots': self.boots_name_box,
                            'Amulet': self.amulet_name_box,
                            'Ring': self.ring_one_name_box,
                            'Ring2': self.ring_two_name_box,
                            'Belt': self.belt_name_box}

        # Retrieve the items from the items file that was selected by the user
        self.equipped_items = itemstats.ItemStats('files/items.txt', 'PrutsMarauder').get_item_info()
        # Loop over the item slots
        for item in self.equipped_items:
            # Skip secondary weapon for now, since we don't have a box for that
            # TODO: Implement weapon swap option for secondary mainhand/offhand/2H
            if item != 'Weapon2':
                # Update the text of the item name box with the name of the item
                # TODO: Add base item type to the name, separated by a comma
                gearslot_mapping[item].setText(str(self.equipped_items[item]['name']))
        
    def handle_load_build_url(self):
        # Get the build URL
        build_url = self.build_url_box.text()
        
        # Create an instance of the passives parser
        passive_parser = passives.PassiveCalculator(build_url)
        
        # Retrieve the passive bonuses of the given tree URL
        statsblob = passive_parser.get_bonus_for_selected_nodes()
        
        # Display the stats in the statbox
        self.statbox.setText(statsblob)
    
    def make_support_skills_available(self, *support_skill_slots):
        # Create a set that contains all of the support skills that we have
        all_supports = set(self.support_skill_dict.keys())
        
        # Create a set that contains the support skills that are selected in the dropdown menus
        support_skill_slots = set(support_skill_slots)
        
        # Create a set that contains elements that are not selected yet
        difference = all_supports.difference(support_skill_slots)
        
        # Loop over these skills
        for skill in difference:
            
            # Set the skill to available
            self.support_skill_dict[skill] = True
        
        # Update the available support skills for each dropdown menu
        self.set_available_support_skills()
    
    def set_available_support_skills(self):
        # Retrieve the values that are selected in the dropdown menus
        support_skill_one = self.support_skill_combobox_one.currentText()
        support_skill_two = self.support_skill_combobox_two.currentText()
        support_skill_three = self.support_skill_combobox_three.currentText()
        support_skill_four = self.support_skill_combobox_four.currentText()
        support_skill_five = self.support_skill_combobox_five.currentText()
        
        # Get the list of available support skills
        available_skills = self.get_available_support_skills(self.support_skill_dict)
        
        # Update skill list for box one
        self.support_skill_combobox_one.clear()
        self.support_skill_combobox_one.addItems(available_skills + [support_skill_one])
        self.support_skill_combobox_one.setCurrentIndex(self.support_skill_combobox_one.findText(support_skill_one))
        
        # Update skill list for box two
        self.support_skill_combobox_two.clear()
        self.support_skill_combobox_two.addItems(available_skills + [support_skill_two])
        self.support_skill_combobox_two.setCurrentIndex(self.support_skill_combobox_two.findText(support_skill_two))
        
        # Update skill list for box three
        self.support_skill_combobox_three.clear()
        self.support_skill_combobox_three.addItems(available_skills + [support_skill_three])
        self.support_skill_combobox_three.setCurrentIndex(self.support_skill_combobox_three.findText(support_skill_three))
        
        # Update skill list for box four
        self.support_skill_combobox_four.clear()
        self.support_skill_combobox_four.addItems(available_skills + [support_skill_four])
        self.support_skill_combobox_four.setCurrentIndex(self.support_skill_combobox_four.findText(support_skill_four))
        
        # Update the skill list for box five
        self.support_skill_combobox_five.clear()
        self.support_skill_combobox_five.addItems(available_skills + [support_skill_five])
        self.support_skill_combobox_five.setCurrentIndex(self.support_skill_combobox_five.findText(support_skill_five))
    
    def update_available_support_skills(self, val):
        # Retrieve the combobox that was triggered
        sender = self.sender()
        
        # Retrieve the value of the triggered dropdown
        self.support_skill_dict[str(sender.currentText())] = False
        
        # Get the values of each of the dropdowns
        support_val_one = str(self.support_skill_combobox_one.currentText())
        support_val_two = str(self.support_skill_combobox_two.currentText())
        support_val_three = str(self.support_skill_combobox_three.currentText())
        support_val_four = str(self.support_skill_combobox_four.currentText())
        support_val_five = str(self.support_skill_combobox_five.currentText())
        
        # Make the support skills that aren't selected available
        self.make_support_skills_available(support_val_one, support_val_two, support_val_three, support_val_four, support_val_five)
        
    def initUI(self):
        
        # Box to show stats from gear and passives
        self.statbox = QtGui.QTextEdit()
        self.statbox.setReadOnly(True)
        self.statbox.setText("sadasdasd\nasdsadsadsaads")
        
        # Create a grid layout
        grid = QtGui.QGridLayout()
        
        # Add some spacing
        grid.setSpacing(8)
        
        self.add_build_url_widgets(grid)
        
        # Add the passive data box below the build URL box and make it span 20 lines
        grid.addWidget(self.statbox, 9, 0, 13, 23)
        
        # Add active skill gem widget
        self.create_active_skill_combo_box(grid)
        
        # Add support skill gem widgets
        self.create_passive_skill_combo_boxes(grid)
        
        # Add the offensive stats
        self.add_offensive_stats(grid)
        
        # Add the defensive stats
        self.add_defensive_stats(grid)
        
        self.add_item_customization(grid)
        
        # Set the layout
        self.setLayout(grid)
        
        # Set the size of the app
        self.setGeometry(100, 100, 1200, 600)
        
        # Set the window title
        self.setWindowTitle("Path of Exile DPS calculator")
        
        # Show the window
        self.show()
    
    def add_build_url_widgets(self, grid):
        # Build URL label
        self.build_url_lbl = QtGui.QLabel("Build URL")
        
        # QLineEdit to enter build URL
        self.build_url_box = QtGui.QLineEdit()
        
        # Create the build URL load button
        self.build_url_load_btn = QtGui.QPushButton("Load build")
        self.build_url_load_btn.clicked.connect(self.handle_load_build_url)
        
        # Add the label above the build url box
        grid.addWidget(self.build_url_lbl, 0, 0, 1, 6)
        grid.addWidget(self.build_url_box, 1, 0, 1, 22)
        
        # Add spacer label
        grid.addWidget(self.build_url_load_btn, 1, 22)
        
        
    def create_active_skill_combo_box(self, grid):
        # Create label for active skill
        self.active_skill_lbl = QtGui.QLabel("Active skill")
        
        # Create a dropdown
        self.active_skill = QtGui.QComboBox()
        active_skills = ["Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw"]
        
        # Fill dropdown with active skills
        for skill in active_skills:
            self.active_skill.addItem(skill)
            
        # Add active skill label to grid
        grid.addWidget(self.active_skill_lbl, 2, 19)
        
        # Add active skill dropdown to grid
        grid.addWidget(self.active_skill, 2, 20)
        
        # Retrieve level label and level selection dropdown
        level_lbl, self.active_level_box = self.add_gem_level_selection_widget()
        
        # Add the level label and level selection dropdown to the grid
        grid.addWidget(level_lbl, 2, 21)
        grid.addWidget(self.active_level_box, 2, 22)
        
    def create_passive_skill_combo_boxes(self, grid):
        #self.support_skill_boxes = []
        
        # Dictionary to store the support skill gems with their available state (True for available, False for in use
        self.support_skill_dict = {}
        
        # Loop over all the passive skills
        for s in self.passive_skills:
            # Add them to the dictionary and set them to available by default
            self.support_skill_dict[s] = True
        
        # Sorted list of the support skills
        support_skills = sorted(self.support_skill_dict.keys())
        
        # Add 5 widgets, starting with support skill 1
        
        # Create the label
        support_skill_lbl_one = QtGui.QLabel("Support skill 1")
        
        # Add the widget to the next row, 3rd column
        grid.addWidget(support_skill_lbl_one, 3, 19)
        
        # Create a combobox widget
        self.support_skill_combobox_one = QtGui.QComboBox()
        self.support_skill_combobox_one.activated[str].connect(self.update_available_support_skills)
        
        # Loop over the passive skills and add them to the combo box
        for s in self.get_available_support_skills(support_skills):
            self.support_skill_combobox_one.addItem(s)
        
        # Add the combo box widget to the grid
        grid.addWidget(self.support_skill_combobox_one, 3, 20)
        
        # Retrieve the skill that's displayed in the current dropdown and set it to False, so that
        # it is not shown in other dropdowns when it's already selected.
        selected_skill = str(self.support_skill_combobox_one.currentText())
        self.support_skill_dict[selected_skill] = False
        
        # Get the level label and level selection box
        level_lbl, self.support_level_box_one = self.add_gem_level_selection_widget()
        
        # ..and add them to the grid
        grid.addWidget(level_lbl, 3, 21)
        grid.addWidget(self.support_level_box_one, 3, 22)
        #self.support_skill_boxes.append([support_skill_combobox, level_box])
        
        # Create the label
        support_skill_lbl_two = QtGui.QLabel("Support skill 2")
        
        # Add the widget to the next row, 3rd column
        grid.addWidget(support_skill_lbl_two, 4, 19)
        
        # Create a combobox widget
        self.support_skill_combobox_two = QtGui.QComboBox()
        self.support_skill_combobox_two.activated[str].connect(self.update_available_support_skills)
        
        # Loop over the passive skills and add them to the combo box
        for s in self.get_available_support_skills(support_skills):
            self.support_skill_combobox_two.addItem(s)
        
        # Add the combo box widget to the grid
        grid.addWidget(self.support_skill_combobox_two, 4, 20)
        
        # Retrieve the skill that's displayed in the current dropdown and set it to False, so that
        # it is not shown in other dropdowns when it's already selected.
        selected_skill = str(self.support_skill_combobox_two.currentText())
        self.support_skill_dict[selected_skill] = False
        
        # Get the level label and level selection box
        level_lbl, self.support_level_box_two = self.add_gem_level_selection_widget()
        
        # ..and add them to the grid
        grid.addWidget(level_lbl, 4, 21)
        grid.addWidget(self.support_level_box_two, 4, 22)
        
        # Create the label
        support_skill_lbl_three = QtGui.QLabel("Support skill 3")
        
        # Add the widget to the next row, 3rd column
        grid.addWidget(support_skill_lbl_three, 5, 19)
        
        # Create a combobox widget
        self.support_skill_combobox_three = QtGui.QComboBox()
        self.support_skill_combobox_three.activated[str].connect(self.update_available_support_skills)
        
        # Loop over the passive skills and add them to the combo box
        for s in self.get_available_support_skills(support_skills):
            self.support_skill_combobox_three.addItem(s)
        
        # Add the combo box widget to the grid
        grid.addWidget(self.support_skill_combobox_three, 5, 20)
        
        # Retrieve the skill that's displayed in the current dropdown and set it to False, so that
        # it is not shown in other dropdowns when it's already selected.
        selected_skill = str(self.support_skill_combobox_three.currentText())
        self.support_skill_dict[selected_skill] = False
        
        # Get the level label and level selection box
        level_lbl, self.support_level_box_three = self.add_gem_level_selection_widget()
        
        # ..and add them to the grid
        grid.addWidget(level_lbl, 5, 21)
        grid.addWidget(self.support_level_box_three, 5, 22)
        
        # Create the label
        support_skill_lbl_four = QtGui.QLabel("Support skill 4")
        
        # Add the widget to the next row, 3rd column
        grid.addWidget(support_skill_lbl_four, 6, 19)
        
        # Create a combobox widget
        self.support_skill_combobox_four = QtGui.QComboBox()
        self.support_skill_combobox_four.activated[str].connect(self.update_available_support_skills)
        
        # Loop over the passive skills and add them to the combo box
        for s in self.get_available_support_skills(support_skills):
            print s
            self.support_skill_combobox_four.addItem(s)
        
        # Add the combo box widget to the grid
        grid.addWidget(self.support_skill_combobox_four, 6, 20)
        
        # Retrieve the skill that's displayed in the current dropdown and set it to False, so that
        # it is not shown in other dropdowns when it's already selected.
        selected_skill = str(self.support_skill_combobox_four.currentText())
        self.support_skill_dict[selected_skill] = False
        
        # Get the level label and level selection box
        level_lbl, self.support_level_box_four = self.add_gem_level_selection_widget()
        
        # ..and add them to the grid
        grid.addWidget(level_lbl, 6, 21)
        grid.addWidget(self.support_level_box_four, 6, 22)
        
        # Create the label
        support_skill_lbl_five = QtGui.QLabel("Support skill 5")
        
        # Add the widget to the next row, 3rd column
        grid.addWidget(support_skill_lbl_five, 7, 19)
        
        # Create a combobox widget
        self.support_skill_combobox_five = QtGui.QComboBox()
        self.support_skill_combobox_five.activated[str].connect(self.update_available_support_skills)
        
        # Loop over the passive skills and add them to the combo box
        for s in self.get_available_support_skills(support_skills):
            self.support_skill_combobox_five.addItem(s)
        
        # Add the combo box widget to the grid
        grid.addWidget(self.support_skill_combobox_five, 7, 20)
        
        # Retrieve the skill that's displayed in the current dropdown and set it to False, so that
        # it is not shown in other dropdowns when it's already selected.
        selected_skill = str(self.support_skill_combobox_five.currentText())
        self.support_skill_dict[selected_skill] = False
        
        # Get the level label and level selection box
        level_lbl, self.support_level_box_five = self.add_gem_level_selection_widget()
        
        # ..and add them to the grid
        grid.addWidget(level_lbl, 7, 21)
        grid.addWidget(self.support_level_box_five, 7, 22)
        
        # Update the available support skill gems for all the slots
        # TODO: Create something nicer than this, for example selecting the values for the support skill boxes beforehand and adding the items to each box afterwards
        self.set_available_support_skills()
            
    def add_gem_level_selection_widget(self):
        # Create the level label
        level_label = QtGui.QLabel('Lvl')
        
        # Make the text right-aligned
        level_label.setAlignment(QtCore.Qt.AlignRight)
        
        # Create the level selection dropdown
        level_widget = QtGui.QComboBox()
        
        # Add lvl 1 up to 20
        for i in range(1, 21, 1):
            level_widget.addItem(str(i))
            
        # Return the label and dropdown
        return level_label, level_widget
        
    def add_offensive_stats(self, grid):
        # Create a header for the offensive stats
        off_stats_lbl = QtGui.QLabel("Offensive stats")
        
        # Add the header to the grid
        grid.addWidget(off_stats_lbl, 0, 26, 1, 2)
        
        # Create a label and textbox for each offensive stat and add them to the grid
        # The textboxes should be set to read-only mode so that the user can't alter the value
        dps_lbl = QtGui.QLabel("DPS")
        self.dps_box = QtGui.QLineEdit()
        self.dps_box.setReadOnly(True)
        
        grid.addWidget(dps_lbl, 1, 26)
        grid.addWidget(self.dps_box, 1, 27)
        
        aps_lbl = QtGui.QLabel("APS")
        self.aps_box = QtGui.QLineEdit()
        self.aps_box.setReadOnly(True)
        
        grid.addWidget(aps_lbl, 1, 28)
        grid.addWidget(self.aps_box, 1, 29)
        
        dmg_per_hit_lbl = QtGui.QLabel("Damage per hit")
        self.dmg_per_hit_box = QtGui.QLineEdit()
        self.dmg_per_hit_box.setReadOnly(True)
        
        grid.addWidget(dmg_per_hit_lbl, 1, 30)
        grid.addWidget(self.dmg_per_hit_box, 1, 31)
        
        crit_chance_lbl = QtGui.QLabel("Crit chance")
        self.crit_chance_box = QtGui.QLineEdit()
        self.crit_chance_box.setReadOnly(True)
        
        grid.addWidget(crit_chance_lbl, 2, 26)
        grid.addWidget(self.crit_chance_box, 2, 27)
        
        crit_multi_lbl = QtGui.QLabel("Crit multiplier")
        self.crit_multi_box = QtGui.QLineEdit()
        self.crit_multi_box.setReadOnly(True)
        
        grid.addWidget(crit_multi_lbl, 2, 28)
        grid.addWidget(self.crit_multi_box, 2, 29)
        
        life_leech_lbl = QtGui.QLabel("Life leech")
        self.life_leech_box = QtGui.QLineEdit()
        self.life_leech_box.setReadOnly(True)
        
        grid.addWidget(life_leech_lbl, 3, 26)
        grid.addWidget(self.life_leech_box, 3, 27)
        
        mana_leech_lbl = QtGui.QLabel("Mana Leech")
        self.mana_leech_box = QtGui.QLineEdit()
        self.mana_leech_box.setReadOnly(True)
        
        grid.addWidget(mana_leech_lbl, 3, 28)
        grid.addWidget(self.mana_leech_box, 3, 29)
        
    def add_defensive_stats(self, grid):
        # Create header label and add it to the grid
        def_stats_lbl = QtGui.QLabel("Defensive stats")
        grid.addWidget(def_stats_lbl, 4, 26, 1, 2)
        
        # Create a label and textbox for each defensive stat. The textboxes should be put into read-only mode
        # so that the user can't alter the value of the box. Add all the widgets to the grid.
        life_lbl = QtGui.QLabel("Life")
        self.life_box = QtGui.QLineEdit()
        self.life_box.setReadOnly(True)
        
        grid.addWidget(life_lbl, 5, 26)
        grid.addWidget(self.life_box, 5, 27)
        
        es_lbl = QtGui.QLabel("Energy Shield")
        self.es_box = QtGui.QLineEdit()
        self.es_box.setReadOnly(True)
        
        grid.addWidget(es_lbl, 5, 28)
        grid.addWidget(self.es_box, 5, 29)
        
        mana_lbl = QtGui.QLabel("Mana")
        #mana_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.mana_box = QtGui.QLineEdit()
        self.mana_box.setReadOnly(True)
        
        grid.addWidget(mana_lbl, 5, 30)
        grid.addWidget(self.mana_box, 5, 31)
        
        life_regen_lbl = QtGui.QLabel("Life regen")
        self.life_regen_box = QtGui.QLineEdit()
        self.life_regen_box.setReadOnly(True)
        
        grid.addWidget(life_regen_lbl, 6, 26)
        grid.addWidget(self.life_regen_box, 6, 27)
        
        mana_regen_lbl = QtGui.QLabel("Mana regen")
        self.mana_regen_box = QtGui.QLineEdit()
        self.mana_regen_box.setReadOnly(True)
        
        grid.addWidget(mana_regen_lbl, 6, 28)
        grid.addWidget(self.mana_regen_box, 6, 29)
        
        block_chance_lbl = QtGui.QLabel("Chance to block")
        self.block_chance_box = QtGui.QLineEdit()
        self.block_chance_box.setReadOnly(True)
        
        grid.addWidget(block_chance_lbl, 6, 30)
        grid.addWidget(self.block_chance_box, 6, 31)
        
        fire_res_lbl = QtGui.QLabel("Fire resistance")
        self.fire_res_box = QtGui.QLineEdit()
        self.fire_res_box.setReadOnly(True)
        
        grid.addWidget(fire_res_lbl, 7, 26)
        grid.addWidget(self.fire_res_box, 7, 27)
        
        cold_res_lbl = QtGui.QLabel("Cold resistance")
        self.cold_res_box = QtGui.QLineEdit()
        self.cold_res_box.setReadOnly(True)
        
        grid.addWidget(cold_res_lbl, 7, 28)
        grid.addWidget(self.cold_res_box, 7, 29)
        
        lightning_res_lbl = QtGui.QLabel("Lightning resistance")
        self.lightning_res_box = QtGui.QLineEdit()
        self.lightning_res_box.setReadOnly(True)
        
        grid.addWidget(lightning_res_lbl, 7, 30)
        grid.addWidget(self.lightning_res_box, 7, 31)
        
        chaos_res_lbl = QtGui.QLabel("Chaos resistance")
        self.chaos_res_box = QtGui.QLineEdit()
        self.chaos_res_box.setReadOnly(True)
        
        grid.addWidget(chaos_res_lbl, 8, 26)
        grid.addWidget(self.chaos_res_box, 8, 27)
    
    def add_item_customization(self, grid):
        # Starts on row 10
        
        # Create item customization header
        items_lbl = QtGui.QLabel("Item customization")
        
        # Add the items label
        grid.addWidget(items_lbl, 11, 26)
        
        self.load_items_btn = QtGui.QPushButton("Load items")
        #self.load_items_btn.clicked.connect(self.load_items)
        
        # Add the load items button to the grid
        grid.addWidget(self.load_items_btn, 12, 26)
        
        # Add the helmet
        self.add_helmet_widgets(grid)
            
        # Add the amulet
        self.add_amulet_widgets(grid)
        
        # Add the main-hand
        self.add_main_hand_widgets(grid)
        
        # Add the off-hand
        self.add_off_hand_widgets(grid)
        
        # Add the chest
        self.add_chest_widgets(grid)
        
        # Add the gloves
        self.add_gloves_widgets(grid)
        
        # Add the rings
        self.add_ring_one_widgets(grid)
        self.add_ring_two_widgets(grid)
        
        # Add the belt
        self.add_belt_widgets(grid)
        
        # Add the boots
        self.add_boots_widgets(grid)
    
    def add_helmet_widgets(self, grid):
        # Create helmet widgets
        helm_lbl = QtGui.QLabel("Helmet")
        helm_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.helm_name_box = QtGui.QLineEdit()
        self.helm_name_box.setReadOnly(True)
        helm_unique_btn = QtGui.QPushButton("Select unique helmet")
        helm_customize_btn = QtGui.QPushButton("Create custom helmet")
        
        # Add the helmet widgets to the grid
        grid.addWidget(helm_lbl, 13, 26)
        grid.addWidget(self.helm_name_box, 13, 27, 1, 3)
        grid.addWidget(helm_unique_btn, 13, 30)
        grid.addWidget(helm_customize_btn, 13, 31)
     
    def add_amulet_widgets(self, grid):
        # Create amulet widgets
        amulet_lbl = QtGui.QLabel("Amulet")
        amulet_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.amulet_name_box = QtGui.QLineEdit()
        self.amulet_name_box.setReadOnly(True)
        amulet_unique_btn = QtGui.QPushButton("Select unique amulet")
        amulet_customize_btn = QtGui.QPushButton("Create custom amulet")
        
        # Add the amulet widgets to the grid
        grid.addWidget(amulet_lbl, 14, 26)
        grid.addWidget(self.amulet_name_box, 14, 27, 1, 3)
        grid.addWidget(amulet_unique_btn, 14, 30)
        grid.addWidget(amulet_customize_btn, 14, 31)
        
    def add_main_hand_widgets(self, grid):
        # Create main hand widgets
        mh_lbl = QtGui.QLabel("Main-hand")
        mh_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.mh_name_box = QtGui.QLineEdit()
        self.mh_name_box.setReadOnly(True)
        mh_unique_btn = QtGui.QPushButton("Select unique main-hand")
        mh_customize_btn = QtGui.QPushButton("Create custom main-hand")
        
        # Add the main hand widgets to the grid
        grid.addWidget(mh_lbl, 15, 26)
        grid.addWidget(self.mh_name_box, 15, 27, 1, 3)
        grid.addWidget(mh_unique_btn, 15, 30)
        grid.addWidget(mh_customize_btn, 15, 31)
    
    def add_off_hand_widgets(self, grid):
        # Create main hand widgets
        oh_lbl = QtGui.QLabel("Off-hand")
        oh_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.oh_name_box = QtGui.QLineEdit()
        self.oh_name_box.setReadOnly(True)
        oh_unique_btn = QtGui.QPushButton("Select unique off-hand")
        oh_customize_btn = QtGui.QPushButton("Create custom off-hand")
        
        # Add the main hand widgets to the grid
        grid.addWidget(oh_lbl, 16, 26)
        grid.addWidget(self.oh_name_box, 16, 27, 1, 3)
        grid.addWidget(oh_unique_btn, 16, 30)
        grid.addWidget(oh_customize_btn, 16, 31)
    
    def add_chest_widgets(self, grid):
        # Create helmet widgets
        chest_lbl = QtGui.QLabel("Chest")
        chest_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.chest_name_box = QtGui.QLineEdit()
        self.chest_name_box.setReadOnly(True)
        chest_unique_btn = QtGui.QPushButton("Select unique chest")
        chest_customize_btn = QtGui.QPushButton("Create custom chest")
        
        # Add the helmet widgets to the grid
        grid.addWidget(chest_lbl, 17, 26)
        grid.addWidget(self.chest_name_box, 17, 27, 1, 3)
        grid.addWidget(chest_unique_btn, 17, 30)
        grid.addWidget(chest_customize_btn, 17, 31)
    
    def add_gloves_widgets(self, grid):
        # Create helmet widgets
        gloves_lbl = QtGui.QLabel("Gloves")
        gloves_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.gloves_name_box = QtGui.QLineEdit()
        self.gloves_name_box.setReadOnly(True)
        gloves_unique_btn = QtGui.QPushButton("Select unique gloves")
        gloves_customize_btn = QtGui.QPushButton("Create custom gloves")
        
        # Add the helmet widgets to the grid
        grid.addWidget(gloves_lbl, 18, 26)
        grid.addWidget(self.gloves_name_box, 18, 27, 1, 3)
        grid.addWidget(gloves_unique_btn, 18, 30)
        grid.addWidget(gloves_customize_btn, 18, 31)
        
    def add_ring_one_widgets(self, grid):
        # Create helmet widgets
        ring_lbl = QtGui.QLabel("Ring 1")
        ring_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.ring_one_name_box = QtGui.QLineEdit()
        self.ring_one_name_box.setReadOnly(True)
        ring_unique_btn = QtGui.QPushButton("Select unique ring")
        ring_customize_btn = QtGui.QPushButton("Create custom ring")
        
        # Add the helmet widgets to the grid
        grid.addWidget(ring_lbl, 19, 26)
        grid.addWidget(self.ring_one_name_box, 19, 27, 1, 3)
        grid.addWidget(ring_unique_btn, 19, 30)
        grid.addWidget(ring_customize_btn, 19, 31)
    
    def add_ring_two_widgets(self, grid):
        # Create helmet widgets
        ring_lbl = QtGui.QLabel("Ring 2")
        ring_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.ring_two_name_box = QtGui.QLineEdit()
        self.ring_two_name_box.setReadOnly(True)
        ring_unique_btn = QtGui.QPushButton("Select unique ring")
        ring_customize_btn = QtGui.QPushButton("Create custom ring")
        
        # Add the helmet widgets to the grid
        grid.addWidget(ring_lbl, 20, 26)
        grid.addWidget(self.ring_two_name_box, 20, 27, 1, 3)
        grid.addWidget(ring_unique_btn, 20, 30)
        grid.addWidget(ring_customize_btn, 20, 31)
        
    def add_belt_widgets(self, grid):
        # Create helmet widgets
        belt_lbl = QtGui.QLabel("Belt")
        belt_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.belt_name_box = QtGui.QLineEdit()
        self.belt_name_box.setReadOnly(True)
        belt_unique_btn = QtGui.QPushButton("Select unique belt")
        belt_customize_btn = QtGui.QPushButton("Create custom belt")
        
        # Add the helmet widgets to the grid
        grid.addWidget(belt_lbl, 21, 26)
        grid.addWidget(self.belt_name_box, 21, 27, 1, 3)
        grid.addWidget(belt_unique_btn, 21, 30)
        grid.addWidget(belt_customize_btn, 21, 31)
        
    def add_boots_widgets(self, grid):
        # Create helmet widgets
        boots_lbl = QtGui.QLabel("Boots")
        boots_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.boots_name_box = QtGui.QLineEdit()
        self.boots_name_box.setReadOnly(True)
        boots_unique_btn = QtGui.QPushButton("Select unique boots")
        boots_customize_btn = QtGui.QPushButton("Create custom boots")
        
        # Add the helmet widgets to the grid
        grid.addWidget(boots_lbl, 22, 26)
        grid.addWidget(self.boots_name_box, 22, 27, 1, 3)
        grid.addWidget(boots_unique_btn, 22, 30)
        grid.addWidget(boots_customize_btn, 22, 31)

    def get_available_support_skills(self, support_skills):
        # Return a list of the support skill gems that are not selected in the dropdown menus
        return [skill for skill in self.support_skill_dict.keys() if self.support_skill_dict[skill]]
    
    def load_items(self):
        pass


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = PoEGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()