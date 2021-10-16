from pygame.tests.test_utils import endian


class Warrior:
    DAMAGE_FIELD_M_PAL = [[0, 0, 0, 0, 0],
                          [0, 4, 6, 4, 0],
                          [0, 6, 0, 6, 0],
                          [0, 4, 6, 4, 0],
                          [0, 0, 0, 0, 0]]

    def __init__(self, team, health, number_of_attack, damage_field):
        self.team = team
        self.health = health
        self.number_of_attack = number_of_attack
        self.damage_field = damage_field

    def print_warrior_info(self):
        print(self.team, self.health, self.number_of_attack)


class Game:
    MAX_SIZE_X = 8
    MAX_SIZE_Y = 8
    DEFAULT_MOVE_POINTS = 10

    def __init__(self, mode, move_points, selected_cell, warriors):
        self.mode = mode
        self.move_points = move_points
        self.selected_cell = selected_cell
        self.warriors = warriors

    def print_game_info(self):
        print()
        print("------ Game Info ------")
        print("Mode = {0}".format(self.mode))
        print("Move points = {0}".format(self.move_points))
        print("Selected cell = {0}".format(self.selected_cell))
        for coordinates, warrior in self.warriors.items():
            print(coordinates, end=' ')
            warrior.print_warrior_info()
        print("-----------------------")

    def select(self, x, y):
        if 0 <= x < self.MAX_SIZE_X and 0 <= y < self.MAX_SIZE_Y:
            self.selected_cell = (x, y)

    def go(self, from_x, from_y, to_x, to_y):
        if (0 <= from_x < self.MAX_SIZE_X and
                0 <= from_y < self.MAX_SIZE_Y and
                0 <= to_x < self.MAX_SIZE_X and
                0 <= to_y < self.MAX_SIZE_Y and
                (from_x, from_y) in self.warriors and
                (to_x, to_y) not in self.warriors and
                (abs(from_x - to_x) + abs(from_y - to_y)) <= self.move_points):
            w = self.warriors[(from_x, from_y)]
            self.warriors[(to_x, to_y)] = w
            del self.warriors[(from_x, from_y)]
            self.move_points -= abs(from_x - to_x) + abs(from_y - to_y)
            self.select(to_x, to_y)

    def get_count_warriors(self, team):
        count = 0
        for coordinates, warrior in self.warriors:
            if warrior.team == team:
                count += 1
        return count

    def end_turn(self):
        if self.get_count_warriors("M") == 0:
            self.mode = "Win W"
        elif self.get_count_warriors("W") == 0:
            self.mode = "Win M"
        elif self.mode == "Turn M":
            self.mode == "Turn W"
            self.move_points = self.DEFAULT_MOVE_POINTS
        elif self.mode == "Turn W":
            self.mode == "Turn M"
            self.move_points = self.DEFAULT_MOVE_POINTS


if __name__ == "__main__":
    w1 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w2 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w3 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w4 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w5 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
    w6 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)

    ws = {(0, 0): w1,
          (0, 1): w2,
          (0, 2): w3,
          (7, 0): w4,
          (7, 1): w5,
          (7, 2): w6}

    g = Game("Turn_M", 10, (0, 0), ws)
    g.print_game_info()
    g.go(0, 0, 3, 0)
    g.print_game_info()
