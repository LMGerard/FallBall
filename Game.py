import arcade as ac
from random import randint, randrange, choice
import Platforms


class Game(ac.View):
    def __init__(self, window: ac.Window):
        super(Game, self).__init__(window=window)
        self.score = 0
        self.is_paused = False
        self.platforms = ac.SpriteList()

        Platforms.Platform.init_textures(self.window)

        self.ball = Ball(self)

        self.setup()

    def setup(self):
        platform = Platforms.BasicPlatform(self)

        platform.center_x = self.window.width // 2

        self.platforms.append(platform)

        for i in range(1, 5):
            platform = Platforms.BasicPlatform(self)

            platform.center_y = - self.window.height // 5 * i

            self.platforms.append(platform)

    def on_update(self, delta_time: float):
        if not self.is_paused:
            self.ball.update()
            self.platforms.on_update(delta_time)

            for platform in self.ball.collides_with_list(self.platforms):
                if platform.score_points > 0:
                    self.score += platform.score_points
                    platform.score_points = 0

            Platforms.Platform.speed = 2 + 0.1 * (self.score // 20)

    def on_draw(self):
        ac.start_render()
        self.platforms.draw()
        self.ball.draw()

        ac.draw_text(f"{self.score}", start_x=0, start_y=self.window.height, anchor_x="left", anchor_y="top",
                     color=(255, 0, 0), font_size=30)
        if self.is_paused:
            ac.draw_rectangle_filled(center_x=self.window.width // 2, center_y=self.window.height // 2,
                                     width=self.window.width,
                                     height=self.window.height, color=(255, 255, 255, 100))
            ac.draw_text("PAUSE", start_x=self.window.width // 2, start_y=self.window.height // 2, anchor_x="center",
                         anchor_y="center", color=(255, 255, 255), font_size=60)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == ac.key.RIGHT:
            self.ball.right_move = True
        elif symbol == ac.key.LEFT:
            self.ball.left_move = True
        elif (symbol == ac.key.SPACE or symbol == ac.key.UP) and self.ball.physic_engine.can_jump():
            self.ball.physic_engine.jump(20)
        elif symbol == ac.key.ESCAPE:
            self.is_paused = not self.is_paused

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == ac.key.RIGHT:
            self.ball.right_move = False
        elif _symbol == ac.key.LEFT:
            self.ball.left_move = False


class Ball(ac.Sprite):
    speed = 10

    def __init__(self, game: Game):
        self.game = Game
        self.window = game.window

        super(Ball, self).__init__(filename="assets/game/ball.png", scale=0.05, center_x=self.window.width // 2,
                                   center_y=self.window.height // 2)
        self.left_move, self.right_move = False, False
        self.physic_engine = ac.PhysicsEnginePlatformer(self, game.platforms, 1)

    def update(self):
        self.physic_engine.update()

        self.change_x = self.right_move * self.speed - self.left_move * self.speed

        if self.bottom >= self.window.height or self.top <= 0:
            self.window.show_game()
