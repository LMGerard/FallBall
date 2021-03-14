import arcade as ac
from random import randint, randrange, choice


class Platform(ac.Sprite):
    speed = 2
    textures_pattern = []
    super_platform_texture = None

    def __init__(self, game: ac.View):
        self.game = game
        self.window = game.window

        super(Platform, self).__init__()

        self.score_points = 1
        self.can_generate = True

        x_0 = int(max(self.game.ball.left - 300, self.width // 2))
        x_1 = int(min(self.game.ball.right + 300, self.window.width - self.width // 2))
        self.center_x = randint(x_0, x_1)

        self.change_y = Platform.speed

    def on_update(self, delta_time: float = 1 / 60):
        self.position = [self._position[0] + self.change_x, self._position[1] + self.change_y]

        if self.bottom >= self.window.height:
            self.game.platforms.remove(self)

            if self.can_generate:
                Platform.generate_platform(self.game)

        self.update()

    def update(self):
        pass

    @staticmethod
    def generate_platform(game: ac.View):
        percent = randrange(100)

        if percent < 50:
            game.platforms.append(BasicPlatform(game))
        elif 50 <= percent < 70:
            game.platforms.append(LeanedPlatform(game))
        elif 70 <= percent < 90:
            game.platforms.append(MovingPlatform(game))
        elif 90 <= percent < 100:
            game.platforms.append(BasicPlatform(game))
            game.platforms.append(SuperPlatform(game))

    @staticmethod
    def init_textures(window: ac.Window):
        for i in range(11):
            Platform.textures_pattern.append(ac.SpriteSolidColor(width=100 + 10 * i, height=window.height // 50,
                                                                 color=(255, 0, 0)).texture)

        Platform.super_platform_texture = ac.SpriteSolidColor(width=50, height=window.height // 50,
                                                              color=(224, 246, 41)).texture


class BasicPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(BasicPlatform, self).__init__(game)
        self.texture = Platform.textures_pattern[randint(0, 10)]


class SuperPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(SuperPlatform, self).__init__(game)
        self.texture = Platform.super_platform_texture
        self.score_points = 5
        self.can_generate = False


class MovingPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(MovingPlatform, self).__init__(game)
        self.texture = Platform.textures_pattern[randint(0, 10)]

        self.change_x = choice((-1, 1))
        self.min_x, self.max_x = self.left - 100, self.right + 100

    def update(self):
        if self.left <= self.min_x or self.right >= self.max_x:
            self.change_x *= -1

        if self.collides_with_sprite(self.game.ball):
            self.game.ball.center_x += self.change_x


class LeanedPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(LeanedPlatform, self).__init__(game)
        self.texture = Platform.textures_pattern[randint(0, 5)]
        self.angle = 45 * choice((-1, 1))
