import arcade as ac
from arcade.experimental.camera import Camera2D
import Game
import Menu
from cryptography.fernet import Fernet
import json

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "FallingBall by LoupioFR"


class FallingBall(ac.Window):
    def __init__(self):
        super(FallingBall, self).__init__(title=WINDOW_TITLE, width=960, height=540)

        # loading settings
        with open("settings.json") as file:
            self.settings = json.loads(file.read())
        if self.settings["full_screen"]:
            self.set_fullscreen()
        else:
            self.maximize()
        # init encrypter : yes you can see this key... but it's...
        self.encrypter = Fernet("y3pEb-6qmTIkpl8Tx5tjw_eIj6qKseV3yQE20PhO9D4=".encode())

        # creating main camera
        self.camera = Camera2D(
            viewport=(0, 0, self.width, self.height),
            projection=(0, 1920, 0, 1080)
        )

        self.CURSOR = self._mouse_cursor

        # creating views
        self.menu = Menu.Menu(self, self.camera)
        self.game = Game.Game(self, self.camera)

        self.show_menu()

    def show_game(self):
        self.set_mouse_visible(False)
        self.show_view(self.game)

    def show_menu(self):
        self.set_mouse_visible(True)
        self.show_view(self.menu)

    def on_resize(self, width: float, height: float):
        self.camera.viewport = (0, 0, width, height)

    def set_setting(self, key: str, value: bool or int):
        self.settings[key] = value

    def on_close(self):
        # saving settings
        with open("settings.json", "w") as file:
            file.write(json.dumps(self.settings))
        self.close()


if __name__ == '__main__':
    app = FallingBall()
    ac.run()
