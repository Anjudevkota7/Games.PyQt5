import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGridLayout, 
                             QLineEdit, QMessageBox, QStackedWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class GameCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Center")
        self.setGeometry(100, 100, 800, 600)
        
        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create main menu
        self.create_main_menu()
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)

    def create_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🎮 Game Center")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; margin: 30px;")
        layout.addWidget(title)
        
        # Game buttons
        games = [
            ("🎯 Tic Tac Toe", self.start_tic_tac_toe),
            ("🎪 Hangman", self.start_hangman),
            ("✂️ Rock Paper Scissors", self.start_rps),
            ("🔢 Number Guessing", self.start_number_guess)
        ]
        
        for game_name, game_func in games:
            btn = QPushButton(game_name)
            btn.setFont(QFont("Arial", 16))
            btn.setMinimumHeight(60)
            btn.clicked.connect(game_func)
            layout.addWidget(btn)
        
        layout.addStretch()
        main_menu.setLayout(layout)
        self.stacked_widget.addWidget(main_menu)

    def start_tic_tac_toe(self):
        self.tic_tac_toe = TicTacToe(self)
        self.stacked_widget.addWidget(self.tic_tac_toe)
        self.stacked_widget.setCurrentWidget(self.tic_tac_toe)

    def start_hangman(self):
        self.hangman = Hangman(self)
        self.stacked_widget.addWidget(self.hangman)
        self.stacked_widget.setCurrentWidget(self.hangman)

    def start_rps(self):
        self.rps = RockPaperScissors(self)
        self.stacked_widget.addWidget(self.rps)
        self.stacked_widget.setCurrentWidget(self.rps)

    def start_number_guess(self):
        self.number_guess = NumberGuessing(self)
        self.stacked_widget.addWidget(self.number_guess)
        self.stacked_widget.setCurrentWidget(self.number_guess)

    def return_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)

class GameBase(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
    def create_back_button(self):
        back_btn = QPushButton("← Back to Menu")
        back_btn.setMaximumWidth(150)
        back_btn.clicked.connect(self.parent.return_to_menu)
        return back_btn

class TicTacToe(GameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title and back button
        header = QHBoxLayout()
        header.addWidget(self.create_back_button())
        header.addStretch()
        title = QLabel("Tic Tac Toe")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Current player display
        self.status_label = QLabel(f"Current Player: {self.current_player}")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.status_label)
        
        # Game board
        grid = QGridLayout()
        for i in range(9):
            btn = QPushButton("")
            btn.setMinimumSize(100, 100)
            btn.setFont(QFont("Arial", 24, QFont.Bold))
            btn.clicked.connect(lambda checked, pos=i: self.make_move(pos))
            self.buttons.append(btn)
            grid.addWidget(btn, i // 3, i % 3)
        
        board_widget = QWidget()
        board_widget.setLayout(grid)
        board_widget.setMaximumSize(320, 320)
        
        board_container = QHBoxLayout()
        board_container.addStretch()
        board_container.addWidget(board_widget)
        board_container.addStretch()
        layout.addLayout(board_container)
        
        # Reset button
        reset_btn = QPushButton("New Game")
        reset_btn.clicked.connect(self.reset_game)
        layout.addWidget(reset_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def make_move(self, position):
        if self.board[position] == "":
            self.board[position] = self.current_player
            self.buttons[position].setText(self.current_player)
            
            if self.check_winner():
                QMessageBox.information(self, "Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif "" not in self.board:
                QMessageBox.information(self, "Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.setText(f"Current Player: {self.current_player}")

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] 
                and self.board[combo[0]] != ""):
                return True
        return False

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        for btn in self.buttons:
            btn.setText("")
        self.status_label.setText(f"Current Player: {self.current_player}")

class Hangman(GameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.words = ["PYTHON", "PROGRAMMING", "COMPUTER", "ALGORITHM", "SOFTWARE", 
                     "DEVELOPMENT", "FUNCTION", "VARIABLE", "LOOP", "CONDITION"]
        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title and back button
        header = QHBoxLayout()
        header.addWidget(self.create_back_button())
        header.addStretch()
        title = QLabel("Hangman")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Word display
        self.word_label = QLabel("")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFont(QFont("Courier", 20, QFont.Bold))
        layout.addWidget(self.word_label)
        
        # Hangman drawing
        self.hangman_label = QLabel("")
        self.hangman_label.setAlignment(Qt.AlignCenter)
        self.hangman_label.setFont(QFont("Courier", 12))
        layout.addWidget(self.hangman_label)
        
        # Guess input
        guess_layout = QHBoxLayout()
        guess_layout.addWidget(QLabel("Enter a letter:"))
        self.guess_input = QLineEdit()
        self.guess_input.setMaxLength(1)
        self.guess_input.returnPressed.connect(self.make_guess)
        guess_layout.addWidget(self.guess_input)
        
        guess_btn = QPushButton("Guess")
        guess_btn.clicked.connect(self.make_guess)
        guess_layout.addWidget(guess_btn)
        layout.addLayout(guess_layout)
        
        # Wrong letters
        self.wrong_letters_label = QLabel("Wrong letters: ")
        layout.addWidget(self.wrong_letters_label)
        
        # New game button
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self.new_game)
        layout.addWidget(new_game_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def new_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_letters = set()
        self.wrong_count = 0
        self.update_display()

    def make_guess(self):
        letter = self.guess_input.text().upper()
        self.guess_input.clear()
        
        if not letter or len(letter) != 1 or not letter.isalpha():
            QMessageBox.warning(self, "Invalid Input", "Please enter a single letter.")
            return
            
        if letter in self.guessed_letters:
            QMessageBox.warning(self, "Already Guessed", "You already guessed that letter!")
            return
            
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            if set(self.word) <= self.guessed_letters:
                QMessageBox.information(self, "Congratulations!", f"You won! The word was {self.word}")
                self.new_game()
        else:
            self.wrong_letters.add(letter)
            self.wrong_count += 1
            if self.wrong_count >= 6:
                QMessageBox.information(self, "Game Over", f"You lost! The word was {self.word}")
                self.new_game()
        
        self.update_display()

    def update_display(self):
        # Update word display
        display_word = " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)
        self.word_label.setText(display_word)
        
        # Update hangman drawing
        hangman_stages = [
            "",
            "  +---+\n      |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
        ]
        self.hangman_label.setText(hangman_stages[min(self.wrong_count, len(hangman_stages) - 1)])
        
        # Update wrong letters
        self.wrong_letters_label.setText(f"Wrong letters: {', '.join(sorted(self.wrong_letters))}")

class RockPaperScissors(GameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.player_score = 0
        self.computer_score = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title and back button
        header = QHBoxLayout()
        header.addWidget(self.create_back_button())
        header.addStretch()
        title = QLabel("Rock Paper Scissors")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Score
        self.score_label = QLabel(f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.score_label)
        
        # Choices
        choices_layout = QHBoxLayout()
        for choice in ["Rock 🗿", "Paper 📄", "Scissors ✂️"]:
            btn = QPushButton(choice)
            btn.setMinimumHeight(80)
            btn.setFont(QFont("Arial", 14))
            btn.clicked.connect(lambda checked, c=choice.split()[0]: self.play(c))
            choices_layout.addWidget(btn)
        layout.addLayout(choices_layout)
        
        # Result display
        self.result_label = QLabel("Choose your move!")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setMinimumHeight(100)
        layout.addWidget(self.result_label)
        
        # Reset score button
        reset_btn = QPushButton("Reset Score")
        reset_btn.clicked.connect(self.reset_score)
        layout.addWidget(reset_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def play(self, player_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)
        
        result = self.determine_winner(player_choice, computer_choice)
        
        if result == "win":
            self.player_score += 1
            result_text = f"You chose {player_choice}\nComputer chose {computer_choice}\nYou Win! 🎉"
        elif result == "lose":
            self.computer_score += 1
            result_text = f"You chose {player_choice}\nComputer chose {computer_choice}\nYou Lose! 😔"
        else:
            result_text = f"You chose {player_choice}\nComputer chose {computer_choice}\nIt's a Tie! 🤝"
        
        self.result_label.setText(result_text)
        self.score_label.setText(f"Player: {self.player_score} | Computer: {self.computer_score}")

    def determine_winner(self, player, computer):
        if player == computer:
            return "tie"
        elif ((player == "Rock" and computer == "Scissors") or
              (player == "Paper" and computer == "Rock") or
              (player == "Scissors" and computer == "Paper")):
            return "win"
        else:
            return "lose"

    def reset_score(self):
        self.player_score = 0
        self.computer_score = 0
        self.score_label.setText(f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.result_label.setText("Choose your move!")

class NumberGuessing(GameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title and back button
        header = QHBoxLayout()
        header.addWidget(self.create_back_button())
        header.addStretch()
        title = QLabel("Number Guessing Game")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Instructions
        instructions = QLabel("I'm thinking of a number between 1 and 100!")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setFont(QFont("Arial", 14))
        layout.addWidget(instructions)
        
        # Guess input
        guess_layout = QHBoxLayout()
        guess_layout.addWidget(QLabel("Your guess:"))
        self.guess_input = QLineEdit()
        self.guess_input.returnPressed.connect(self.make_guess)
        guess_layout.addWidget(self.guess_input)
        
        guess_btn = QPushButton("Guess")
        guess_btn.clicked.connect(self.make_guess)
        guess_layout.addWidget(guess_btn)
        layout.addLayout(guess_layout)
        
        # Attempts counter
        self.attempts_label = QLabel(f"Attempts: {0}")
        self.attempts_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.attempts_label)
        
        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setMinimumHeight(60)
        layout.addWidget(self.result_label)
        
        # New game button
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self.new_game)
        layout.addWidget(new_game_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def new_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.setText(f"Attempts: {self.attempts}")
        self.result_label.setText("")
        self.guess_input.clear()

    def make_guess(self):
        try:
            guess = int(self.guess_input.text())
            if guess < 1 or guess > 100:
                QMessageBox.warning(self, "Invalid Input", "Please enter a number between 1 and 100.")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            return
        
        self.attempts += 1
        self.attempts_label.setText(f"Attempts: {self.attempts}")
        self.guess_input.clear()
        
        if guess == self.target_number:
            self.result_label.setText(f"🎉 Congratulations! You guessed it in {self.attempts} attempts!")
            QMessageBox.information(self, "You Won!", f"Great job! The number was {self.target_number}")
        elif guess < self.target_number:
            self.result_label.setText("📈 Too low! Try a higher number.")
        else:
            self.result_label.setText("📉 Too high! Try a lower number.")

def main():
    app = QApplication(sys.argv)
    game_center = GameCenter()
    game_center.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()