class Ship:  # корабль
    def __init__(self, coordinates, size, orientation):
        self.cord = coordinates
        self.size = size
        self.orien = orientation
        self.deck = []

    def gen_deck(self):  # палуба(бы)
        deck = [self.cord]
        for i in range(1, self.size):
            deck.append(deck[0].copy())  # копируем первую палубу
            deck[i][self.orien] += i  # изменяем координату i палубы
        self.deck = deck
        return self.deck

    def __repr__(self):
        return self.deck

    # def shot(self, shot):


class Board:  # доска
    def __init__(self, fleet, size):
        self.fleet = fleet
        self.size = size
        self.bord = [["·"] * size for _ in range(size)]


    @property
    def open(self):
        for i in self.fleet:
            if i[2]:
                self.bord[i[0]-1][i[1]-1] = "х"
            else:
                self.bord[i[0] - 1][i[1] - 1] = "■"
        size = range(len(self.bord))  # Размер матрицы
        b = " "  # отступ первой строки
        for a in size:  # первая строка  str("1  2  3 ... n")
            b += "  " + str(a + 1)
        for a in size:  # последующие строки матрицы с номерацией
            b += f"\n{a + 1}  " + "  ".join(self.bord[a])
        return b


    def close(self):
        for _ in range(self.bord.count("■")):
            print(6)


    def shot(self,shot):
        c = shot.split()
        loyal_x = int(c[0]) - 1
        loyal_y = int(c[1]) - 1
        self.bord[loyal_x][loyal_y] = "֍"

ship1 = Ship([1,2,False],3,0)
print(ship1.gen_deck())
print(ship1)
fleet = ship1

board = Board(fleet.gen_deck(), 6)
print(board.open)
board.shot(input("x y: "))
print(board.open)
