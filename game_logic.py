class Game:
    # mode = 'Arrange W'
    # move_points = 10
    # selected_cell = (0, 0)
    # warriors = []

    def __init__(self, mode, move_points, selected_cell, warriors):
        self.mode = mode
        self.move_points = move_points
        self.selected_cell = selected_cell
        self.warriors = warriors

    def print_game_info(self):
        print(self.mode)
        print(self.move_points)
        print(self.selected_cell)
        print(self.warriors)
