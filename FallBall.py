import arcade as ac
from arcade.experimental.camera import Camera2D
import Game
import Menu
from cryptography.fernet import Fernet

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "FallingBall by LoupioFR"


class FallingBall(ac.Window):
    def __init__(self):
        super(FallingBall, self).__init__(title=WINDOW_TITLE, resizable=True)
        self.maximize()
        # yes you can see this key... but it's...
        self.encrypter = Fernet("y3pEb-6qmTIkpl8Tx5tjw_eIj6qKseV3yQE20PhO9D4=".encode())
        self.camera = Camera2D(
            viewport=(0, 0, self.width, self.height),
            projection=(0, 1920, 0, 1080)
        )
        self.CURSOR = self._mouse_cursor

        self.menu = Menu.Menu(self, self.camera)
        self.game = Game.Game(self, self.camera)

        self.show_menu()

    def show_game(self):
        self.set_mouse_visible(False)
        self.show_view(self.game)

    def show_menu(self):
        self.camera.scroll = (0, 0)
        self.set_mouse_visible(True)
        self.show_view(self.menu)

    def on_resize(self, width: float, height: float):
        self.camera.viewport = (0, 0, width, height)


if __name__ == '__main__':
    app = FallingBall()
    ac.run()
