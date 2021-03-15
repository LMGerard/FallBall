import arcade as ac
import Game
import Menu
import json
from cryptography.fernet import Fernet

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "FallingBall by LoupioFR"


class FallingBall(ac.Window):
    def __init__(self):
        super(FallingBall, self).__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
        self.set_fullscreen()

        self.encrypter = Fernet("y3pEb-6qmTIkpl8Tx5tjw_eIj6qKseV3yQE20PhO9D4=".encode())

        self.CURSOR = self._mouse_cursor

    def show_game(self):
        self.set_mouse_visible(False)
        self.set_viewport(0, self.width, 0, self.height)
        self.show_view(Game.Game(self))

    def show_menu(self):
        self.set_mouse_visible(True)
        self.show_view(Menu.Menu(self))


if __name__ == '__main__':
    app = FallingBall()
    app.show_menu()
    ac.run()
