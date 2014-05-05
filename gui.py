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
        grid.setSpacing(10)
        
        self.add_build_url_widgets(grid)
        
        # Add the passive data box below the build URL box and make it span 20 lines
        grid.addWidget(statbox, 2, 0, 18, 4)
        
        # Add active skill gem widget
        self.create_active_skill_combo_box(grid)
        
        # Add support skill gem widgets
        self.create_passive_skill_combo_boxes(grid)
        
        # Set the layout
        self.setLayout(grid)
        
        # Set the size of the app
        self.setGeometry(100, 100, 800, 600)
        
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
        grid.addWidget(build_url_lbl, 0, 0, 1, 2)
        grid.addWidget(build_url_box, 1, 0, 1, 10)
        grid.addWidget(build_url_load_btn, 1, 10)
        
        
    def create_active_skill_combo_box(self, grid):
        active_skill_lbl = QtGui.QLabel("Active skill")
        active_skill = QtGui.QComboBox()
        active_skills = ["Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw", "Arc", "Double Strike", "Lightning Arrow", "Spectral Throw"]
        for skill in active_skills:
            active_skill.addItem(skill)
        grid.addWidget(active_skill_lbl, 2, 4)
        grid.addWidget(active_skill, 2, 6)
        level_lbl, level_box = self.add_gem_level_selection_widget()
        grid.addWidget(level_lbl, 2, 7)
        grid.addWidget(level_box, 2, 8)
        
    def create_passive_skill_combo_boxes(self, grid):
        # Add 5 widgets, starting with support skill 1
        for i in range(1, 6, 1):
            # Create the label
            support_skill_lbl = QtGui.QLabel("Support skill %d" % i)
            
            # Add the widget to the next row, 3rd column
            grid.addWidget(support_skill_lbl, 2+i, 4, 1, 2)
            
            # Create a combobox widget
            support_skill_combobox = QtGui.QComboBox()
            
            # Loop over the passive skills and add them to the combo box
            for s in self.passive_skills:
                support_skill_combobox.addItem(s)
            # Add the combo box widget to the grid
            grid.addWidget(support_skill_combobox, 2+i, 6)
            level_lbl, level_box = self.add_gem_level_selection_widget()
            grid.addWidget(level_lbl, 2+i, 7)
            grid.addWidget(level_box, 2+i, 8)
            
    def add_gem_level_selection_widget(self):
        level_label = QtGui.QLabel('Lvl')
        level_label.setAlignment(QtCore.Qt.AlignRight)
        level_widget = QtGui.QComboBox()
        for i in range(1, 21, 1):
            level_widget.addItem(str(i))
        return level_label, level_widget
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = PoEGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    