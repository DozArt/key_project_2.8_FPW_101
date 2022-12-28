from random import randint


class Dot:  # точка
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # строковое представление точки?
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        # print(ship_dots)
        return ship_dots

    # def shooten(self, shot):
    #     return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "·"
                    self.busy.append(cur)

    def __str__(self):
        res = " "
        for a in range(self.size):  # Изменил нумерацию верхней строки
            res += "  " + str(a + 1)
        res += " |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}| " + "  ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def split(self):
        res = [" "]
        for a in range(self.size):
            res[0] += "  " + str(a + 1)
        res[0] += "  "
        for i, row in enumerate(self.field):
            res.append(f"{i + 1}| " + "  ".join(row) + " |")
            if self.hid:
                res[i + 1] = res[i + 1].replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "·"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):  # добавляем elf.enemy.size чтобы AI знал размер поля
        d = Dot(randint(0, self.enemy.size - 1), randint(0, self.enemy.size - 1))

        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=8):
        self.size = self.greet()  # Теперь мы запрашиваем размер поля перед инициализацией
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("---------------------")
        print("   Приветсвуем вас  ")
        print("       в игре       ")
        print("     морской бой    ")
        print("---------------------")
        while True:
            print(" Введите размер поля")
            size = int(input(" от 5 до 9: "))
            if 5 <= size <= 9:
                break
            else:
                print("Размер вне диапазона")
        print("---------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        return size

    def loop(self):
        s = self.us.board.size  # размер матрицы
        num = 0
        while True:
            print("-" * 6 * (s + 2))  # Высшая математика количество дефисов
            print(f"Доска пользователя: {'   ' * (s - 5)}    Доска компьютера:")  # динамический пробел
            for i in range(s + 1):
                print(f"{self.us.board.split()[i]}      {self.ai.board.split()[i]}")
            # print("Доска пользователя:")
            # print(self.us.board)
            # print("-" * 20)
            # print("Доска компьютера:")
            # print(self.ai.board)
            if num % 2 == 0:
                print("-" * 6 * (s + 2))
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        # self.greet()
        self.loop()


g = Game()
g.start()
