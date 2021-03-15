import arcade as ac
from random import randint, randrange, choice


class Platform(ac.Sprite):
    textures_pattern = []
    super_platform_texture = None
    teleportation_platform_texture = None
    reverse_platform_texture = None

    def __init__(self, game: ac.View, center_x=None):
        self.game = game
        self.window = game.window

        super(Platform, self).__init__()

        self.score_points = 1
        self.can_generate = True

        if center_x is None:
            x_0 = int(self.game.platforms[-1].left - 400)
            x_1 = int(self.game.platforms[-1].right + 400)
            self.center_x = randint(x_0, x_1)
        else:
            self.center_x = center_x
        self.center_y = self.game.offset_y - self.window.height // 5

    def on_update(self, delta_time: float = 1 / 60):
        self.position = [self._position[0] + self.change_x, self._position[1] + self.change_y]
        self.angle += self.change_angle

        if self.bottom >= self.window.get_viewport()[3]:
            self.game.platforms.remove(self)

            if self.can_generate:
                Platform.generate_platform(self.game)

        self.update()

    def update(self):
        pass

    @staticmethod
    def generate_platform(game: ac.View):
        percent = randrange(100)

        if percent < 40:
            game.platforms.append(BasicPlatform(game))
        elif 40 <= percent < 60:
            game.platforms.append(LeanedPlatform(game))
        elif 60 <= percent < 65:
            game.platforms.append(RotatingPlatform(game))
        elif 65 <= percent < 70:
            game.platforms.append(TeleportationPlatform(game))
        elif 70 <= percent < 90:
            game.platforms.append(MovingPlatform(game))
        elif 90 <= percent < 100:
            game.platforms.append(SuperPlatform(game))
            game.platforms.append(BasicPlatform(game))

    @staticmethod
    def init_textures(window: ac.Window):
        for i in range(11):
            Platform.textures_pattern.append(ac.SpriteSolidColor(width=100 + 10 * i, height=window.height // 50,
                                                                 color=(255, 0, 0)).texture)

        Platform.super_platform_texture = ac.SpriteSolidColor(width=50, height=window.height // 50,
                                                              color=(224, 246, 41)).texture
        Platform.teleportation_platform_texture = ac.SpriteSolidColor(width=100, height=window.height // 50,
                                                                      color=(0, 0, 255)).texture
        Platform.reverse_platform_texture = ac.SpriteSolidColor(width=100, height=window.height // 50,
                                                                color=(0, 0, 255)).texture


class BasicPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View, center_x=None):
        super(BasicPlatform, self).__init__(game, center_x=center_x)
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

        if self in self.game.colliding_platforms:
            self.game.ball.center_x += self.change_x


class LeanedPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(LeanedPlatform, self).__init__(game)
        self.texture = Platform.textures_pattern[randint(0, 5)]
        self.angle = 45 * choice((-1, 1))


class RotatingPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(RotatingPlatform, self).__init__(game)
        self.texture = Platform.textures_pattern[randint(0, 5)]
        self.change_angle = 4 * choice((-1, 1))


class TeleportationPlatform(Platform, ac.Sprite):
    def __init__(self, game: ac.View):
        super(TeleportationPlatform, self).__init__(game)
        self.texture = Platform.teleportation_platform_texture

    def update(self):
        if self in self.game.colliding_platforms:
            platform = self.game.platforms[-2]
            new_platform = BasicPlatform(self.game, center_x=platform.center_x)
            new_platform.center_y = platform.center_y

            self.game.platforms.insert(-2, new_platform)
            self.game.platforms.remove(platform)

            self.game.ball.center_x = new_platform.center_x
            self.game.ball.bottom = new_platform.top

