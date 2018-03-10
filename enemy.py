import random
import vars
from bearlibterminal import terminal

class Enemy(object):

    NAME = "Enemy"

    HP = 0
    DAMAGE = 2
    MOVE = 1

    ATTACK_RANGE = 1 # Melee

    DETECT_RANGE = 4

    IMAGE = 0
    ALERT_IMAGE = 0x224

    def __init__(self, world, x = 0, y = 0, level=1):

        self.hp = type(self).HP
        self.damage = type(self).DAMAGE

        self.level = level
        self.world = world
        self.position_x = x
        self.position_y = y
        if x == y == 0:
            self.spawn()
        self.move_points = type(self).MOVE
        self.image = type(self).IMAGE
        self.alert_image = type(self).ALERT_IMAGE
        self.attack_range = type(self).ATTACK_RANGE
        self.name = type(self).NAME
        self.detect_range = type(self).DETECT_RANGE

        self.alerted = False
        self.took_damage = 0

    def update(self):
        if not self.check_if_died():
            self.search_enemy()
            if self.is_enemy_in_range():
                self.attack()
            else:
                self.move()

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
        if self.took_damage:
            terminal.layer(vars.EFFECTS_LAYER)
            terminal.put(self.world.calculate_draw_x_coordinate(self.position_x),
                         self.world.calculate_draw_y_coordinate(self.position_y),
                         0xE549
                         )
            terminal.layer(vars.LABEL_ON_EFFECTS_LAYER)
            terminal.printf(self.world.calculate_draw_x_coordinate(self.position_x),
                         self.world.calculate_draw_y_coordinate(self.position_y),
                         "[color=crimson]{0}".format(self.took_damage)
                        )
            # Reset took damage meter
            self.took_damage = 0

    """ <---------------- ### ---------------->"""

    def check_if_died(self):
        if self.hp <= 0:
            self.world.info.add_message("{0} died!".format(self.name), vars.INFOBAR_DEFAULT)
            self.world.enemies.remove(self)
            self.world.corpses.append(self.get_coordinates())
            del self
            return True
        return False


    def attack(self):
        if self.get_hit():
            critical = self.get_critical()
            total_damage = self.get_total_damage() * 2 if critical else self.get_total_damage()
            self.world.player.take_damage(total_damage, self.name)
            self.world.info.add_message("You are {0} by a {2} for {1} damage!".format("critical hit" if critical else "hit", total_damage, self.name), vars.INFOBAR_DAMAGE)
        else:
            pass

    def get_hit(self):
        # Base hit is 80% plus 5% each level difference between enemy and player
        hit_chance = vars.ENEMY_DEFAULT_HIT_CHANCE + (0.05 * (self.level - self.world.player.level))
        r = random.random()
        msg = "{0} attack with fierce! ".format(self.name, hit_chance , r)
        if r <= hit_chance:
            hit = True
            msg += "HIT!"
        else:
            hit = False
            msg += "MISSED!"
        self.world.info.add_message(msg, vars.INFOBAR_DAMAGE)
        return hit

    def get_critical(self):
        # Critical chance is 5% and increase 5% each level difference
        critical_hit_chance = vars.ENEMY_DEFAULT_CRITICAL_HIT_CHANCE + (0.05 * (self.level - self.world.player.level))
        return random.random() <= critical_hit_chance

    def get_total_damage(self):
        return self.damage

    def get_coordinates(self):
        return self.position_x, self.position_y

    def is_enemy_in_range(self):
        return self.world.calculate_distance(self.get_coordinates(), self.world.player.get_coordinates()) <= self.attack_range

    def spawn(self):
        while True:
            # Randomize staring position
            x, y = random.randint(0, self.world.width - 1), random.randint(0, self.world.height - 1)
            # Check if position is in bounds of dungeon
            if self.world.is_field_available(x, y) and self.world.calculate_distance((x, y), self.world.player.get_coordinates()) > 10:
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


    def search_enemy(self):
        if self.world.calculate_distance(self.world.player.get_coordinates(), self.get_coordinates()) < self.detect_range:
            if not self.alerted:
                self.world.info.add_message("You were spotted by {0}!".format(self.name), vars.INFOBAR_LOOT_MESSAGE)
                self.alerted = True
        else:
            if self.alerted:
                self.world.info.add_message("You have escaped {0}!".format(self.name), vars.INFOBAR_LOOT_MESSAGE)
            self.alerted = False

    def take_damage(self, damage):
        self.hp -= damage
        self.took_damage += damage


class Goblin(Enemy):

    NAME = "Goblin"
    HP = random.randint(8, 12)
    DAMAGE = random.randint(2, 3)
    IMAGE = 0x792