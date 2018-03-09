import random
import vars
from bearlibterminal import terminal

class Player(object):

    def __init__(self, name, world):

        self.world = world
        self.world.player = self

        self.strength = 10
        self.agility = 8
        self.stamina = 10
        self.intellect = 6

        self.level = 1
        self.exp = 0
        self.next_level_exp = self.get_next_level_exp_required()
        self.role = "Warrior"

        self.max_hp = self.get_max_hp()
        self.hp = self.max_hp

        self.max_mana = self.get_max_hp()
        self.mana = self.max_hp

        self.position_x, self.position_y = self.world.stars_up
        self.name = name

        self.turn = 1
        self.died = False
        self.restart = False

        self.init_start_position()

    def update(self):
            key = terminal.read()
            if key == terminal.TK_CLOSE:
                vars.QUIT = True
            if not self.check_if_died():
                if key == terminal.TK_RIGHT:
                    if self.world.is_field_available(self.position_x + 1, self.position_y):
                        self.position_x += 1
                        self.world.x_offset += 1
                        self.turn += 1
                    else:
                        enemy = self.world.is_taken_by_enemy(self.position_x + 1, self.position_y)
                        if enemy:
                            self.attack(enemy)
                if key == terminal.TK_LEFT:
                    if self.world.is_field_available(self.position_x - 1, self.position_y):
                        self.position_x -= 1
                        self.world.x_offset -= 1
                        self.turn += 1
                    else:
                        enemy = self.world.is_taken_by_enemy(self.position_x - 1, self.position_y)
                        if enemy:
                            self.attack(enemy)
                if key == terminal.TK_UP:
                    if self.world.is_field_available(self.position_x, self.position_y - 1):
                        self.position_y -= 1
                        self.world.y_offset -= 1
                        self.turn += 1
                    else:
                        enemy = self.world.is_taken_by_enemy(self.position_x, self.position_y - 1)
                        if enemy:
                            self.attack(enemy)
                if key == terminal.TK_DOWN:
                    if self.world.is_field_available(self.position_x, self.position_y + 1):
                        self.position_y += 1
                        self.world.y_offset += 1
                        self.turn += 1
                    else:
                        enemy = self.world.is_taken_by_enemy(self.position_x, self.position_y + 1)
                        if enemy:
                            self.attack(enemy)
            else:
                if key == terminal.TK_R:
                    self.restart = True

    def attack(self, enemy):
        if self.get_hit(enemy):
            critical = self.get_critical(enemy)
            total_damage = self.get_total_damage() * 2 if critical else self.get_total_damage()
            enemy.take_damage(total_damage)
            self.world.info.add_message("You {0} a {2} for {1} damage!".format("critical hit" if critical else "hit", total_damage, enemy.name), vars.INFOBAR_DAMAGE)
        else:
            pass

    def get_hit(self, enemy):
        # Base hit is 80% plus 5% each level difference between enemy and player
        hit_chance = vars.ENEMY_DEFAULT_HIT_CHANCE + (0.05 * (self.level - enemy.level))
        r = random.random()
        msg = "You attack with fierce! "
        if r <= hit_chance:
            hit = True
            msg += "HIT!"
        else:
            hit = False
            msg += "MISSED!"
        self.world.info.add_message(msg, vars.INFOBAR_DAMAGE)
        return hit

    def get_critical(self, enemy):
        # Critical chance is 5% and increase 5% each level difference
        critical_hit_chance = vars.ENEMY_DEFAULT_CRITICAL_HIT_CHANCE + (0.05 * (self.level - enemy.level))
        return random.random() <= critical_hit_chance

    def get_total_damage(self):
        return int(self.strength/2)


    def get_coordinates(self):
        return self.position_x, self.position_y

    def init_start_position(self):
        self.world.x_offset = self.position_x - int(vars.FIELDS_WIDTH / 2)
        self.world.y_offset = self.position_y - int(vars.FIELDS_HEIGHT / 2)
        if self.world.x_offset < 0:
            self.world.x_offset = 0
        if self.world.y_offset < 0:
            self.world.y_offset = 0

    def draw(self):
        # Draw player
        terminal.layer(vars.UNIT_LAYER)
        if self.world.is_currently_visible(self.position_x, self.position_y):
            terminal.put(self.world.calculate_draw_x_coordinate(self.position_x),
                         self.world.calculate_draw_y_coordinate(self.position_y),
                         0xE6E8)

        # # Draw player turn
        # terminal.layer(vars.MAP_LAYER)
        # terminal.printf(0, vars.CONSOLE_HEIGHT - 1, "Turn {0}".format(self.turn))

    def get_max_hp(self):
        return 5 + self.stamina * 2

    def get_max_mana(self):
        return 5 + self.intellect * 2

    def get_next_level_exp_required(self):
        return int(self.level ** 1.75) * 1000

    def check_if_died(self):
        if self.hp <= 0:
            if not self.died:
                self.world.info.add_message("You died!", vars.INFOBAR_DAMAGE)
                self.world.info.add_message("END GAME", vars.INFOBAR_DAMAGE)
                self.died = True
            return True
        return False

    def take_damage(self, damage, who):
        self.hp -= damage
