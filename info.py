import vars
from bearlibterminal import terminal

class InfoBar(object):

    def __init__(self):
        self.messages = list()

    def update(self):
        pass

    def draw(self):
        y = vars.FIELDS_HEIGHT * vars.FIELDS_Y_SPACING
        terminal.layer(vars.UNIT_LAYER)
        for idx, msg in enumerate(self.messages[-5:]):
            terminal.printf(2, y + idx, msg)

    def add_message(self, message, type):
        self.messages.append("[color={0}]{1}".format(type, message))

