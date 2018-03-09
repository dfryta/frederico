import world
import vars
import player
import gui
import info
import time
from bearlibterminal import terminal

class Game(object):

    def __init__(self):
        self.info = info.InfoBar()
        self.world = world.World(50, 50, self.info)
        self.player = player.Player("Frederico", self.world)
        self.world.create_enemies()
        self.gui = gui.GUI(self.player)
        terminal.open()
        terminal.set("window: title='Frederico', size={0}x{1}".format(vars.CONSOLE_WIDTH, vars.CONSOLE_HEIGHT))
        terminal.set("0xE000: resources/materials.png, size=16x16, resize=32x32, spacing=2x1")
        self.game_loop()
        self.quit = False

    def update(self):
        self.player.update()
        if not self.player.died:
            for e in self.world.enemies:
                e.update()
        if self.player.restart:
            self.info = info.InfoBar()
            self.world = world.World(50, 50, self.info, seed=time.time())
            self.player = player.Player("Frederico", self.world)
            self.world.create_enemies()
            self.gui = gui.GUI(self.player)

    def draw(self):
        terminal.clear()
        self.world.draw()
        self.player.draw()
        self.gui.draw()
        self.info.draw()
        terminal.refresh()

    def game_loop(self):
        self.draw()
        while True:
            self.update()
            self.draw()
            if vars.QUIT:
                break
        terminal.close()