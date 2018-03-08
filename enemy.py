import random
import vars
from bearlibterminal import terminal

class Enemy(object):

    HP = 0
    DAMAGE = 2
    MOVE = 1

    IMAGE = 0
    ALERT_IMAGE = 0x224

    def __init__(self, world, x = 0, y = 0):

        self.hp = type(self).HP
        self.damage = type(self).DAMAGE

        self.world = world
        self.position_x = x
        self.position_y = y
        if x == y == 0:
            self.spawn()
        self.move_points = type(self).MOVE
        self.image = type(self).IMAGE
        self.alert_image = type(self).ALERT_IMAGE

        self.alerted = False

    def get_coordinates(self):
        return self.position_x, self.position_y

    def spawn(self):
        while True:
            # Randomize staring position
            x, y = random.randint(0, self.world.width - 1), random.randint(0, self.world.height - 1)
            # Check if position is in bounds of dungeon
            if self.world.is_field_available(x, y):
                self.position_x = x
                self.position_y = y
                self.world.enemies.append(self)
                return

    def pathfinding(self, x, y):
        # Try estimate shortest way to player
        # Basic version
        possible_actions = list()
        if self.position_x < x:
            possible_actions.append(2) # Go right
        if self.position_x > x:
            possible_actions.append(4) # Go left
        if self.position_y > y:
            possible_actions.append(1) # Go up
        if self.position_y < y:
            possible_actions.append(3) # Go down
        # print(possible_actions)
        return random.choice(possible_actions)

    def move(self):
        # 0 - stay
        # 1 - go up
        # 2 - go right
        # 3 - go down
        # 4 - go left
        counter = 0
        while True:
            if self.alerted:
                player_x, player_y = self.world.player.get_coordinates()
                move = self.pathfinding(player_x, player_y)
                # In case of stuck
                if counter > 5:
                    move = 0
            else:
                # IF NOT ALERTED (player is not in visible range) - move randomly here and there
                move = random.randint(0, 5)
            if move == 0:
                break
            if move == 1:
                if self.world.is_field_available(self.position_x, self.position_y - 1):
                    self.position_y -= 1
                    break
            if move == 2:
                if self.world.is_field_available(self.position_x + 1, self.position_y):
                    self.position_x += 1
                    break
            if move == 3:
                if self.world.is_field_available(self.position_x, self.position_y + 1):
                    self.position_y += 1
                    break
            if move == 4:
                if self.world.is_field_available(self.position_x - 1, self.position_y):
                    self.position_x -= 1
                    break
            counter += 1


    def is_alerted(self):
        if self.world.calculate_distance(self.world.player.get_coordinates(), self.get_coordinates()) < 6:
            self.alerted = True
        else:
            self.alerted = False

    def update(self):
        self.move()
        self.is_alerted()



    def draw(self):
        # Draw enemy
        if self.world.is_currently_visible(self.position_x, self.position_y):
            terminal.layer(vars.UNIT_LAYER)
            terminal.put(self.world.calculate_draw_x_coordinate(self.position_x),
                         self.world.calculate_draw_y_coordinate(self.position_y),
                         0xE000 + self.image
            )
            terminal.layer(vars.EFFECTS_LAYER)
            if self.alerted:
                terminal.put(self.world.calculate_draw_x_coordinate(self.position_x),
                             self.world.calculate_draw_y_coordinate(self.position_y),
                             0xE000 + self.alert_image
                             )



class Goblin(Enemy):

    HP = random.randint(8, 12)
    DAMAGE = random.randint(2, 3)
    IMAGE = 0x792