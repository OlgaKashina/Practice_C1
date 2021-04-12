from random import randint  # случайные числа


class Dot:  # класс точек на поле
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # чтобы точки можно было проверять на равенство
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # вернет строку, содержащую печатаемое формальное представление объекта
        return f"({self.x}, {self.y})"


class BoardException(Exception):  # Родитель всех исключений
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Shot outside the board!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "This cell has already been shot!"


class BoardWrongShipException(BoardException):  # Не правильно поставлен корабль
    pass


class Ship:  # корабль на игровом поле, который описывается параметрами:
    def __init__(self, bow, length, o):
        self.bow = bow  # точка, где размещён нос корабля
        self.length = length  # длина
        self.o = o  # направление корабля(вертикальное / горизонтальное)
        self.lives = length  # количеством жизней (сколько точек корабля еще не подбито)

    @property
    def dots(self):  # возвращает список всех точек корабля
        ship_dots = []
        for i in range(self.length):
            new_x = self.bow.x
            new_y = self.bow.y

            if self.o == 0:
                new_x += i

            elif self.o == 1:
                new_y += i

            ship_dots.append(Dot(new_x, new_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:  # игровая доска, описывается параметрами
    def __init__(self, hid=False, size=6):
        self.size = size  # размер поля
        self.hid = hid  # информация о том, нужно ли скрывать корабли на доске

        self.count = 0  # Количество убитых кораблей на доске

        self.field = [["0"] * size for _ in range(size)]  # Двумерный список, в котором хранятся состояния клеток

        self.busy = []  # Список занятых клеток
        self.ships = []  # Список кораблей доски

    def add_ship(self, ship):  # ставит корабль на доску (если ставить не получается, выбрасывается исключение)

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # обводит корабль по контуру
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):  # выводит доску в консоль в зависимости от параметра hid
        res = ""  # переменная res записывает всю доску
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | {' | '.join(row)} | "

        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, d):  # для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):  # делает выстрел по доске
        if self.out(d):  # если есть попытка выстрелить за пределы
            raise BoardOutException()

        if d in self.busy:  # и в использованную точку
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Ship destroyed!")
                    return False
                else:
                    print("The ship is injured!")
                    return True

        self.field[d.x][d.y] = "."
        print("Past!")
        return False

    def begin(self):
        self.busy = []


class Player:  # класс игрока в игру (и AI, и пользователь).
    def __init__(self, board, enemy):
        self.board = board  # Собственная доска (объект класса Board)
        self.enemy = enemy  # Доска врага

    def ask(self):  # «спрашивает» игрока, в какую клетку он делает выстрел, потомки должны реализовать этот метод
        raise NotImplementedError()

    def move(self):  # делает ход в игре
        while True:
            try:
                target = self.ask()  # спрашиваем координаты выстрела в доску врага
                repeat = self.enemy.shot(target)  # делаем выстрел по вражеской доске
                return repeat
            except BoardException as e:  # отлавливаем исключения, и если они есть, пытаемся повторить ход
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))  # выбор случайной точки
        print(f"Computer run: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):  # спрашивает координаты точки из консоли
        while True:
            cords = input("Your turn: ").split()

            if len(cords) != 2:
                print(" Enter 2 coordinates! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not(y.isdigit()):
                print(" Enter numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()  # Доска пользователя
        co = self.random_board()  # Доска компьютера
        co.hid = True

        self.ai = AI(co, pl)  # Игрок-компьютер, объект класса Ai
        self.us = User(pl, co)  # Игрок-пользователь, объект класса User

    def random_board(self):  # генерирует случайную доску
        board = None  # изначально пустая доска
        while board is None:  # в бесконечном цикле пытаемся поставить корабль в случайную току,
            board = self.random_place()     # пока наша попытка не окажется успешной
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in lens:
            while True:
                attempts += 1  # Если было сделано много (несколько тысяч) попыток установить корабль,
                if attempts > 2000:  # но это не получилось, значит доска неудачная и на неё корабль уже не добавить.
                    return None  # В таком случае нужно начать генерировать новую доску.
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-----------------------")
        print("  Welcome to the game  ")
        print("      Sea Battle       ")
        print("-----------------------")
        print("   format input: x y   ")
        print("   x - number line     ")
        print("   y - number column   ")

    def loop(self):  # метод с самим игровым циклом. Последовательно вызываем метод mode для игроков и делаем проверку,
        num = 0  # сколько живых кораблей осталось на досках, чтобы определить победу
        while True:
            print("-" * 20)
            print("User board:")
            print(self.us.board)
            print("-" * 20)
            print("Computer board:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("User go!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Computer go!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("User win!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Computer win!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
