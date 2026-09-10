""" This program is for my ncea lv 3 programing assessment. it is a simple wackamole game.By: Samuel Rattray. When: 2026"""

import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QFileDialog, QLabel

number_of_rows_cols = 5


class WackamoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wack-a-Mole")
        self.resize(600, 600)
        self.setStyleSheet("background-color: #59d119;")

        self.buttons = []
        self.point = 0

        self.point_label = QLabel("Points: 0")
        self.point_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: thin;")
 
        #randomly select a mole position
        self.mole_row = random.randint(0, {number_of_rows_cols-1})
        self.mole_col = random.randint(0, {number_of_rows_cols-1})

        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.addWidget(self.point_label,0,3)

        for row in range(number_of_rows_cols):
            row_buttons = []
            for col in range(number_of_rows_cols):
                button = QPushButton("")
                button.setFixedSize(60,60)
                button.setStyleSheet(
                    "QPushButton { background-color: #591d1d; color: #ffffff; font-size: 20px; font-weight: bold; border-radius: 30px; border-style: solid; border-width: 2px }"    
                )
                button.clicked.connect(lambda checked, r=row, c=col: self.button_clicked(r, c))
                grid_layout.addWidget(button, row, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

        
        #shows the mole 
        self.buttons[self.mole_row][self.mole_col].setText("Mole ")
        

    def button_clicked(self, row, col):
        
        if row == self.mole_row and col == self.mole_col:

            #add point or smt
            self.point +=1

            #updates points 
            self.point_label.setText(f"Points: {self.point}")

            self.buttons[self.mole_row][self.mole_col].setText("")

            new_row = random.randint(0, {number_of_rows_cols-1})
            new_col = random.randint(0, {number_of_rows_cols-1})

            self.mole_row = new_row
            self.mole_col = new_col

            self.buttons[self.mole_row][self.mole_col].setText("Mole")


app = QApplication(sys.argv)
window = WackamoleWindow()
window.show()
sys.exit(app.exec)

