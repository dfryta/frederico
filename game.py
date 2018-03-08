import world
import vars
import player
import gui
from bearlibterminal import terminal

class Game(object):

    def __init__(self):
        self.world = world.World(50, 50)
        self.player = player.Player("Jamie", self.world)
        self.gui = gui.GUI(self.player)
        terminal.open()
        terminal.set("window: title='Frederico', size={0}x{1}".format(vars.CONSOLE_WIDTH, vars.CONSOLE_HEIGHT))
        terminal.set("0xE000: resources/materials.png, size=16x16, resize=32x32, spacing=2x1")
        self.game_loop()
        self.quit = False

    def update(self):
        self.player.update()
        for e in self.world.enemies:
            e.update()

    def draw(self):
        terminal.clear()
        self.world.draw()
        self.player.draw()
        self.gui.draw()
        terminal.refresh()

    def game_loop(self):
        self.draw()
        while True:
            self.update()
            self.draw()
            if vars.QUIT:
                break
        terminal.close()