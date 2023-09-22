from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class RuleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(750, 200)
        self.setWindowTitle("Правила")

        layout = QVBoxLayout()

        head_label = QLabel("Правила игры Быки и Коровы")
        head_label.setAlignment(Qt.AlignCenter)
        head_label.setFont(QFont("Times", 18, italic=True))

        rules_label = QLabel(
            "Каждый из противников задумывает четырехзначное число (первая цифра числа отлична от нуля).\n\n" +
            "Необходимо разгадать задуманное число! Выигрывает тот, кто отгадает первый.\n\n" +
            "Противники по очереди называют друг другу числа и сообщают о количестве «быков» и «коров» в названом "
            "числе:\n" +
            "«бык» — цифра есть в записи задуманного числа и стоит в той же позиции, что и в задуманном числе;\n" +
            "«корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции, что и в задуманном "
            "числе.\n")
        rules_label.setFont(QFont("Times", 10, italic=True))
        layout.addWidget(rules_label)

        self.setLayout(layout)


def toggle_window(win):
    if win.isVisible():
        win.hide()
    else:
        win.show()


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Быки и коровы")
        self.setFixedSize(300, 200)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.game_window = None
        rule_window = RuleWindow()

        layout = QVBoxLayout()

        heading_label = QLabel("Главное меню")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setFont(QFont("Times", 18, italic=True))
        layout.addWidget(heading_label)

        two_players_game_button = QPushButton("Режим игры на 2-х игроков")
        two_players_game_button.clicked.connect(lambda: self.start_game("TwoPlayers"))
        layout.addWidget(two_players_game_button)

        computer_game_button = QPushButton("Режим игры с компьютером")
        computer_game_button.clicked.connect(lambda: self.start_game("WithComputer"))
        layout.addWidget(computer_game_button)

        rules_button = QPushButton("Правила")
        rules_button.clicked.connect(lambda checked: toggle_window(rule_window))
        layout.addWidget(rules_button)

        rules_button = QPushButton("Выйти из игры")
        rules_button.clicked.connect(self.close)
        layout.addWidget(rules_button)
        self.central_widget.setLayout(layout)

    def start_game(self, opponent):
        try:
            module = __import__(opponent)
            opponent_class = getattr(module, f"{opponent}")
            self.game_window = opponent_class()
            self.game_window.show()
            self.close()
        except ImportError as e:
            print(f"Ошибка импорта модуля: {e}")


if __name__ == "__main__":
    app = QApplication()
    window = MainMenu()
    window.show()
    app.exec()
