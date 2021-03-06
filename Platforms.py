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
            x_0 = int(self.game.platforms[-1].left - 350)
            x_1 = int(self.game.platforms[-1].right + 350)
            self.center_x = randint(x_0, x_1)
        else:
            self.center_x = center_x
        self.center_y = self.game.camera.scroll_y - 216

    def on_update(self, delta_time: float = 1 / 60):
        self.position = [self._position[0] + self.change_x, self._position[1] + self.change_y]
        self.angle += self.change_angle

        if self.bottom >= 1080 + self.game.camera.scroll_y:
            self.game.platforms.remove(self)

            if self.can_generate:
                Platform.generate_platform(self.game)

        self.update()

    def update(self):
        pass

    @staticmethod
    def generate_platform(game: ac.View):
        percent = randrange(100)
        platform = None
        if percent < 40:
            platform = BasicPlatform(game)
        elif 40 <= percent < 60:
            platform = LeanedPlatform(game)
        elif 60 <= percent < 65:
            platform = RotatingPlatform(game)
        elif 65 <= percent < 70:
            platform = TeleportationPlatform(game)
        elif 70 <= percent < 90:
            platform = MovingPlatform(game)
        elif 90 <= percent < 100:
            game.platforms.append(SuperPlatform(game))
            platform = BasicPlatform(game)

        TeleportationPlatform.goal_platform = game.platforms[-1]
        game.platforms.append(platform)

    @staticmethod
    def init_textures(width: int, height: int):
        for i in range(11):
            Platform.textures_pattern.append(ac.SpriteSolidColor(width=100 + 10 * i, height=height // 50,
                                                                 color=(255, 0, 0)).texture)

        Platform.super_platform_texture = ac.SpriteSolidColor(width=50, height=height // 50,
                                                              color=(224, 246, 41)).texture
        Platform.teleportation_platform_texture = ac.SpriteSolidColor(width=100, height=height // 50,
                                                                      color=(0, 0, 255)).texture
        Platform.reverse_platform_texture = ac.SpriteSolidColor(width=100, height=height // 50,
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
    goal_platform = None

    def __init__(self, game: ac.View):
        super(TeleportationPlatform, self).__init__(game)
        self.texture = Platform.teleportation_platform_texture

    def update(self):
        if self in self.game.colliding_platforms:
            if TeleportationPlatform.goal_platform.center_y < self.game.camera.scroll_y:
                return
            index = self.game.platforms.index(TeleportationPlatform.goal_platform)

            new_platform = BasicPlatform(self.game, center_x=TeleportationPlatform.goal_platform.center_x)
            new_platform.center_y = TeleportationPlatform.goal_platform.center_y

            self.game.platforms.insert(index, new_platform)
            self.game.platforms.remove(TeleportationPlatform.goal_platform)

            self.game.ball.center_x = new_platform.center_x
            self.game.ball.bottom = new_platform.top
