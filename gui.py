import vars
from bearlibterminal import terminal

class GUI(object):

    def __init__(self, player):
        self.player = player

    def draw(self):
        x = vars.FIELDS_WIDTH * vars.FIELDS_X_SPACING
        y = vars.FIELDS_HEIGHT * vars.FIELDS_Y_SPACING
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

        # Character

        terminal.printf(x, 15, "Equipment")

        # Head
        terminal.layer(vars.MAP_LAYER)
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75), 18, 0xE5F7)

        # Chest
        #terminal.printf(x + int((vars.CONSOLE_WIDTH - x) / 2 - 1), 19, "Chest")
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75), 21, 0xE5F7)

        # Right hand
        # terminal.printf(x + int((vars.CONSOLE_WIDTH - x) / 2 - 1), 19, "Right hand")
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75) - int(vars.FIELDS_X_SPACING * 1.5), 21, 0xE5F7)

        # Left hand
        # terminal.printf(x + int((vars.CONSOLE_WIDTH - x) / 2 - 1), 19, "Left Hand")
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75) + int(vars.FIELDS_X_SPACING * 1.5), 21, 0xE5F7)

        # Boots
        # terminal.printf(x + int((vars.CONSOLE_WIDTH - x) / 2 - 1), 23, "Legs")
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75), 24, 0xE5F7)

        # Boots
        #terminal.printf(x + int((vars.CONSOLE_WIDTH - x) / 2 - 1), 23, "Boots")
        terminal.put(x + int((vars.CONSOLE_WIDTH - x) / 1.75), 27, 0xE5F7)

        terminal.printf(x, 29, "-" * 28)

        # Backpack
        terminal.printf(x, 30, "Backpack")

        for i in range(5):
            terminal.put(x + 2 + i * vars.FIELDS_X_SPACING + i * 1, 32, 0xE506)
            terminal.put(x + 2 + i * vars.FIELDS_X_SPACING + i * 1, 35, 0xE506)
            terminal.put(x + 2 + i * vars.FIELDS_X_SPACING + i * 1, 38, 0xE506)

        # InfoBar top
        terminal.put(1, y, 0xE5BA)
        for i in range(1, 15):
            terminal.put(1 + i * vars.FIELDS_X_SPACING, y, 0xE5BB)
        terminal.put(1 + 15 * vars.FIELDS_X_SPACING, y, 0xE5BC)
        # InfoBar middle
        terminal.put(1, y + vars.FIELDS_Y_SPACING, 0xE5F3)
        for i in range(1, 15):
            terminal.put(1 + i * vars.FIELDS_X_SPACING, y + vars.FIELDS_Y_SPACING, 0xE5F4)
        terminal.put(1 + 15 * vars.FIELDS_X_SPACING, y + vars.FIELDS_Y_SPACING, 0xE5F5)
        # InfoBar bottom
        terminal.put(1, y + 2 * vars.FIELDS_Y_SPACING, 0xE62C)
        for i in range(1, 15):
            terminal.put(1 + i * vars.FIELDS_X_SPACING, y + 2 * vars.FIELDS_Y_SPACING, 0xE62D)
        terminal.put(1 + 15 * vars.FIELDS_X_SPACING, y + 2 * vars.FIELDS_Y_SPACING, 0xE62E)