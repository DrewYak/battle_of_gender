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

    def __init__(self, mode, move_points, selected_cell, warriors):
        self.mode = mode
        self.move_points = move_points
        self.selected_cell = selected_cell
        self.warriors = warriors

    def print_game_info(self):
        print(self.mode)
        print(self.move_points)
        print(self.selected_cell)
        for coordinates, warrior in self.warriors.items():
            print(coordinates, end=' ')
            warrior.print_warrior_info()
        print(self.warriors)


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

    g = Game("Turn_M", 10, (0,0), ws)
    g.print_game_info()
