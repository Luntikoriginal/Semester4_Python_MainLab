from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QMessageBox, QListWidget, QHBoxLayout, QMenuBar, QMenu


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


class TwoPlayers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Быки и коровы")

        self.main_menu_window = None
        self.rule_window = RuleWindow()
        self.num_attempts = 1
        self.secret_number_player1 = None
        self.secret_number_player2 = None
        self.current_player = 1

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = QMenu("Меню", self)
        menu_bar.addMenu(file_menu)
        main_menu_action = QAction("Главное меню", self)
        main_menu_action.triggered.connect(self.main_menu)
        file_menu.addAction(main_menu_action)
        new_game_action = QAction("Новая игра", self)
        new_game_action.triggered.connect(self.new_game)
        file_menu.addAction(new_game_action)
        rules_action = QAction("Правила", self)
        rules_action.triggered.connect(self.rule_window.show)
        file_menu.addAction(rules_action)

        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.label_steps_player1 = QLabel("Ходы игрока 1")
        self.label_steps_player1.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(self.label_steps_player1)
        self.history_list_player1 = QListWidget()
        self.left_layout.addWidget(self.history_list_player1)
        self.main_layout.addLayout(self.left_layout)

        self.central_layout = QVBoxLayout()

        self.label_game = QLabel("Игрок 1: Загадайте число")
        self.label_game.setFixedSize(140, 40)
        self.label_game.setAlignment(Qt.AlignCenter)
        self.central_layout.addWidget(self.label_game)
        self.input_box = QLineEdit()
        self.central_layout.addWidget(self.input_box)
        self.button = QPushButton("Проверить")
        self.button.clicked.connect(self.check_guess)
        self.central_layout.addWidget(self.button)
        self.label_result = QLabel()
        self.label_result.setFixedSize(140, 30)
        self.label_result.setAlignment(Qt.AlignCenter)
        self.central_layout.addWidget(self.label_result)
        self.main_layout.addLayout(self.central_layout)

        self.right_layout = QVBoxLayout()
        self.label_steps_player2 = QLabel("Ходы игрока 2")
        self.label_steps_player2.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.label_steps_player2)
        self.history_list_player2 = QListWidget()
        self.right_layout.addWidget(self.history_list_player2)
        self.main_layout.addLayout(self.right_layout)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def check_guess(self):
        guess = self.input_box.text()

        if not self.check_correct(guess):
            QMessageBox.warning(self, "Ошибка", "Введите 4-значное число!")
            return

        if self.secret_number_player1 is None and self.current_player == 1:
            self.secret_number_player1 = guess
            QMessageBox.information(self, "Информация", "Число загадано!")
            self.current_player = 2
            self.input_box.clear()
            self.label_game.setText("Игрок 2: Загадайте число")
            return

        if self.secret_number_player2 is None and self.current_player == 2:
            self.secret_number_player2 = guess
            QMessageBox.information(self, "Информация", "Число загадано!")
            self.current_player = 1
            self.input_box.clear()
            self.label_game.setText("Игрок 1: Отгадывайте")
            return

        if self.current_player == 1:
            bulls, cows = self.check_step(guess, self.secret_number_player2)
            result = f"Игрок {self.current_player}:\nБыки: {bulls}, Коровы: {cows}"
            self.label_result.setText(result)
            self.history_list_player1.addItem(
                f"{self.num_attempts}. {guess} - Быки: {bulls}, Коровы: {cows}")
            if bulls == 4:
                QMessageBox.information(self, "Победа!", f"Игрок 1 выиграл за {self.num_attempts} попыток!\n"
                                                         f"Загадавший число {self.secret_number_player1}")
                self.main_menu()
                self.close()
            self.current_player = 2
            self.input_box.clear()
            self.label_game.setText("Игрок 2: Отгадывайте")
            return

        if self.current_player == 2:
            bulls, cows = self.check_step(guess, self.secret_number_player1)
            result = f"Игрок {self.current_player}:\nБыки: {bulls}, Коровы: {cows}"
            self.label_result.setText(result)
            self.history_list_player2.addItem(
                f"{self.num_attempts}. {guess} - Быки: {bulls}, Коровы: {cows}")
            if bulls == 4:
                QMessageBox.information(self, "Победа!", f"Игрок 2 выиграл за {self.num_attempts} попыток!\n"
                                                         f"Загадавший число {self.secret_number_player2}")
                self.main_menu()
                self.close()
            self.current_player = 1
            self.input_box.clear()
            self.num_attempts += 1
            self.label_game.setText("Игрок 1: Отгадывайте")
            return

    @staticmethod
    def get_figure(number, n):
        return int(number) // 10 ** n % 10

    def check_correct(self, n):
        return n.isdigit() and len(n) == 4 and self.get_figure(n, 3) != 0

    def check_step(self, numb, numb_opponent_player):
        i_used_indexes = []
        j_used_indexes = []
        bulls = 0
        cows = 0
        for i in range(0, 4):
            if self.get_figure(numb, i) == self.get_figure(numb_opponent_player, i):
                bulls += 1
                i_used_indexes.append(i)
                j_used_indexes.append(i)
        for i in range(0, 4):
            if i in i_used_indexes:
                continue
            for j in range(0, 4):
                if j in j_used_indexes:
                    continue
                if self.get_figure(numb, i) == self.get_figure(numb_opponent_player, j):
                    cows += 1
                    i_used_indexes.append(i)
                    j_used_indexes.append(j)
                    break
        return bulls, cows

    def main_menu(self):
        try:
            module = __import__("MainMenu")
            main_menu_class = getattr(module, f"MainMenu")
            self.main_menu_window = main_menu_class()
            self.main_menu_window.show()
            self.close()
        except ImportError as e:
            print(f"Ошибка импорта модуля: {e}")

    def new_game(self):
        self.num_attempts = 1
        self.secret_number_player1 = None
        self.secret_number_player2 = None
        self.current_player = 1
        self.label_game.setText("Игрок 1: Загадайте число")
        self.history_list_player1.clear()
        self.history_list_player2.clear()
        self.label_result.clear()


if __name__ == "__main__":
    app = QApplication([])
    game = TwoPlayers()
    game.show()
    app.exec()
