import arcade as ac
from arcade.experimental.camera import Camera2D
from time import time
import Platforms
import json


class Game(ac.View):
    def __init__(self, window: ac.Window, camera: Camera2D):
        super(Game, self).__init__(window=window)
        self.camera = camera

        Platforms.Platform.init_textures(width=1920, height=1080)
        self.last_score = self.score = self.is_paused = self.platforms = self.colliding_platforms = self.ball = self.timer = None

    def on_show_view(self):
        # reset camera
        self.camera.projection = (0, 1920, 0, 1080)
        self.camera.scroll = (0, 0)

        self.last_score = -1
        self.score = 0
        self.is_paused = False
        self.platforms = ac.SpriteList()
        self.colliding_platforms = ac.SpriteList()
        self.ball = Ball(self)

        # init timer
        self.timer = 0

        # load initial platforms
        platform = Platforms.BasicPlatform(self, center_x=960)
        platform.center_y = 0

        self.platforms.append(platform)

        for i in range(1, 6):
            platform = Platforms.BasicPlatform(self)
            platform.center_y = - 216 * i

            self.platforms.append(platform)

    def on_update(self, delta_time: float):
        if not self.is_paused:
            self.timer += delta_time
            self.platforms.on_update(delta_time)

            if not self.ball.update():
                return

            self.colliding_platforms = self.ball.physic_engine.update()

            for platform in self.colliding_platforms:
                if platform.score_points > 0:
                    if self.last_score + 1 == self.score or self.last_score + 5 == self.score:
                        self.last_score = self.score

                        self.score += platform.score_points
                        platform.score_points = 0
                    else:
                        self.window.close()

            self.camera.scroll_y -= 3 + self.timer // 10
            self.camera.scroll_x = self.ball.center_x - 960

    def on_draw(self):
        ac.start_render()
        self.camera.use()
        self.platforms.draw()
        self.ball.draw()

        ac.draw_text(f"{self.score}\n{round(self.timer, 2)}",
                     start_x=self.camera.scroll_x,
                     start_y=self.camera.scroll_y + 1080, anchor_x="left", anchor_y="top",
                     color=(255, 0, 0), font_size=30)

        if self.ball.center_y - self.camera.scroll_y > 810:
            alpha = self.ball.center_y - self.camera.scroll_y - 810

            ac.draw_rectangle_filled(center_x=self.camera.scroll_x + 1080 // 2,
                                     center_y=self.camera.scroll_y + 1080 // 2,
                                     width=1920,
                                     height=1080, color=(255, 0, 0, alpha * 0.7))
        if self.is_paused:
            ac.draw_rectangle_filled(center_x=self.camera.scroll_x + 960,
                                     center_y=self.camera.scroll_y + 540,
                                     width=1920,
                                     height=1080, color=(255, 255, 255, 100))
            ac.draw_text("PAUSE", start_x=self.camera.scroll_x + 960,
                         start_y=self.camera.scroll_y + 540, anchor_x="center",
                         anchor_y="center", color=(255, 255, 255), font_size=60)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == ac.key.RIGHT:
            self.ball.right_move = True
        elif symbol == ac.key.LEFT:
            self.ball.left_move = True
        elif (symbol == ac.key.SPACE or symbol == ac.key.UP) and self.ball.physic_engine.can_jump():
            self.ball.physic_engine.jump(15)
        elif symbol == ac.key.ESCAPE:
            self.is_paused = not self.is_paused

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == ac.key.RIGHT:
            self.ball.right_move = False
        elif _symbol == ac.key.LEFT:
            self.ball.left_move = False


class Ball(ac.SpriteCircle):
    speed = 10

    def __init__(self, game: Game):
        self.game = game
        self.window = game.window

        super(Ball, self).__init__(color=(255, 255, 0), radius=15)
        self.position = 960, 540

        self.left_move, self.right_move = False, False
        self.physic_engine = ac.PhysicsEnginePlatformer(self, game.platforms, 1)

    def update(self):
        self.change_x = self.right_move * self.speed - self.left_move * self.speed

        if self.bottom >= 1080 - self.game.camera.scroll_y or self.top <= self.game.camera.scroll_y:
            with open("scores.json", "r") as file:
                data = json.loads(file.read())

                encrypted_score = self.window.encrypter.encrypt(str(self.game.score).encode()).decode()
                encrypted_time = self.window.encrypter.encrypt(
                    str(round(self.game.timer, 3)).encode()).decode()

                data.append((encrypted_score, encrypted_time))
            with open("scores.json", "w") as file:
                file.write(json.dumps(data))
            self.window.show_menu()
            return False
        return True
