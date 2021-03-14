import arcade as ac
import Game

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "FallingBall by LoupioFR"


class FallingBall(ac.Window):
    def __init__(self):
        super(FallingBall, self).__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
        self.set_fullscreen()

    def show_game(self):
        self.show_view(Game.Game(self))


if __name__ == '__main__':
    app = FallingBall()
    app.show_game()
    ac.run()
