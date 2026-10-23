""" This program is for my ncea lv 3 programing assessment. it is a simple wackamole game.By: Samuel Rattray. When: 2026"""

import sys
import random
from PyQt6.QtCore import QUrl, QTimer
from pathlib import Path
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QVBoxLayout, QLabel, QDialog, QSpinBox

number_of_rows_cols = 4

#this makes the window for the game  
class WackamoleWindow(QMainWindow):
    def __init__(self, duration):
        super().__init__()

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.music_player = QMediaPlayer()
        self.music_player.setAudioOutput(self.audio_output)
        music_file = Path(__file__).resolve().parent / "sounds" / "monume-retro-arcade-game-music-577980.mp3    "
        self.music_player.setSource(QUrl.fromLocalFile(str(music_file)))
        self.music_player.play()

        self.setWindowTitle("Wack-a-Mole")
        self.resize(600, 600)
        self.setStyleSheet("background-color: #59d119;")
        self.layout = QVBoxLayout()
        self.counter = duration
        self.label = QLabel(f"Time left: {self.counter} seconds")
        self.layout.addWidget(self.label)

        self.buttons = []
        self.point = 0
        self.game_over = False

        self.point_label = QLabel("Points: 0")
        self.point_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: thin;")
        self.layout.addWidget(self.point_label)

        self.mole_row = random.randint(0, number_of_rows_cols - 1)
        self.mole_col = random.randint(0, number_of_rows_cols - 1)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

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

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        self.layout.addWidget(grid_widget)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.buttons[self.mole_row][self.mole_col].setText("Mole")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.counter -= 1
        self.label.setText(f"Time left: {self.counter} seconds")
        if self.counter == 0:
            self.end_game()

    def button_clicked(self, row, col):
        if self.game_over:
            return 
        
        if row == self.mole_row and col == self.mole_col:

            #add point or smt
            self.point += 1

            #updates points 
            self.point_label.setText(f"Points: {self.point}")

            self.buttons[self.mole_row][self.mole_col].setText("")

            new_row = random.randint(0, number_of_rows_cols-1)
            new_col = random.randint(0, number_of_rows_cols-1)

            self.mole_row = new_row
            self.mole_col = new_col

            self.buttons[self.mole_row][self.mole_col].setText("Mole")

        else: 
            self.end_game()

    def end_game(self):
        if self.game_over:
            return

        self.game_over = True
        self.timer.stop()

        for row_buttons in self.buttons:
            for button in row_buttons:
                button.setEnabled(False)

        score_file = Path(__file__).resolve().parent / "score.txt"
        try:
            with score_file.open("a", encoding="utf-8") as file:
                file.write(f"Score: {self.point}\n")
        except OSError as error:
            QMessageBox.warning(
                self,
                "Could not save score",
                f"Your score could not be saved to {score_file}.\n{error}",
            )

        QMessageBox.information(self, "Game Over", f"You missed the mole LOSER! \nYour final score is: {self.point}")
        self.close()

        


class StartMenu(QDialog):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Wack-a-Mole")
        self.duration = None

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter game length in seconds:"))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(15, 60)
        self.duration_input.setValue(30)
        layout.addWidget(self.duration_input)

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.choose_duration)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def choose_duration(self):
        self.duration = self.duration_input.value()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = StartMenu()

    if menu.exec() == QDialog.DialogCode.Accepted and menu.duration is not None:
        window = WackamoleWindow(menu.duration)
        window.show()
        sys.exit(app.exec())

    sys.exit(0)
