import arcade
import math

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

class WarriorWithHealth(arcade.Sprite):
    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)
        self.max_health = max_health
        self.cur_health = max_health

    def update(self):
        if self.new_center_x != self.center_x:
            self.center_x += self.change_x
        elif self.new_center_y != self.center_y:
            self.center_y += self.change_y
        else:
            self.change_x = 0
            self.change_y = 0

    def go_to(self, new_center_x, new_center_y):
        if self.change_x == 0 and self.change_y == 0 and SHIFT + 50 <= new_center_x <= SHIFT + 750:
            self.new_center_x = new_center_x
            self.new_center_y = new_center_y

            dif_x = self.new_center_x - self.center_x
            dif_y = self.new_center_y - self.center_y

            self.change_x = math.copysign(WARRIOR_MOVEMENT_SPEED, dif_x)
            self.change_y = math.copysign(WARRIOR_MOVEMENT_SPEED, dif_y)

    def draw_health_number(self):
        health_string = f"{self.cur_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.BLACK)

    def draw_health_bar(self):
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTH_BAR_OFFSET_Y,
                                         width=HEALTH_BAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        health_width = HEALTH_BAR_WIDTH * (self.cur_health / self.max_health)
        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTH_BAR_WIDTH - health_width),
                                     center_y=self.center_y + 45,
                                     width=health_width,
                                     height=HEALTH_BAR_HEIGHT,
                                     color=arcade.color.ASPARAGUS)


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
        # super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        super().__init__()
        self.cell_list = None
        self.cell_sprite = None

        self.warrior_list = None
        self.warrior_sprite = None

        self.window.background_color = (217, 205, 175)

    def setup(self):
        self.cell_list = arcade.SpriteList()
        img = "images/cell.png"
        for i in range(SIZE):
            for j in range(SIZE):
                self.cell_sprite = arcade.Sprite(img, SPRITE_SCALING_CELL)
                self.cell_sprite.center_x = SHIFT + 50 + 100 * i
                self.cell_sprite.center_y = 50 + 100 * j
                self.cell_list.append(self.cell_sprite)

        self.warrior_list = arcade.SpriteList()

        img = "images/T1_P_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 50
        self.warrior_sprite.center_y = 50
        self.warrior_sprite.new_center_x = SHIFT + 50
        self.warrior_sprite.new_center_y = 50
        self.warrior_list.append(self.warrior_sprite)

        img = "images/T1_A_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 50
        self.warrior_sprite.center_y = 150
        self.warrior_sprite.new_center_x = SHIFT + 150
        self.warrior_sprite.new_center_y = 150
        self.warrior_list.append(self.warrior_sprite)

        img = "images/T1_W_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 50
        self.warrior_sprite.center_y = 250
        self.warrior_sprite.new_center_x = SHIFT + 50
        self.warrior_sprite.new_center_y = 250
        self.warrior_list.append(self.warrior_sprite)

        img = "images/T2_P_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 750
        self.warrior_sprite.center_y = 50
        self.warrior_sprite.new_center_x = SHIFT + 750
        self.warrior_sprite.new_center_y = 50
        self.warrior_list.append(self.warrior_sprite)

        img = "images/T2_A_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 750
        self.warrior_sprite.center_y = 150
        self.warrior_sprite.new_center_x = SHIFT + 750
        self.warrior_sprite.new_center_y = 150
        self.warrior_list.append(self.warrior_sprite)

        img = "images/T2_W_128.png"
        self.warrior_sprite = WarriorWithHealth(img, SPRITE_SCALING_WARRIOR, MAX_HEALTH)
        self.warrior_sprite.center_x = SHIFT + 750
        self.warrior_sprite.center_y = 250
        self.warrior_sprite.new_center_x = SHIFT + 750
        self.warrior_sprite.new_center_y = 50
        self.warrior_list.append(self.warrior_sprite)

    def on_draw(self):
        arcade.start_render()
        self.cell_list.draw()
        self.warrior_list.draw()

        for w in self.warrior_list:
            w.draw_health_number()
            w.draw_health_bar()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.warrior_list[0].go_to(x // 100 * 100 + 50, y // 100 * 100 + 50)

    def on_update(self, delta_time):
        self.cell_list.update()
        self.warrior_list.update()

        if self.warrior_list[0].center_x == 750 + SHIFT:
            view = GameOverView()
            self.window.show_view(view)


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
