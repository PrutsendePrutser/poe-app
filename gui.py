import sys
from PyQt4 import QtGui, QtCore

class PoEGUI(QtGui.QWidget):
    
    def __init__(self):
        super(PoEGUI, self).__init__()
        
        # Var to store all the support skills
        self.passive_skills = ['Multistrike', 'Faster Casting', 'Elemental Proliferation', 'Melee Physical Damage', 'Chain']
        
        # Var to store all the active skills
        self.active_skills = ["Arc", "Spectral Throw", "Flameblast"]
        
        self.initUI()
        
        
    def initUI(self):
        
        # Box to show stats from gear and passives
        statbox = QtGui.QTextEdit()
        statbox.setReadOnly(True)
        statbox.setText("sadasdasd\nasdsadsadsaads")
        
        # Create a grid layout
        grid = QtGui.QGridLayout()
        
        # Add some spacing
        grid.setSpacing(8)
        
        self.add_build_url_widgets(grid)
        
        # Add the passive data box below the build URL box and make it span 20 lines
        grid.addWidget(statbox, 2, 0, 18, 6)
        
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
        build_url_lbl = QtGui.QLabel("Build URL")
        
        # QLineEdit to enter build URL
        build_url_box = QtGui.QLineEdit()
        
        # Create the build URL load button
        build_url_load_btn = QtGui.QPushButton("Load build")
        
        # Add the label above the build url box
        grid.addWidget(build_url_lbl, 0, 0, 1, 6)
        grid.addWidget(build_url_box, 1, 0, 1, 18)
        # Add spacer label
        spacerlbl = QtGui.QLabel(" ")
        grid.addWidget(spacerlbl, 0, 25, 1, 20)
        grid.addWidget(build_url_load_btn, 1, 18)
        
        
    def create_active_skill_combo_box(self, grid):
        # Create label for active skill
        active_skill_lbl = QtGui.QLabel("Active skill")
        
        # Create a dropdown
        active_skill = QtGui.QComboBox()
        active_skills = ["Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw"]
        
        # Fill dropdown with active skills
        for skill in active_skills:
            active_skill.addItem(skill)
            
        # Add active skill label to grid
        grid.addWidget(active_skill_lbl, 2, 8)
        
        # Add active skill dropdown to grid
        grid.addWidget(active_skill, 2, 10)
        
        # Retrieve level label and level selection dropdown
        level_lbl, level_box = self.add_gem_level_selection_widget()
        
        # Add the level label and level selection dropdown to the grid
        grid.addWidget(level_lbl, 2, 14)
        grid.addWidget(level_box, 2, 16)
        
    def create_passive_skill_combo_boxes(self, grid):
        # Add 5 widgets, starting with support skill 1
        for i in range(1, 6, 1):
            # Create the label
            support_skill_lbl = QtGui.QLabel("Support skill %d" % i)
            
            # Add the widget to the next row, 3rd column
            grid.addWidget(support_skill_lbl, 2+i, 8)
            
            # Create a combobox widget
            support_skill_combobox = QtGui.QComboBox()
            
            # Loop over the passive skills and add them to the combo box
            for s in self.passive_skills:
                support_skill_combobox.addItem(s)
            # Add the combo box widget to the grid
            grid.addWidget(support_skill_combobox, 2+i, 10)
            
            # Get the level label and level selection box
            level_lbl, level_box = self.add_gem_level_selection_widget()
            
            # ..and add them to the grid
            grid.addWidget(level_lbl, 2+i, 14)
            grid.addWidget(level_box, 2+i, 16)
            
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
        dps_box = QtGui.QLineEdit()
        dps_box.setReadOnly(True)
        
        grid.addWidget(dps_lbl, 1, 26)
        grid.addWidget(dps_box, 1, 27)
        
        aps_lbl = QtGui.QLabel("APS")
        aps_box = QtGui.QLineEdit()
        aps_box.setReadOnly(True)
        
        grid.addWidget(aps_lbl, 1, 28)
        grid.addWidget(aps_box, 1, 29)
        
        dmg_per_hit_lbl = QtGui.QLabel("Damage per hit")
        dmg_per_hit_box = QtGui.QLineEdit()
        dmg_per_hit_box.setReadOnly(True)
        
        grid.addWidget(dmg_per_hit_lbl, 1, 30)
        grid.addWidget(dmg_per_hit_box, 1, 31)
        
        crit_chance_lbl = QtGui.QLabel("Crit chance")
        crit_chance_box = QtGui.QLineEdit()
        crit_chance_box.setReadOnly(True)
        
        grid.addWidget(crit_chance_lbl, 2, 26)
        grid.addWidget(crit_chance_box, 2, 27)
        
        crit_multi_lbl = QtGui.QLabel("Crit multiplier")
        crit_multi_box = QtGui.QLineEdit()
        crit_multi_box.setReadOnly(True)
        
        grid.addWidget(crit_multi_lbl, 2, 28)
        grid.addWidget(crit_multi_box, 2, 29)
        
        life_leech_lbl = QtGui.QLabel("Life leech")
        life_leech_box = QtGui.QLineEdit()
        life_leech_box.setReadOnly(True)
        
        grid.addWidget(life_leech_lbl, 3, 26)
        grid.addWidget(life_leech_box, 3, 27)
        
        mana_leech_lbl = QtGui.QLabel("Mana Leech")
        mana_leech_box = QtGui.QLineEdit()
        mana_leech_box.setReadOnly(True)
        
        grid.addWidget(mana_leech_lbl, 3, 28)
        grid.addWidget(mana_leech_box, 3, 29)
        
    def add_defensive_stats(self, grid):
        # Create header label and add it to the grid
        def_stats_lbl = QtGui.QLabel("Defensive stats")
        grid.addWidget(def_stats_lbl, 4, 26, 1, 2)
        
        # Create a label and textbox for each defensive stat. The textboxes should be put into read-only mode
        # so that the user can't alter the value of the box. Add all the widgets to the grid.
        life_lbl = QtGui.QLabel("Life")
        life_box = QtGui.QLineEdit()
        life_box.setReadOnly(True)
        
        grid.addWidget(life_lbl, 5, 26)
        grid.addWidget(life_box, 5, 27)
        
        es_lbl = QtGui.QLabel("Energy Shield")
        es_box = QtGui.QLineEdit()
        es_box.setReadOnly(True)
        
        grid.addWidget(es_lbl, 5, 28)
        grid.addWidget(es_box, 5, 29)
        
        mana_lbl = QtGui.QLabel("Mana")
        mana_lbl.setAlignment(QtCore.Qt.AlignRight)
        mana_box = QtGui.QLineEdit()
        mana_box.setReadOnly(True)
        
        grid.addWidget(mana_lbl, 5, 30)
        grid.addWidget(mana_box, 5, 31)
        
        life_regen_lbl = QtGui.QLabel("Life regen")
        life_regen_box = QtGui.QLineEdit()
        life_regen_box.setReadOnly(True)
        
        grid.addWidget(life_regen_lbl, 6, 26)
        grid.addWidget(life_regen_box, 6, 27)
        
        mana_regen_lbl = QtGui.QLabel("Mana regen")
        mana_regen_box = QtGui.QLineEdit()
        mana_regen_box.setReadOnly(True)
        
        grid.addWidget(mana_regen_lbl, 6, 28)
        grid.addWidget(mana_regen_box, 6, 29)
        
        block_chance_lbl = QtGui.QLabel("Chance to block")
        block_chance_box = QtGui.QLineEdit()
        block_chance_box.setReadOnly(True)
        
        grid.addWidget(block_chance_lbl, 6, 30)
        grid.addWidget(block_chance_box, 6, 31)
        
        fire_res_lbl = QtGui.QLabel("Fire resistance")
        fire_res_box = QtGui.QLineEdit()
        fire_res_box.setReadOnly(True)
        
        grid.addWidget(fire_res_lbl, 7, 26)
        grid.addWidget(fire_res_box, 7, 27)
        
        cold_res_lbl = QtGui.QLabel("Cold resistance")
        cold_res_box = QtGui.QLineEdit()
        cold_res_box.setReadOnly(True)
        
        grid.addWidget(cold_res_lbl, 7, 28)
        grid.addWidget(cold_res_box, 7, 29)
        
        lightning_res_lbl = QtGui.QLabel("Lightning resistance")
        lightning_res_box = QtGui.QLineEdit()
        lightning_res_box.setReadOnly(True)
        
        grid.addWidget(lightning_res_lbl, 7, 30)
        grid.addWidget(lightning_res_box, 7, 31)
        
        chaos_res_lbl = QtGui.QLabel("Chaos resistance")
        chaos_res_box = QtGui.QLineEdit()
        chaos_res_box.setReadOnly(True)
        
        grid.addWidget(chaos_res_lbl, 8, 26)
        grid.addWidget(chaos_res_box, 8, 27)
    
    def add_item_customization(self, grid):
        # Starts on row 10
        
        # Create item customization header
        items_lbl = QtGui.QLabel("Item customization")
        
        # Add the items label
        grid.addWidget(items_lbl, 11, 26)
        
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
        helm_name_box = QtGui.QLineEdit()
        helm_name_box.setReadOnly(True)
        helm_unique_btn = QtGui.QPushButton("Select unique helmet")
        helm_customize_btn = QtGui.QPushButton("Create custom helmet")
        
        # Add the helmet widgets to the grid
        grid.addWidget(helm_lbl, 12, 26)
        grid.addWidget(helm_name_box, 12, 27, 1, 3)
        grid.addWidget(helm_unique_btn, 12, 30)
        grid.addWidget(helm_customize_btn, 12, 31)
     
    def add_amulet_widgets(self, grid):
        # Create amulet widgets
        amulet_lbl = QtGui.QLabel("Amulet")
        amulet_lbl.setAlignment(QtCore.Qt.AlignRight)
        amulet_name_box = QtGui.QLineEdit()
        amulet_name_box.setReadOnly(True)
        amulet_unique_btn = QtGui.QPushButton("Select unique amulet")
        amulet_customize_btn = QtGui.QPushButton("Create custom amulet")
        
        # Add the amulet widgets to the grid
        grid.addWidget(amulet_lbl, 13, 26)
        grid.addWidget(amulet_name_box, 13, 27, 1, 3)
        grid.addWidget(amulet_unique_btn, 13, 30)
        grid.addWidget(amulet_customize_btn, 13, 31)
        
    def add_main_hand_widgets(self, grid):
        # Create main hand widgets
        mh_lbl = QtGui.QLabel("Main-hand")
        mh_lbl.setAlignment(QtCore.Qt.AlignRight)
        mh_name_box = QtGui.QLineEdit()
        mh_name_box.setReadOnly(True)
        mh_unique_btn = QtGui.QPushButton("Select unique main-hand")
        mh_customize_btn = QtGui.QPushButton("Create custom main-hand")
        
        # Add the main hand widgets to the grid
        grid.addWidget(mh_lbl, 14, 26)
        grid.addWidget(mh_name_box, 14, 27, 1, 3)
        grid.addWidget(mh_unique_btn, 14, 30)
        grid.addWidget(mh_customize_btn, 14, 31)
    
    def add_off_hand_widgets(self, grid):
        # Create main hand widgets
        oh_lbl = QtGui.QLabel("Off-hand")
        oh_lbl.setAlignment(QtCore.Qt.AlignRight)
        oh_name_box = QtGui.QLineEdit()
        oh_name_box.setReadOnly(True)
        oh_unique_btn = QtGui.QPushButton("Select unique off-hand")
        oh_customize_btn = QtGui.QPushButton("Create custom off-hand")
        
        # Add the main hand widgets to the grid
        grid.addWidget(oh_lbl, 15, 26)
        grid.addWidget(oh_name_box, 15, 27, 1, 3)
        grid.addWidget(oh_unique_btn, 15, 30)
        grid.addWidget(oh_customize_btn, 15, 31)
    
    def add_chest_widgets(self, grid):
        # Create helmet widgets
        chest_lbl = QtGui.QLabel("Chest")
        chest_lbl.setAlignment(QtCore.Qt.AlignRight)
        chest_name_box = QtGui.QLineEdit()
        chest_name_box.setReadOnly(True)
        chest_unique_btn = QtGui.QPushButton("Select unique chest")
        chest_customize_btn = QtGui.QPushButton("Create custom chest")
        
        # Add the helmet widgets to the grid
        grid.addWidget(chest_lbl, 16, 26)
        grid.addWidget(chest_name_box, 16, 27, 1, 3)
        grid.addWidget(chest_unique_btn, 16, 30)
        grid.addWidget(chest_customize_btn, 16, 31)
    
    def add_gloves_widgets(self, grid):
        # Create helmet widgets
        gloves_lbl = QtGui.QLabel("Gloves")
        gloves_lbl.setAlignment(QtCore.Qt.AlignRight)
        gloves_name_box = QtGui.QLineEdit()
        gloves_name_box.setReadOnly(True)
        gloves_unique_btn = QtGui.QPushButton("Select unique gloves")
        gloves_customize_btn = QtGui.QPushButton("Create custom gloves")
        
        # Add the helmet widgets to the grid
        grid.addWidget(gloves_lbl, 17, 26)
        grid.addWidget(gloves_name_box, 17, 27, 1, 3)
        grid.addWidget(gloves_unique_btn, 17, 30)
        grid.addWidget(gloves_customize_btn, 17, 31)
        
    def add_ring_one_widgets(self, grid):
        # Create helmet widgets
        ring_lbl = QtGui.QLabel("Ring 1")
        ring_lbl.setAlignment(QtCore.Qt.AlignRight)
        ring_name_box = QtGui.QLineEdit()
        ring_name_box.setReadOnly(True)
        ring_unique_btn = QtGui.QPushButton("Select unique ring")
        ring_customize_btn = QtGui.QPushButton("Create custom ring")
        
        # Add the helmet widgets to the grid
        grid.addWidget(ring_lbl, 18, 26)
        grid.addWidget(ring_name_box, 18, 27, 1, 3)
        grid.addWidget(ring_unique_btn, 18, 30)
        grid.addWidget(ring_customize_btn, 18, 31)
    
    def add_ring_two_widgets(self, grid):
        # Create helmet widgets
        ring_lbl = QtGui.QLabel("Ring 2")
        ring_lbl.setAlignment(QtCore.Qt.AlignRight)
        ring_name_box = QtGui.QLineEdit()
        ring_name_box.setReadOnly(True)
        ring_unique_btn = QtGui.QPushButton("Select unique ring")
        ring_customize_btn = QtGui.QPushButton("Create custom ring")
        
        # Add the helmet widgets to the grid
        grid.addWidget(ring_lbl, 19, 26)
        grid.addWidget(ring_name_box, 19, 27, 1, 3)
        grid.addWidget(ring_unique_btn, 19, 30)
        grid.addWidget(ring_customize_btn, 19, 31)
        
    def add_belt_widgets(self, grid):
        # Create helmet widgets
        belt_lbl = QtGui.QLabel("Belt")
        belt_lbl.setAlignment(QtCore.Qt.AlignRight)
        belt_name_box = QtGui.QLineEdit()
        belt_name_box.setReadOnly(True)
        belt_unique_btn = QtGui.QPushButton("Select unique belt")
        belt_customize_btn = QtGui.QPushButton("Create custom belt")
        
        # Add the helmet widgets to the grid
        grid.addWidget(belt_lbl, 20, 26)
        grid.addWidget(belt_name_box, 20, 27, 1, 3)
        grid.addWidget(belt_unique_btn, 20, 30)
        grid.addWidget(belt_customize_btn, 20, 31)
        
    def add_boots_widgets(self, grid):
        # Create helmet widgets
        boots_lbl = QtGui.QLabel("Boots")
        boots_lbl.setAlignment(QtCore.Qt.AlignRight)
        boots_name_box = QtGui.QLineEdit()
        boots_name_box.setReadOnly(True)
        boots_unique_btn = QtGui.QPushButton("Select unique boots")
        boots_customize_btn = QtGui.QPushButton("Create custom boots")
        
        # Add the helmet widgets to the grid
        grid.addWidget(boots_lbl, 21, 26)
        grid.addWidget(boots_name_box, 21, 27, 1, 3)
        grid.addWidget(boots_unique_btn, 21, 30)
        grid.addWidget(boots_customize_btn, 21, 31)
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = PoEGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()