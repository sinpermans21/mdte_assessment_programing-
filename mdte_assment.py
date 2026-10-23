""" This program is for my ncea lv 3 programing assessment. it is a simple wackamole game.By: Samuel Rattray. When: 2026"""

#imports all the modules needed for the game to run 
import sys
import random
from PyQt6.QtCore import QUrl, QTimer
from pathlib import Path
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox, QVBoxLayout, QLabel, QDialog, QSpinBox

#Controls the number of rows and columns in the game grid 
number_of_rows_cols = 4

#this makes the window for the game  
class WackamoleWindow(QMainWindow):
    def __init__(self, duration):
        super().__init__()

        #Creates the audio and music player for the game sets the volume to %50 and plays the music in the background 
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.music_player = QMediaPlayer()
        self.music_player.setAudioOutput(self.audio_output)
        
        #gets the music file from sounds folder
        music_file = Path(__file__).resolve().parent / "sounds" / "monume-retro-arcade-game-music-577980.mp3    "
        self.music_player.setSource(QUrl.fromLocalFile(str(music_file)))
        self.music_player.play()

        #set the title siz and background color 
        self.setWindowTitle("Wack-a-Mole")
        self.resize(600, 600)
        self.setStyleSheet("background-color: #59d119;")
        self.layout = QVBoxLayout()
        self.counter = duration
        self.label = QLabel(f"Time left: {self.counter} seconds")
        self.layout.addWidget(self.label)

        #creates the buttons for the game and sets the point counter to 0 and game over to false
        self.buttons = []
        self.point = 0
        self.game_over = False

        # makes display for player points
        self.point_label = QLabel("Points: 0")
        self.point_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: thin;")
        self.layout.addWidget(self.point_label)

        #randomly puts mole on one of the buttons
        self.mole_row = random.randint(0, number_of_rows_cols - 1)
        self.mole_col = random.randint(0, number_of_rows_cols - 1)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        #creates the buttons and sets them in rows and columns 
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

        #creates a widget to keep grid layout
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        self.layout.addWidget(grid_widget)

        #creates a container for the main game 
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.buttons[self.mole_row][self.mole_col].setText("Mole")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    #updates the timer and ends the game when the time runs out
    def update_timer(self):
        self.counter -= 1
        self.label.setText(f"Time left: {self.counter} seconds")
        if self.counter == 0:
            self.end_game()

    #this function is called when a button is clicked it checks if the game is over and if not it checks if the clicked button is the mole it updates the score labeland moves the mole to a new position if the clicked button is not the mole it ends the game
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

    #this is the fuction that ends the game and disables all the buttons
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

        

#makes the start menu for the game that lets you set the time you want to play for 
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

#this runs the game and checks if the start menu was accepted
if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = StartMenu()
    #ends game
    if menu.exec() == QDialog.DialogCode.Accepted and menu.duration is not None:
        window = WackamoleWindow(menu.duration)
        window.show()
        sys.exit(app.exec())

    sys.exit(0)
