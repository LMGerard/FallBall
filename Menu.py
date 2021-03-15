import arcade as ac
import json
from cryptography.fernet import InvalidToken


class Menu(ac.View):
    def __init__(self, window):
        super(Menu, self).__init__(window=window)
        self.elements = ac.SpriteList()
        self.play_button = PlayButton(self.window)
        self.quit_button = QuitButton(self.window)

        self.elements.append(self.play_button)
        self.elements.append(self.quit_button)

        with open("scores.json", "r") as file:
            file = json.loads(file.read())
            data = []
            for index, value in enumerate(file):
                try:
                    data.append(list(map(lambda x: float(self.window.encrypter.decrypt(x.encode()).decode()), value)))
                except InvalidToken:
                    pass
        data = sorted(data, key=lambda x: x[0] * x[1])[::-1]
        self.scores = "\n".join([f"{int(points)}|{time}|{round(points * time / 10, 3)}" for points, time in data[:10]])

    def on_update(self, delta_time: float):
        self.elements.update()

    def on_draw(self):
        ac.start_render()
        self.window.set_viewport(0, self.window.width, 0, self.window.height)

        self.elements.draw()
        self.play_button.draw()
        self.quit_button.draw()

        ac.draw_text(f"POINTS|TIME|SCORE", color=(0, 0, 0), start_x=self.window.width // 2,
                     start_y=self.window.height * 3 // 8, anchor_y="top",
                     anchor_x="center", font_size=20)
        ac.draw_text(f"\n{self.scores}", color=(0, 0, 0), start_x=self.window.width // 2,
                     start_y=self.window.height * 3 // 8, anchor_y="top",
                     anchor_x="center", font_size=20)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.play_button.collides_with_point((x, y)):
            self.play_button.click()
        elif self.quit_button.collides_with_point((x, y)):
            self.quit_button.click()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == ac.key.ENTER:
            self.play_button.click(hiding_speed=100)


class PlayButton(ac.SpriteCircle):
    def __init__(self, window: ac.Window):
        self.window = window
        super(PlayButton, self).__init__(radius=self.window.height // 2, color=(255, 255, 0))
        self.position = self.window.width // 2, self.window.height // 2
        self.hiding_speed = 20
        self.activated = False

    def draw(self):
        ac.draw_text("PLAY", start_x=self.center_x, start_y=self.center_y, anchor_x="center", anchor_y="center",
                     color=(0, 0, 0), font_size=100)

    def update(self):
        if self.activated:
            self.height -= self.hiding_speed
            self.width -= self.hiding_speed

            if self.height <= 30:
                self.window.show_game()

    def click(self, hiding_speed=20):
        self.activated = True
        self.hiding_speed = hiding_speed


class QuitButton(ac.SpriteCircle):
    def __init__(self, window: ac.Window):
        self.window = window
        super(QuitButton, self).__init__(radius=self.window.height // 50, color=(255, 255, 0))
        self.position = self.window.width - self.width, self.window.height - self.height

    def draw(self):
        ac.draw_text("X", start_x=self.center_x, start_y=self.center_y, anchor_x="center", anchor_y="center",
                     color=(0, 0, 0), font_size=20)

    def click(self):
        self.window.close()
