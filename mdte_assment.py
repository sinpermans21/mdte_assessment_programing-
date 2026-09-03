""" This program is for my ncea lv 3 programing assessment. it is a simple wackamole game.By: Samuel Rattray. When: 2026"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QFileDialog


class WackamoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wack-a-Mole")
        self.resize(300, 300)
        self.setStyleSheet("background-color: #777B7E;")

        self.buttons = []

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        for row in range(4):
            row_buttons = []
            for col in range(4):
                button = QPushButton("")
                button.setStyleSheet(
                    "QPushButton { background-color: #f0f0f0; font-size: 30px; font-weight: bold; }"
                )
                button.clicked.connect(lambda checked, r=row, c=col: self.button_clicked(r, c))
                grid_layout.addWidget(button, row, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
        

    def button_clicked(self, row, col):
        if self.board[row][col] != "":
            return

        self.board[row][col] = self.current_player
        self.buttons[row][col].setText(self.current_player)











app = QApplication(sys.argv)
window = WackamoleWindow()
window.show()
sys.exit(app.exec())

