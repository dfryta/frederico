import vars
from bearlibterminal import terminal

class GUI(object):

    def __init__(self, player):
        self.player = player

    def draw(self):
        x = vars.FIELDS_WIDTH * vars.FIELDS_X_SPACING
        # Name
        terminal.layer(vars.MAP_LAYER)
        terminal.printf(x, 1, self.player.name)
        terminal.printf(x, 2, "-" * 28)
        # Class and level
        terminal.printf(x + 5, 3, "{0} (level {1})".format(self.player.role, self.player.level))
        terminal.printf(x, 4, "-" * 28)
        # Stats
        terminal.printf(x, 5,  "HP: {0}".format(self.player.hp))
        terminal.printf(x, 6,  "MP: {0}".format(self.player.mana))
        terminal.printf(x, 8,  "STR: {0}".format(self.player.strength))
        terminal.printf(x, 9,  "AGI: {0}".format(self.player.agility))
        terminal.printf(x, 10, "STA: {0}".format(self.player.stamina))
        terminal.printf(x, 11, "INT: {0}".format(self.player.intellect))
        # Exp
        terminal.printf(x, 13, "EXP: {0} (next LVL: {1})".format(self.player.exp, self.player.next_level_exp))
        terminal.printf(x, 14, "-" * 28)
