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
        grid.addWidget(active_skill, 2, 12)
        
        # Retrieve level label and level selection dropdown
        level_lbl, level_box = self.add_gem_level_selection_widget()
        
        # Add the level label and level selection dropdown to the grid
        grid.addWidget(level_lbl, 2, 16)
        grid.addWidget(level_box, 2, 18)
        
    def create_passive_skill_combo_boxes(self, grid):
        # Add 5 widgets, starting with support skill 1
        for i in range(1, 6, 1):
            # Create the label
            support_skill_lbl = QtGui.QLabel("Support skill %d" % i)
            
            # Add the widget to the next row, 3rd column
            grid.addWidget(support_skill_lbl, 2+i, 8, 1, 4)
            
            # Create a combobox widget
            support_skill_combobox = QtGui.QComboBox()
            
            # Loop over the passive skills and add them to the combo box
            for s in self.passive_skills:
                support_skill_combobox.addItem(s)
            # Add the combo box widget to the grid
            grid.addWidget(support_skill_combobox, 2+i, 12)
            
            # Get the level label and level selection box
            level_lbl, level_box = self.add_gem_level_selection_widget()
            
            # ..and add them to the grid
            grid.addWidget(level_lbl, 2+i, 16)
            grid.addWidget(level_box, 2+i, 18)
            
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
        grid.addWidget(def_stats_lbl, 5, 26, 1, 2)
        
        # Create a label and textbox for each defensive stat. The textboxes should be put into read-only mode
        # so that the user can't alter the value of the box. Add all the widgets to the grid.
        life_lbl = QtGui.QLabel("Life")
        life_box = QtGui.QLineEdit()
        life_box.setReadOnly(True)
        
        grid.addWidget(life_lbl, 6, 26)
        grid.addWidget(life_box, 6, 27)
        
        es_lbl = QtGui.QLabel("Energy Shield")
        es_box = QtGui.QLineEdit()
        es_box.setReadOnly(True)
        
        grid.addWidget(es_lbl, 6, 28)
        grid.addWidget(es_box, 6, 29)
        
        mana_lbl = QtGui.QLabel("Mana")
        mana_lbl.setAlignment(QtCore.Qt.AlignRight)
        mana_box = QtGui.QLineEdit()
        mana_box.setReadOnly(True)
        
        grid.addWidget(mana_lbl, 6, 30)
        grid.addWidget(mana_box, 6, 31)
        
        life_regen_lbl = QtGui.QLabel("Life regen")
        life_regen_box = QtGui.QLineEdit()
        life_regen_box.setReadOnly(True)
        
        grid.addWidget(life_regen_lbl, 7, 26)
        grid.addWidget(life_regen_box, 7, 27)
        
        mana_regen_lbl = QtGui.QLabel("Mana regen")
        mana_regen_box = QtGui.QLineEdit()
        mana_regen_box.setReadOnly(True)
        
        grid.addWidget(mana_regen_lbl, 7, 28)
        grid.addWidget(mana_regen_box, 7, 29)
        
        block_chance_lbl = QtGui.QLabel("Chance to block")
        block_chance_box = QtGui.QLineEdit()
        block_chance_box.setReadOnly(True)
        
        grid.addWidget(block_chance_lbl, 7, 30)
        grid.addWidget(block_chance_box, 7, 31)
        
        fire_res_lbl = QtGui.QLabel("Fire resistance")
        fire_res_box = QtGui.QLineEdit()
        fire_res_box.setReadOnly(True)
        
        grid.addWidget(fire_res_lbl, 8, 26)
        grid.addWidget(fire_res_box, 8, 27)
        
        cold_res_lbl = QtGui.QLabel("Cold resistance")
        cold_res_box = QtGui.QLineEdit()
        cold_res_box.setReadOnly(True)
        
        grid.addWidget(cold_res_lbl, 8, 28)
        grid.addWidget(cold_res_box, 8, 29)
        
        lightning_res_lbl = QtGui.QLabel("Lightning resistance")
        lightning_res_box = QtGui.QLineEdit()
        lightning_res_box.setReadOnly(True)
        
        grid.addWidget(lightning_res_lbl, 8, 30)
        grid.addWidget(lightning_res_box, 8, 31)
        
        chaos_res_lbl = QtGui.QLabel("Chaos resistance")
        chaos_res_box = QtGui.QLineEdit()
        chaos_res_box.setReadOnly(True)
        
        grid.addWidget(chaos_res_lbl, 9, 26)
        grid.addWidget(chaos_res_box, 9, 27)
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = PoEGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()