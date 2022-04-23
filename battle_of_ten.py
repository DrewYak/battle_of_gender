import arcade
import arcade.gui
import math
import game_logic

# region Константы

SPRITE_SCALING_CELL = 1.0
SPRITE_SCALING_WARRIOR = 87 / 128
SIZE = 8
SHIFT = 300

WARRIOR_MOVEMENT_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Битва полов"

HEALTH_BAR_WIDTH = 95
HEALTH_BAR_HEIGHT = 5
HEALTH_BAR_OFFSET_Y = 50

HEALTH_NUMBER_OFFSET_X = 30
HEALTH_NUMBER_OFFSET_Y = 28

MAX_HEALTH = 10

# endregion


class WarriorSprite(arcade.Sprite):
    def __init__(self, image, scale, warrior):
        super().__init__(image, scale)
        self.destination_x = self.center_x
        self.destination_y = self.center_y
        self.warrior = warrior
        # Наверное, warrior должен знать свои кординаты, а не только игра.
        # self.center_x = 0 * 100 + SHIFT + 50;
        # self.center_y = 0 * 100 + 50;

    def get_norm_x(self):
        return (self.center_x - SHIFT) // 100

    def get_norm_y(self):
        return self.center_y // 100

    def draw_health_number(self):
        health_string = f"{self.warrior.health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + 23,
                         start_y=self.center_y + 30,
                         font_size=14,
                         color=arcade.color.BROWN_NOSE,
                         width=20,
                         align="right",
                         bold=True,
                         font_name=('Kenney Future Narrow', 'arial'))

    def update(self):
        if abs(self.center_x - self.destination_x) <= abs(self.change_x):
            self.center_x = self.destination_x
            self.change_x = 0
        else:
            self.center_x += self.change_x

        if self.change_x == 0:
            if abs(self.center_y - self.destination_y) <= abs(self.change_y):
                self.center_y = self.destination_y
                self.change_y = 0
            else:
                self.center_y += self.change_y


class InstructionView(arcade.View):

    def on_show(self):
        arcade.set_background_color((217, 205, 175))
        arcade.set_viewport(0, SCREEN_WIDTH + SHIFT * 2 - 1, 0, SCREEN_HEIGHT + SHIFT * 2 - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("БИТВА ПОЛОВ",
                         (SCREEN_WIDTH + SHIFT * 2) / 2,
                         SCREEN_HEIGHT / 2,
                         arcade.color.AUBURN,
                         font_size=50,
                         anchor_x="center")
        arcade.draw_text("BATTLE OF GENDER",
                         (SCREEN_WIDTH + SHIFT * 2) / 2,
                         SCREEN_HEIGHT / 2 - 75,
                         arcade.color.AUBURN,
                         font_size=20,
                         anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene = None
        self.g = None

        self.selected_warrior_sprite = None

        self.window.background_color = (217, 205, 175)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.l_box = arcade.gui.UIBoxLayout()

        left_button_end_turn = arcade.gui.UIFlatButton(text="Завершить ход",
                                                       width=SHIFT / 2)
        left_button_end_turn.on_click = self.on_click_left_end_turn
        self.l_box.add(left_button_end_turn.with_space_around(80, 20, 20, 20))

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left",
                                                   anchor_y="top",
                                                   child=self.l_box, ))

    def setup(self):
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Cells")
        self.scene.add_sprite_list("Warriors")

        img = "images/cell.png"
        for i in range(SIZE):
            for j in range(SIZE):
                cell_sprite = arcade.Sprite(img, SPRITE_SCALING_CELL)
                cell_sprite.center_x = SHIFT + 50 + 100 * i
                cell_sprite.center_y = 50 + 100 * j
                self.scene.add_sprite("Cells", cell_sprite)

        self.g = game_logic.Game("Turn M", 10, {})

        warrior = game_logic.Warrior("M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_PAL)
        self.g.add(0, 2, warrior)
        img = "images/T1_P_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 50 + 6 * 100
        warrior_sprite.center_y = 50
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior("M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_ARC)
        self.g.add(2, 0, warrior)
        img = "images/T1_A_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 50
        warrior_sprite.center_y = 150
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior("M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_WIZ)
        self.g.add(0, 0, warrior)
        img = "images/T1_W_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 50
        warrior_sprite.center_y = 250
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior("W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_PAL)
        self.g.add(7, 5, warrior)
        img = "images/T2_P_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 750
        warrior_sprite.center_y = 50
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior("W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_ARC)
        self.g.add(5, 7, warrior)
        img = "images/T2_A_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 750
        warrior_sprite.center_y = 150
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior("W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_WIZ)
        self.g.add(7, 7, warrior)
        img = "images/T2_W_128.png"
        warrior_sprite = WarriorSprite(img, SPRITE_SCALING_WARRIOR, warrior)
        warrior_sprite.center_x = SHIFT + 750
        warrior_sprite.center_y = 250
        self.scene.add_sprite("Warriors", warrior_sprite)

    def on_click_left_end_turn(self, event):
        self.g.end_turn()

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        for ws in self.scene.get_sprite_list("Warriors"):
            ws.draw_health_number()

        text_mode = f"{self.g.mode}"
        arcade.draw_text(text_mode,
                         10,
                         SCREEN_WIDTH - 30,
                         arcade.color.WHITE,
                         18)

        text_move_points = f"{self.g.move_points}"
        arcade.draw_text(text_move_points,
                         10,
                         SCREEN_WIDTH - 50,
                         arcade.color.WHITE,
                         18)

        self.manager.draw()

    def get_warrior_sprite_by_coordinates(self, x, y):
        for warrior_sprite in self.scene.get_sprite_list("Warriors"):
            if (warrior_sprite.center_x // 100 == x // 100 and
                    warrior_sprite.center_y // 100 == y // 100):
                return warrior_sprite
        return None

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        norm_x = (x - SHIFT) // 100
        norm_y = y // 100

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.selected_warrior_sprite is None:
                self.selected_warrior_sprite = self.get_warrior_sprite_by_coordinates(x, y)
            else:
                draw_x = x // 100 * 100 + 50
                draw_y = y // 100 * 100 + 50
                if (SHIFT <= draw_x <= SHIFT + SCREEN_WIDTH and
                        (0 <= draw_y <= SCREEN_HEIGHT)):
                    from_x = self.selected_warrior_sprite.get_norm_x()
                    from_y = self.selected_warrior_sprite.get_norm_y()
                    to_x = norm_x
                    to_y = norm_y

                    self.g.go(from_x, from_y, to_x, to_y)

                    # self.selected_warrior_sprite.destination_x = draw_x
                    # self.selected_warrior_sprite.destination_y = draw_y
                    self.selected_warrior_sprite.destination_x = \
                    self.g.get_norm_coordinates_by_warrior(self.selected_warrior_sprite.warrior)[0] * 100 + SHIFT + 50
                    self.selected_warrior_sprite.destination_y = \
                    self.g.get_norm_coordinates_by_warrior(self.selected_warrior_sprite.warrior)[1] * 100 + 50
                    self.selected_warrior_sprite.change_x = int(math.copysign(1.0,
                                                                              self.selected_warrior_sprite.destination_x - self.selected_warrior_sprite.center_x)) * WARRIOR_MOVEMENT_SPEED
                    self.selected_warrior_sprite.change_y = int(math.copysign(1.0,
                                                                              self.selected_warrior_sprite.destination_y - self.selected_warrior_sprite.center_y)) * WARRIOR_MOVEMENT_SPEED
                self.selected_warrior_sprite = None

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.g.attack(norm_x, norm_y)

    def on_update(self, delta_time):
        self.scene.update()

        #     view = GameOverView()
        #     self.window.show_view(view)


class GameOverView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/cell.png")

    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2,
                                SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH,
                                SCREEN_HEIGHT)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH + SHIFT * 2, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == '__main__':
    main()
