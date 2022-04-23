class Warrior:
    # M_PAL = 43   M_ARC = 36   M_WIZ = 40
    # W_PAL = 44   W_ARC = 36   W_WIZ = 48
    # TODO Может, добавить аптекария, который лечит своих?))

    DAMAGE_FIELD_M_PAL = [[0, 0, 0, 0, 0],
                          [0, 3, 7, 3, 0],
                          [0, 7, 0, 7, 0],
                          [0, 3, 7, 3, 0],
                          [0, 0, 0, 0, 0]]

    DAMAGE_FIELD_M_ARC = [[0, 0, 6, 0, 0],
                          [0, 3, 0, 3, 0],
                          [6, 0, 0, 0, 6],
                          [0, 3, 0, 3, 0],
                          [0, 0, 6, 0, 0]]

    DAMAGE_FIELD_M_WIZ = [[1, 1, 1, 1, 1],
                          [1, 3, 3, 3, 1],
                          [1, 3, 0, 3, 1],
                          [1, 3, 3, 3, 1],
                          [1, 1, 1, 1, 1]]

    DAMAGE_FIELD_W_PAL = [[0, 0, 0, 0, 0],
                          [0, 4, 6, 4, 0],
                          [0, 6, 0, 6, 0],
                          [0, 4, 6, 4, 0],
                          [0, 0, 0, 0, 0]]

    DAMAGE_FIELD_W_ARC = [[0, 0, 5, 0, 0],
                          [0, 4, 0, 4, 0],
                          [5, 0, 0, 0, 5],
                          [0, 4, 0, 4, 0],
                          [0, 0, 5, 0, 0]]

    DAMAGE_FIELD_W_WIZ = [[2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2],
                          [2, 2, 0, 2, 2],
                          [2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2]]

    def __init__(self, x, y, team, health, number_of_attack, damage_field):
        self.team = team
        self.health = health
        self.number_of_attack = number_of_attack
        self.damage_field = damage_field
        self.x = x
        self.y = y

    def print_warrior_info(self):
        print(self.team, self.health, self.number_of_attack)


class Game:
    # TODO Изменить "Turn" на "Move" в значениях поля mode
    # TODO Изменить "Turn" на "Move" в названиях методов
    DEFAULT_SIZE_X = 8
    DEFAULT_SIZE_Y = 8
    DEFAULT_NUMBER_OF_WARRIORS = {"M": 3, "W": 3}
    DEFAULT_MOVE_POINTS = 10
    DEFAULT_NUMBER_OF_ATTACKS = 1

    def __init__(self, mode, move_points, warriors):
        self.mode = mode
        self.move_points = move_points
        self.warriors = warriors

    def print_game_info(self):
        print()
        print("------ Game Info ------")
        print("Mode = {0}".format(self.mode))
        print("Move points = {0}".format(self.move_points))
        for coordinates, warrior in self.warriors.items():
            print(coordinates, end=' ')
            warrior.print_warrior_info()
        print("-----------------------")

    def add_warrior(self, warrior):
        self.warriors.append(warrior)

    def start(self, first_move_team):
        if (first_move_team in ["M", "W"] and
                self.get_count_warriors("M") * self.get_count_warriors("W") != 0):
            self.mode = "Turn " + first_move_team

    def distance(self, x1, y1, x2, y2):
        if (0 <= x1 < self.DEFAULT_SIZE_X and
                0 <= y1 < self.DEFAULT_SIZE_Y and
                0 <= x2 < self.DEFAULT_SIZE_X and
                0 <= y2 < self.DEFAULT_SIZE_Y):
            return abs(x1 - x2) + abs(y1 - y2)
        else:
            return -1

    def get_warrior_by_norm_coordinates(self, norm_x, norm_y):
        for w in self.warriors:
            if (w.x == norm_x) and (w.y == norm_y):
                return w

    def go(self, from_norm_x, from_norm_y, to_norm_x, to_norm_y):
        w = self.get_warrior_by_norm_coordinates(from_norm_x, from_norm_y)
        if all([0 <= from_norm_x < self.DEFAULT_SIZE_X,
                0 <= from_norm_y < self.DEFAULT_SIZE_Y,
                0 <= to_norm_x < self.DEFAULT_SIZE_X,
                0 <= to_norm_y < self.DEFAULT_SIZE_Y,
                w is not None,
                self.get_warrior_by_norm_coordinates(to_norm_x, to_norm_y) is None,
                0 <= self.distance(from_norm_x, from_norm_y, to_norm_x, to_norm_y) <= self.move_points]):
            (w.x, w.y) = (to_norm_x, to_norm_y)
            self.move_points -= self.distance(from_norm_x, from_norm_y, to_norm_x, to_norm_y)

    def get_norm_coordinates_by_warrior(self, warrior):
        for c, w in self.warriors.items():
            if w == warrior:
                return c
        return None

    def get_count_warriors(self, team):
        count = 0
        for warrior in self.warriors.values():
            if warrior.team == team:
                count += 1
        return count

    def attack(self, from_x, from_y):
        attack_cell = (from_x, from_y)
        if (0 <= from_x < self.DEFAULT_SIZE_X and
                0 <= from_y < self.DEFAULT_SIZE_Y and
                attack_cell in self.warriors and
                "Turn " + self.warriors[attack_cell].team == self.mode and
                self.warriors[attack_cell].number_of_attack > 0):
            self.warriors[attack_cell].number_of_attack -= 1
            for dx in range(-2, 3, 1):
                for dy in range(-2, 3, 1):
                    victim_cell = (from_x + dx, from_y + dy)
                    if (0 <= from_x + dx < Game.DEFAULT_SIZE_X and
                            0 <= from_y + dy < Game.DEFAULT_SIZE_Y and
                            victim_cell in self.warriors and
                            self.warriors[attack_cell].team != self.warriors[victim_cell].team):
                        self.warriors[victim_cell].health -= self.warriors[attack_cell].damage_field[2 - dy][2 + dx]
                        if self.warriors[victim_cell].health <= 0:
                            del self.warriors[victim_cell]
                            if self.get_count_warriors(self.warriors[victim_cell].team) == 0:
                                self.mode = "Win " + self.warriors[attack_cell].team

    def refresh(self, team):
        if team == 'M' or team == 'W':
            self.move_points = self.DEFAULT_MOVE_POINTS
            for warrior in self.warriors.values():
                if warrior.team == team:
                    warrior.number_of_attack = self.DEFAULT_NUMBER_OF_ATTACKS

    def end_turn(self):
        if self.get_count_warriors("M") == 0:
            self.mode = "Win W"
        elif self.get_count_warriors("W") == 0:
            self.mode = "Win M"
        elif self.mode == "Turn M":
            self.mode = "Turn W"
            self.refresh("W")
        elif self.mode == "Turn W":
            self.mode = "Turn M"
            self.refresh("M")


if __name__ == "__main__":
    w1 = Warrior(0, 0, "M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w2 = Warrior(0, 1, "M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w3 = Warrior(0, 2, "M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w4 = Warrior(7, 0, "W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w5 = Warrior(7, 1, "W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w6 = Warrior(7, 2, "W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)

    ws = [w1, w2, w3, w4, w5, w6]

    g = Game("Turn M", 10, ws)
    g.print_game_info()
    g.go(0, 0, 6, 0)
    g.print_game_info()
    g.attack(6, 0)
    g.print_game_info()
