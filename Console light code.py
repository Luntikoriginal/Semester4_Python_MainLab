import itertools
import random


def input_num():
    while True:
        numb = int(input("Число: "))
        if 999 < numb < 10000:
            return numb
        else:
            print("Число 4-х значное, попробуйте снова!")


def get_figure(number, n):
    return number // 10 ** n % 10


def check_step(numb, numb_opponent_player):
    i_used_indexes = []
    j_used_indexes = []
    box = []
    bulls = 0
    cows = 0
    for i in range(0, 4):
        if get_figure(numb, i) == get_figure(numb_opponent_player, i):
            bulls += 1
            i_used_indexes.append(i)
            j_used_indexes.append(i)
    for i in range(0, 4):
        if i in i_used_indexes:
            continue
        for j in range(0, 4):
            if j in j_used_indexes:
                continue
            if get_figure(numb, i) == get_figure(numb_opponent_player, j):
                cows += 1
                i_used_indexes.append(i)
                j_used_indexes.append(j)
                break
    box.append(bulls)
    box.append(cows)

    return box


def player_step(numb_opponent_player):
    numb = input_num()
    return check_step(numb, numb_opponent_player)


def two_players_game():
    print("\nИгра начинается!\n")
    print("Игрок 1 загадывает число")
    num_player1 = input_num()
    print("Игрок 2 загадывает число")
    num_player2 = input_num()
    step = 0
    while True:
        step += 1
        if step % 2 == 1:
            print("Ход игрока 1")
            bulls_cows_box = player_step(num_player2)
            print("Быков:", bulls_cows_box[0], "Коров: ", bulls_cows_box[1])
            if bulls_cows_box[0] == 4:
                break
        else:
            print("Ход игрока 2")
            bulls_cows_box = player_step(num_player1)
            print("Быков:", bulls_cows_box[0], "Коров: ", bulls_cows_box[1])
            if bulls_cows_box[0] == 4:
                break
    if step % 2 == 1:
        print("Победил Игрок 1!")
    else:
        print("Победил Игрок 2!")
    return


def first_instruction(numb_opponent_player, figures, used_figures, possible_figures):

    a = random.choice(figures)
    while a == 0:
        a = random.choice(figures)

    b = random.choice(figures)
    while b == a:
        b = random.choice(figures)

    c = random.choice(figures)
    while c == a or c == b:
        c = random.choice(figures)

    d = random.choice(figures)
    while d == a or d == b or d == c:
        d = random.choice(figures)

    numb = int(''.join(map(str, [a, b, c, d])))
    print(numb)
    box = check_step(numb, numb_opponent_player)

    if box[0] == 0 and box[1] == 0:
        used_figures.append(a)
        figures.remove(a)
        used_figures.append(b)
        figures.remove(b)
        used_figures.append(c)
        figures.remove(c)
        used_figures.append(d)
        figures.remove(d)

    elif box[0] + box[1] == 4:
        possible_figures.append(a)
        possible_figures.append(b)
        possible_figures.append(c)
        possible_figures.append(d)

    return box


def second_instruction(numb_opponent_player, figures, used_figures, possible_figures):

    a = used_figures[0]
    b = used_figures[1]
    c = random.choice(figures)
    d = random.choice(figures)
    while d == c:
        d = random.choice(figures)

    numb = int(''.join(map(str, [a, b, c, d])))
    print(numb)
    box = check_step(numb, numb_opponent_player)

    if box[0] == 0 and box[1] == 0:
        used_figures.append(c)
        figures.remove(c)
        used_figures.append(d)
        figures.remove(d)

    elif box[0] + box[1] == 2:
        possible_figures.append(c)
        possible_figures.append(d)

    return box


def third_instruction(numb_opponent_player, figures, used_figures, possible_figures):
    if figures[0] != 0:
        a = figures[0]
        numb = int(''.join(map(str, [a, a, a, a])))
    else:
        b = used_figures[0]
        a = figures[0]
        numb = int(''.join(map(str, [b, a, a, a])))

    print(numb)
    box = check_step(numb, numb_opponent_player)

    possible = box[0] + box[1]
    if possible > 0:
        if a in possible_figures:
            for i in range(0, possible - 1):
                possible_figures.append(a)
        else:
            for i in range(0, possible):
                possible_figures.append(a)
        figures.remove(a)
    else:
        figures.remove(a)

    return box


def last_instruction(numb_opponent_player, possible_combinations):

    numb = random.choice(possible_combinations)
    print(numb)
    box = check_step(numb, numb_opponent_player)

    possible_combinations.remove(numb)

    return box


def computer_step(numb_opponent_player, figures, used_figures, possible_figures, possible_combinations):
    if len(possible_figures) == 4:
        return last_instruction(numb_opponent_player, possible_combinations)
    elif len(figures) == 10:
        return first_instruction(numb_opponent_player, figures, used_figures, possible_figures)
    elif len(figures) == 6:
        return second_instruction(numb_opponent_player, figures, used_figures, possible_figures)
    elif len(figures) <= 4:
        return third_instruction(numb_opponent_player, figures, used_figures, possible_figures)
    return


def computer_game():
    print("\nИгра начинается!\n")
    print("Загадайте число")
    num_player = input_num()
    num_computer = random.randint(1000, 9999)
    data_figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    data_used_figures = []
    data_possible_figures = []
    data_possible_combinations = []
    flag_full_data_possible = False

    step = 0
    while True:
        step += 1
        if step % 2 == 1:
            print("\nВаш ход")
            bulls_cows_box = player_step(num_computer)
            print("Быков:", bulls_cows_box[0], "Коров: ", bulls_cows_box[1])
            if bulls_cows_box[0] == 4:
                break
        else:
            print("\nХод компьютера")

            if len(data_possible_figures) == 4:
                if not flag_full_data_possible:
                    flag_full_data_possible = True
                    combinations = itertools.permutations(data_possible_figures)
                    for i in combinations:
                        num = int(''.join(map(str, i)))
                        if num >= 1000:
                            data_possible_combinations.append(num)

            bulls_cows_box = computer_step(num_player, data_figures, data_used_figures,
                                           data_possible_figures, data_possible_combinations)
            print("Быков:", bulls_cows_box[0], "Коров: ", bulls_cows_box[1])
            if bulls_cows_box[0] == 4:
                break

    if step % 2 == 1:
        print("Вы победили!")
    else:
        print("Победил гениальный компьютер, загадавший", num_computer)
    return


if __name__ == '__main__':
    while True:
        opponent = str(input("\nС кем будем играть: "))
        match opponent:
            case "player":
                two_players_game()
            case "computer":
                computer_game()
