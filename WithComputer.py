import itertools
import random

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


class WithComputer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Быки и коровы")

        self.main_menu_window = None
        self.rule_window = RuleWindow()
        self.num_attempts = 1
        self.secret_number_player = None
        self.secret_number_computer = random.randint(1000, 9999)
        self.data_figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.data_used_figures = []
        self.data_possible_figures = []
        self.data_possible_combinations = []
        self.flag_full_data_possible = False

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
        self.history_list_player = QListWidget()
        self.left_layout.addWidget(self.history_list_player)
        self.main_layout.addLayout(self.left_layout)

        self.central_layout = QVBoxLayout()

        self.label_game = QLabel("Загадайте число")
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
        self.label_steps_player2 = QLabel("Ходы компьютера")
        self.label_steps_player2.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.label_steps_player2)
        self.history_list_computer = QListWidget()
        self.right_layout.addWidget(self.history_list_computer)
        self.main_layout.addLayout(self.right_layout)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def check_guess(self):
        guess = self.input_box.text()

        if not self.check_correct(guess):
            QMessageBox.warning(self, "Ошибка", "Введите 4-значное число!")
            return

        if self.secret_number_player is None:
            self.secret_number_player = guess
            QMessageBox.information(self, "Информация", "Число загадано!")
            self.input_box.clear()
            self.label_game.setText("Отгадайте число")
            return

        bulls, cows = self.check_step(guess, self.secret_number_computer)
        result = f"Прошлый ход:\nБыки: {bulls}, Коровы: {cows}"
        self.label_result.setText(result)
        self.history_list_player.addItem(
            f"{self.num_attempts}. {guess} - Быки: {bulls}, Коровы: {cows}")
        if bulls == 4:
            QMessageBox.information(self, "Победа!", f"Выиграл игрок за {self.num_attempts} попыток!\n"
                                                     f"Загадавший {self.secret_number_player}")
            self.main_menu()
            self.close()
        self.input_box.clear()

        bulls, cows, computer_guess = self.computer_step()
        self.history_list_computer.addItem(
            f"{self.num_attempts}. {computer_guess} - Быки: {bulls}, Коровы: {cows}")
        if bulls == 4:
            QMessageBox.information(self, "Победа!", f"Выиграл гениальный компьютер за {self.num_attempts} попыток!\n"
                                                     f"Загадавший {self.secret_number_computer}")

            self.main_menu()
            self.close()
        if len(self.data_possible_figures) == 4:
            if not self.flag_full_data_possible:
                self.flag_full_data_possible = True
                combinations = itertools.permutations(self.data_possible_figures)
                for i in combinations:
                    num = int(''.join(map(str, i)))
                    if num >= 1000:
                        self.data_possible_combinations.append(num)
        self.num_attempts += 1
        return

    def first_instruction(self):

        box = []

        a = random.choice(self.data_figures)
        while a == 0:
            a = random.choice(self.data_figures)

        b = random.choice(self.data_figures)
        while b == a:
            b = random.choice(self.data_figures)

        c = random.choice(self.data_figures)
        while c == a or c == b:
            c = random.choice(self.data_figures)

        d = random.choice(self.data_figures)
        while d == a or d == b or d == c:
            d = random.choice(self.data_figures)

        numb = int(''.join(map(str, [a, b, c, d])))
        bulls, cows = self.check_step(numb, self.secret_number_player)

        if bulls == 0 and cows == 0:
            self.data_used_figures.append(a)
            self.data_figures.remove(a)
            self.data_used_figures.append(b)
            self.data_figures.remove(b)
            self.data_used_figures.append(c)
            self.data_figures.remove(c)
            self.data_used_figures.append(d)
            self.data_figures.remove(d)

        elif bulls + cows == 4:
            self.data_possible_figures.append(a)
            self.data_possible_figures.append(b)
            self.data_possible_figures.append(c)
            self.data_possible_figures.append(d)

        box.append(bulls)
        box.append(cows)
        box.append(numb)

        return box

    def second_instruction(self):

        box = []

        a = self.data_used_figures[0]
        b = self.data_used_figures[1]
        c = random.choice(self.data_figures)
        d = random.choice(self.data_figures)
        while d == c:
            d = random.choice(self.data_figures)

        numb = int(''.join(map(str, [a, b, c, d])))
        bulls, cows = self.check_step(numb, self.secret_number_player)

        if bulls == 0 and cows == 0:
            self.data_used_figures.append(c)
            self.data_figures.remove(c)
            self.data_used_figures.append(d)
            self.data_figures.remove(d)

        elif bulls + cows == 2:
            self.data_possible_figures.append(c)
            self.data_possible_figures.append(d)

        box.append(bulls)
        box.append(cows)
        box.append(numb)

        return box

    def third_instruction(self):

        box = []

        if self.data_figures[0] != 0:
            a = self.data_figures[0]
            numb = int(''.join(map(str, [a, a, a, a])))
        else:
            b = self.data_used_figures[0]
            a = self.data_figures[0]
            numb = int(''.join(map(str, [b, a, a, a])))

        bulls, cows = self.check_step(numb, self.secret_number_player)

        possible = bulls + cows
        if possible > 0:
            if a in self.data_possible_figures:
                for i in range(0, possible - 1):
                    self.data_possible_figures.append(a)
            else:
                for i in range(0, possible):
                    self.data_possible_figures.append(a)
            self.data_figures.remove(a)
        else:
            self.data_figures.remove(a)

        box.append(bulls)
        box.append(cows)
        box.append(numb)

        return box

    def last_instruction(self):

        box = []

        numb = random.choice(self.data_possible_combinations)
        bulls, cows = self.check_step(numb, self.secret_number_player)

        self.data_possible_combinations.remove(numb)

        box.append(bulls)
        box.append(cows)
        box.append(numb)

        return box

    def computer_step(self):
        if len(self.data_possible_figures) == 4:
            return self.last_instruction()
        elif len(self.data_figures) == 10:
            return self.first_instruction()
        elif len(self.data_figures) == 6:
            return self.second_instruction()
        elif len(self.data_figures) <= 4:
            return self.third_instruction()
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
        self.secret_number_player = None
        self.secret_number_computer = random.randint(1000, 9999)
        self.data_figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.data_used_figures = []
        self.data_possible_figures = []
        self.data_possible_combinations = []
        self.flag_full_data_possible = False
        self.label_game.setText("Загадайте число")
        self.history_list_player.clear()
        self.history_list_computer.clear()


if __name__ == "__main__":
    app = QApplication([])
    game = WithComputer()
    game.show()
    app.exec()
