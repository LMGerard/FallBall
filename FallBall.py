import arcade as ac
import Game
import Menu

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "FallingBall by LoupioFR"


class FallingBall(ac.Window):
    def __init__(self):
        super(FallingBall, self).__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
        self.set_fullscreen()

        self.CURSOR = self._mouse_cursor

    def show_game(self):
        self.set_mouse_visible(False)
        self.set_viewport(0, self.width, 0, self.height)
        self.show_view(Game.Game(self))

    def show_menu(self):
        self.set_mouse_visible(True)
        self.set_viewport(0, self.width, 0, self.height)
        self.show_view(Menu.Menu(self))


if __name__ == '__main__':
    app = FallingBall()
    app.show_menu()
    ac.run()
