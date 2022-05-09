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

MAN_COLOR = (31, 65, 96)
WOMAN_COLOR = (104, 22, 0)


# endregion


def to_norm_coord(draw_x, draw_y):
    norm_x = (draw_x - SHIFT) // 100
    norm_y = draw_y // 100
    return (norm_x, norm_y)


def to_draw_coord(norm_x, norm_y):
    draw_x = SHIFT + norm_x * 100 + 50
    draw_y = norm_y * 100 + 50
    return (draw_x, draw_y)


class WarriorSprite(arcade.Sprite):
    def __init__(self, image, scale, warrior):
        super().__init__(image, scale)
        self.warrior = warrior
        (self.center_x, self.center_y) = to_draw_coord(warrior.x, warrior.y)

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
                         font_name="Kenney Future Narrow")

    def update(self):
        (dest_x, dest_y) = to_draw_coord(self.warrior.x, self.warrior.y)
        if abs(self.center_x - dest_x) <= abs(self.change_x):
            self.center_x = dest_x
            self.change_x = 0
        else:
            self.center_x += self.change_x

        if self.change_x == 0:
            if abs(self.center_y - dest_y) <= abs(self.change_y):
                self.center_y = dest_y
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

        self.left_text_move_points = None
        self.right_text_move_points = None
        self.left_sprite_move_points = None
        self.right_sprite_move_points = None

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
        for x in range(SIZE):
            for y in range(SIZE):
                cell_sprite = arcade.Sprite(img, SPRITE_SCALING_CELL)
                (cell_sprite.center_x, cell_sprite.center_y) = to_draw_coord(x, y)
                self.scene.add_sprite("Cells", cell_sprite)

        self.g = game_logic.Game("Turn M", 10, [])

        warrior = game_logic.Warrior(0, 0, "M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_PAL)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T1_P_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior(0, 1, "M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_ARC)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T1_A_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior(0, 2, "M", 10, 1, game_logic.Warrior.DAMAGE_FIELD_M_WIZ)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T1_W_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior(7, 0, "W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_PAL)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T2_P_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior(7, 1, "W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_ARC)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T2_A_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        warrior = game_logic.Warrior(7, 2, "W", 10, 1, game_logic.Warrior.DAMAGE_FIELD_W_WIZ)
        self.g.add_warrior(warrior)
        warrior_sprite = WarriorSprite("images/T2_W_128.png", SPRITE_SCALING_WARRIOR, warrior)
        self.scene.add_sprite("Warriors", warrior_sprite)

        self.left_text_move_points = arcade.Text(text=f"{self.g.move_points}",
                                                 start_x=10,
                                                 start_y=SCREEN_HEIGHT - 10,
                                                 color=MAN_COLOR,
                                                 font_size=18,
                                                 font_name="Kenney Future Narrow",
                                                 anchor_x="left",
                                                 anchor_y="top")

        self.right_text_move_points = arcade.Text(text=f"{self.g.move_points}",
                                                  start_x=10,
                                                  start_y=SCREEN_HEIGHT - 10,
                                                  color=WOMAN_COLOR,
                                                  font_size=18,
                                                  font_name="Kenney Future Narrow",
                                                  anchor_x="left",
                                                  anchor_y="top")

    def on_click_left_end_turn(self, event):
        self.g.complete_move()

    def draw_left_text_move_points(self):
        self.left_text_move_points = arcade.Text(text=f"{self.g.move_points}",
                                                 start_x=10,
                                                 start_y=SCREEN_HEIGHT - 10,
                                                 color=MAN_COLOR,
                                                 font_size=18,
                                                 font_name="Kenney Future Narrow",
                                                 anchor_x="left",
                                                 anchor_y="top")
        self.left_text_move_points.draw()

    def draw_left_line_move_points(self):
        if self.g.move_points > 0:
            center_x_begin = 50
            self.left_sprite_move_points = arcade.Sprite(filename="images/left_move_points_M.png",
                                                         image_width=9,
                                                         image_height=18,
                                                         center_y=SCREEN_HEIGHT - 24,
                                                         center_x=center_x_begin)
            self.left_sprite_move_points.draw()

            for i in range(self.g.move_points - 1):
                self.left_sprite_move_points = arcade.Sprite(filename="images/center_move_points_M.png",
                                                             image_width=18,
                                                             image_height=18,
                                                             center_y=SCREEN_HEIGHT - 24,
                                                             center_x=center_x_begin + 13.5 + i * 18)
                self.left_sprite_move_points.draw()

            self.left_sprite_move_points = arcade.Sprite(filename="images/right_move_points_M.png",
                                                         image_width=9,
                                                         image_height=18,
                                                         center_y=SCREEN_HEIGHT - 24,
                                                         center_x=center_x_begin + 9 + (self.g.move_points - 1) * 18)
            self.left_sprite_move_points.draw()

    def draw_right_text_move_points(self):
        self.left_text_move_points = arcade.Text(text=f"{self.g.move_points}",
                                                 start_x=SCREEN_WIDTH + 2 * SHIFT - 10,
                                                 start_y=SCREEN_HEIGHT - 10,
                                                 color=WOMAN_COLOR,
                                                 font_size=18,
                                                 font_name="Kenney Future Narrow",
                                                 anchor_x="right",
                                                 anchor_y="top")
        self.left_text_move_points.draw()

    def draw_right_line_move_points(self):
        if self.g.move_points > 0:
            center_x_begin = SCREEN_HEIGHT + 2 * SHIFT - 50
            self.left_sprite_move_points = arcade.Sprite(filename="images/right_move_points_W.png",
                                                         image_width=9,
                                                         image_height=18,
                                                         center_y=SCREEN_HEIGHT - 24,
                                                         center_x=center_x_begin)
            self.left_sprite_move_points.draw()

            for i in range(self.g.move_points - 1):
                self.left_sprite_move_points = arcade.Sprite(filename="images/center_move_points_W.png",
                                                             image_width=18,
                                                             image_height=18,
                                                             center_y=SCREEN_HEIGHT - 24,
                                                             center_x=center_x_begin - 13.5 - i * 18)
                self.left_sprite_move_points.draw()

            self.left_sprite_move_points = arcade.Sprite(filename="images/left_move_points_W.png",
                                                         image_width=9,
                                                         image_height=18,
                                                         center_y=SCREEN_HEIGHT - 24,
                                                         center_x=center_x_begin - 9 - (self.g.move_points - 1) * 18)
            self.left_sprite_move_points.draw()

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()

        for ws in self.scene.get_sprite_list("Warriors"):
            if ws.warrior.health <= 0:
                ws.remove_from_sprite_lists()
            else:
                ws.draw_health_number()

        if self.g.mode == "Turn M":
            self.draw_left_text_move_points()
            self.draw_left_line_move_points()

        elif self.g.mode == "Turn W":
            self.draw_right_text_move_points()
            self.draw_right_line_move_points()

        if self.selected_warrior_sprite is not None:
            self.draw_damage()
        self.manager.draw()

    def get_warrior_sprite_by_coordinates(self, x, y):
        for warrior_sprite in self.scene.get_sprite_list("Warriors"):
            if (warrior_sprite.center_x // 100 == x // 100 and
                    warrior_sprite.center_y // 100 == y // 100):
                return warrior_sprite

    def draw_damage(self):
        ws = self.selected_warrior_sprite
        df = ws.warrior.damage_field
        (norm_x, norm_y) = to_norm_coord(ws.center_x, ws.center_y)
        start_index = - (len(df) // 2)
        end_index = len(df) // 2
        for y in range(start_index, end_index + 1):
            for x in range(start_index, end_index + 1):
                if ((x, y) != (0, 0) and
                        0 <= norm_x + x < SIZE and
                        0 <= norm_y + y < SIZE and
                        df[y + len(df) // 2][x + len(df) // 2] != 0):
                    (draw_x, draw_y) = to_draw_coord(norm_x + x, norm_y + y)
                    s = str(df[y + len(df) // 2][x + len(df) // 2])
                    arcade.draw_text(s,
                                     draw_x + 4,
                                     draw_y,
                                     arcade.color.CARNELIAN,
                                     40,
                                     anchor_x="center",
                                     anchor_y="center",
                                     font_name="Kenney Future Narrow",
                                     bold=True)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LALT:
            self.scene.get_sprite_list("Cells")[0].color = arcade.csscolor.RED
            if self.selected_warrior_sprite is not None:
                self.draw_damage()

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.LALT:
            self.scene.get_sprite_list("Cells")[0].color = arcade.csscolor.WHITE

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        (norm_x, norm_y) = to_norm_coord(x, y)

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.selected_warrior_sprite is None:
                self.selected_warrior_sprite = self.get_warrior_sprite_by_coordinates(x, y)
            else:
                (draw_x, draw_y) = to_draw_coord(norm_x, norm_y)
                if (SHIFT <= draw_x <= SHIFT + SCREEN_WIDTH and
                        (0 <= draw_y <= SCREEN_HEIGHT)):
                    (from_x, from_y) = to_norm_coord(self.selected_warrior_sprite.center_x,
                                                     self.selected_warrior_sprite.center_y)
                    (to_x, to_y) = (norm_x, norm_y)

                    self.g.go(from_x, from_y, to_x, to_y)

                    self.selected_warrior_sprite.destination_x = draw_x
                    self.selected_warrior_sprite.destination_y = draw_y
                    self.selected_warrior_sprite.change_x = int(math.copysign(1.0,
                                                                              self.selected_warrior_sprite.destination_x - self.selected_warrior_sprite.center_x)) * WARRIOR_MOVEMENT_SPEED
                    self.selected_warrior_sprite.change_y = int(math.copysign(1.0,
                                                                              self.selected_warrior_sprite.destination_y - self.selected_warrior_sprite.center_y)) * WARRIOR_MOVEMENT_SPEED

                self.selected_warrior_sprite = None

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.g.attack(norm_x, norm_y)

    def on_update(self, delta_time):
        self.scene.update()


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
