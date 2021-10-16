class Warrior:

    def __init__(self, team, health, number_of_attack, damage_field):
        self.team = team
        self.health = health
        self.number_of_attack = number_of_attack
        self.damage_field = damage_field

    def print_warrior_info(self):
        print(self.team)
        print(self.health)
        print(self.number_of_attack)


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
        for warrior in self.warriors:
            warrior.print_warrior_info()
        print(self.warriors)
