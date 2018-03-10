import random
import time
import vars
import enemy
from math import sqrt

from bearlibterminal import terminal


class World(object):

    def __init__(self, width, height, info, seed=time.time()):
        self.width = width
        self.height = height
        self.seed = seed
        self.info = info
        self.terrain_rate = 0.49
        self.x_offset = 0
        self.y_offset = 0
        self.board = [[0 for x in range(self.width)] for x in range(self.height)]
        self.enemies = list()
        self.corpses = list()
        self.player = None
        self.generate_world()
        self.process_world(repeat=2)
        self.recognize_continents()
        self.create_stairs()
        self.create_passages()

    def draw(self):
        self.draw_map()
        for e in self.enemies:
            e.draw()

    def draw_map(self):
        """
        Given map values:
        - 0 - rock
        - 1 - dungeon
        - 2 - stars down
        - 3 - stars up
        """

        for y in range(vars.FIELDS_HEIGHT):
            for x in range(vars.FIELDS_WIDTH):
                terminal.layer(vars.MAP_LAYER)
                if 0 <= y + self.y_offset < self.height and 0 <= x + self.x_offset < self.width and self.board[y + self.y_offset][x + self.x_offset] > 0:
                    terminal.put(x * vars.FIELDS_X_SPACING, y * vars.FIELDS_Y_SPACING, 0xE0B1 if ((x + self.x_offset) * (y + self.y_offset)/3) % 2 > 0 else 0xE078)
                else:
                    terminal.put(x * vars.FIELDS_X_SPACING, y * vars.FIELDS_Y_SPACING, 0xE006)
                terminal.layer(vars.EXTRA_MAP_LAYER)
                if 0 <= y + self.y_offset < self.height and 0 <= x + self.x_offset < self.width and self.board[y + self.y_offset][x + self.x_offset] == 2:
                    terminal.layer(1)
                    terminal.put(x * vars.FIELDS_X_SPACING, y * vars.FIELDS_Y_SPACING, 0xE417)
                elif 0 <= y + self.y_offset < self.height and 0 <= x + self.x_offset < self.width and self.board[y + self.y_offset][x + self.x_offset] == 3:
                    terminal.put(x * vars.FIELDS_X_SPACING, y * vars.FIELDS_Y_SPACING, 0xE419)

                if self.player.died:
                    terminal.layer(10)
                    terminal.put(x * vars.FIELDS_X_SPACING, y * vars.FIELDS_Y_SPACING, 0xE398)
                    terminal.layer(11)
                    terminal.printf(int(vars.CONSOLE_WIDTH/3), int(vars.CONSOLE_HEIGHT / 2), "[color=crimson]YOU DIED! Press R for restart!")

        # Draw corpses
        for corpse in self.corpses:
            # Draw enemy
            x, y = corpse
            if self.is_currently_visible(x, y):
                terminal.layer(vars.UNIT_LAYER)
                terminal.put(self.calculate_draw_x_coordinate(x),
                             self.calculate_draw_y_coordinate(y),
                             0xE26D
                             )


    def generate_world(self):
        random.seed(self.seed)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.random() < self.terrain_rate:
                    self.board[y][x] = 1

    def process_world(self, repeat=1):
        for r in range(repeat):
            for y in range(self.height):
                for x in range(self.width):
                    self.cellurar_automata(x, y)


    def is_taken_by_player(self, x, y):
        # Check if field is taken by player
        return x == self.player.position_x and y == self.player.position_y if self.player else None

    def is_taken_by_enemy(self, x, y):
        # Check if field is taken by player
        for e in self.enemies:
            if e.position_x == x and e.position_y == y:
                return e
        return None

    def is_field_available(self, x, y):
        # Check if fields is available to move
        return self.board[y][x] == 1 and not self.is_taken_by_player(x, y) and not self.is_taken_by_enemy(x, y)

    def is_currently_visible(self, x, y):
        # Check if object is currently visible on map
        return self.x_offset < x < self.x_offset + vars.FIELDS_WIDTH and self.y_offset < y < self.y_offset + vars.FIELDS_HEIGHT

    def calculate_draw_x_coordinate(self, x):
        return (x - self.x_offset) * vars.FIELDS_X_SPACING

    def calculate_draw_y_coordinate(self, y):
        return (y - self.y_offset) * vars.FIELDS_Y_SPACING

    def create_enemies(self):
        # Calculate size of dungeon
        size = 0
        for continent in self.continents:
            size += len(continent)

        # Create 1 enemy per 100 tiles
        for enemy_counter in range(int(size/50)):
            enemy.Goblin(self)


    def create_stairs(self):

        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.board[y][x] == 1:
                self.stars_up = x, y
                self.board[y][x] = 2
                break

        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.board[y][x] == 1:
                self.stars_down = x, y
                self.board[y][x] = 3
                break

    def create_passages(self):
        already_created = list()
        for idx, continent in enumerate(self.continents):
            distance_data = self.calculate_continents_distance(idx)
            if distance_data and [distance_data['closest_continent'], idx] not in already_created:
                sx, sy = distance_data['source_c']
                ex, ey = distance_data['c']
                x_offset = ex - sx
                y_offset = ey - sy
                for x in range(x_offset) if x_offset > 0 else range(x_offset, 1):
                    if self.board[sy][sx + x] == 0:
                        self.board[sy][sx + x] = 1
                for y in range(y_offset) if y_offset > 0 else range(y_offset, 1):
                    if self.board[sy + y][sx + x_offset] == 0:
                        self.board[sy + y][sx + x_offset] = 1
                already_created.append([idx, distance_data['closest_continent']])
            if distance_data and distance_data['second'] and [distance_data['second']['closest_continent'], idx] not in already_created:
                sx, sy = distance_data['second']['source_c']
                ex, ey = distance_data['second']['c']
                x_offset = ex - sx
                y_offset = ey - sy
                for x in range(x_offset) if x_offset > 0 else range(x_offset, 1):
                    if self.board[sy][sx + x] == 0:
                        self.board[sy][sx + x] = 1
                for y in range(y_offset) if y_offset > 0 else range(y_offset, 1):
                    if self.board[sy + y][sx + x_offset] == 0:
                        self.board[sy + y][sx + x_offset] = 1
                already_created.append([idx, distance_data['second']['closest_continent']])

    def calculate_continents_distance(self, idc):
        closest_distance = None
        second_closest_distance = None
        for idx, continent in enumerate(self.continents):
            if idx == idc:
                continue
            else:
                for source_c in self.continents[idc]:
                    for c in continent:
                        distance = self.calculate_distance(source_c, c)
                        if closest_distance is None or distance <= closest_distance['distance']:
                            if closest_distance and closest_distance['closest_continent'] != idx:
                                second_closest_distance = closest_distance
                            closest_distance = dict()
                            closest_distance['distance'] = distance
                            closest_distance['source_c'] = source_c
                            closest_distance['c'] = c
                            closest_distance['closest_continent'] = idx
                            closest_distance['second'] = second_closest_distance
        # TEMPORARY
        # if closest_distance:
        #     x, y = closest_distance['c']
        #     self.board[y][x] = 2
        #     x, y = closest_distance['source_c']
        #     self.board[y][x] = 3
        return closest_distance



    def calculate_distance(self, a, b):
        ax, ay = a
        bx, by = b
        return sqrt( (ax - bx)**2 + (ay - by)**2 )


    def parse_continent(self, x, y, land_position=None):
        # This function parse whole continent and checks land position
        if not land_position:
            land_position = set()
        land_position.add((x, y))
        # Check land on each side: top, bottom, left and right
        if x > 0 and (x - 1, y) not in land_position and self.board[y][x - 1] == 1:
            land_position.update(self.parse_continent(x - 1, y, land_position))
        if x < self.width and (x + 1, y) not in land_position and self.board[y][x + 1] == 1:
            land_position.update(self.parse_continent(x + 1, y, land_position))
        if y > 0 and (x, y - 1) not in land_position and self.board[y - 1][x] == 1:
            land_position.update(self.parse_continent(x, y - 1, land_position))
        if y < self.height and (x, y + 1) not in land_position and self.board[y + 1][x] == 1:
            land_position.update(self.parse_continent(x, y + 1, land_position))
        return land_position


    def recognize_continents(self):
        # Top to down, left to right
        self.continents = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if not any((x, y) in coordinates for coordinates in self.continents) and self.board[y][x] == 1:
                    self.continents.append(self.parse_continent(x, y))
        # Remove continents less then 9
        for c in self.continents:
            if len(c) < 9:
                for coordinates in c:
                    x, y = coordinates
                    self.board[y][x] = 0
                self.continents.remove(c)



    def cellurar_automata(self, x, y):
        """
        The basic idea is to fill the first map randomly, then repeatedly create new maps using the 4-5 rule:
        a tile becomes a wall if it was a wall and 4 or more of its eight neighbors were walls, or if it was
        not a wall and 5 or more neighbors were.
        """
        value = self.sum_neighbourhood(x, y)
        if self.board[y][x] == 1 and value < 4:
            self.board[y][x] = 0
        if self.board[y][x] == 0 and value > 4:
            self.board[y][x] = 1

    def sum_neighbourhood(self, x, y):
        top_left = self.board[y - 1][x - 1] if (x > 0 and y > 0) else 0
        top_top = self.board[y - 1][x] if y > 0 else 0
        top_right = self.board[y - 1][x + 1] if y > 0 and (x + 1) < self.width else 0
        center_left = self.board[y][x - 1] if x > 0 else 0
        center_right = self.board[y][x + 1] if (x + 1) < self.width else 0
        bottom_left = self.board[y + 1][x - 1] if x > 0 and (y + 1) < self.height else 0
        botton_bottom = self.board[y + 1][x] if (y + 1) < self.height else 0
        bottom_right = self.board[y + 1][x + 1] if ((x + 1) < self.width and (y + 1) < self.height) else 0

        return top_left + top_top + top_right + center_left + center_right + bottom_left + botton_bottom + bottom_right
