import arcade as ac


class Menu(ac.View):
    def __init__(self, window):
        super(Menu, self).__init__(window=window)
        self.elements = ac.SpriteList()
        self.play_button = PlayButton(self.window)
        self.elements.append(self.play_button)

    def on_update(self, delta_time: float):
        self.elements.update()

    def on_draw(self):
        ac.start_render()
        self.elements.draw()
        self.play_button.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.play_button.collides_with_point((x,y)):
            self.play_button.click()


class PlayButton(ac.SpriteCircle):
    def __init__(self, window: ac.Window):
        self.window = window
        super(PlayButton, self).__init__(radius=self.window.height // 2, color=(255, 255, 0))
        self.position = self.window.width // 2, self.window.height // 2

        self.activated = False

    def draw(self):
        ac.draw_text("PLAY", start_x=self.center_x, start_y=self.center_y, anchor_x="center", anchor_y="center",
                     color=(0, 0, 0), font_size=100)

    def update(self):
        if self.activated:
            self.height -= 20
            self.width -= 20

            if self.height <= 30:
                self.window.show_game()

    def click(self):
        self.activated = True