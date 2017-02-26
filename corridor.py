# T3 Cartridge

import t3

COLORS = {
    'nothing': (0, 0, 0),  # Black.
    'cursor':  (255, 255, 255)  # White.
}

DISPLAY_WIDTH = 3
DISPLAY_HEIGHT = 3


def position(what):
    try:
        pos = what.position
    except AttributeError:
        pos = what

    return pos


class Thing:

    def __init__(self, field, x, y):
        self.field = field
        self.position = (x, y)
        self.color = COLORS['nothing'] # Default. To be overridden.


class Cursor(Thing):

    def __init__(self, field, x, y):
        super().__init__(field, x, y)
        self.color = COLORS['cursor']

    def move(self, direction):
        if direction == t3.left:
            position = (self.position[0] - 1, self.position[1])
        elif direction == t3.right:
            position = (self.position[0] + 1, self.position[1])
        elif direction == t3.up:
            position = (self.position[0], self.position[1] - 1)
        elif direction == t3.down:
            position = (self.position[0], self.position[1] + 1)
        else:
            raise ValueError('Invalid direction.')

        # Stay inside the field.
        if 0 <= position[0] < self.field.WIDTH and 0 <= position[1] < self.field.HEIGHT:
            self.field.clear(self)
            self.position = position
            self.field.draw(self)


class Field:

    WIDTH = 5
    HEIGHT = 5

    def __init__(self):
        self.things = set()
        self.viewport = (1, 1)

    def assert_valid_thing(self, thing):
        if thing not in self.things:
            raise ValueError('Can’t draw an unregistered Thing.')

    def add(self, thing):
        if thing.field != self:
            raise ValueError('Can’t add a Thing from another field.')
        self.things.add(thing)

    def clear(self, what):
        display_position = self.display_position(what)
        if display_position:
            t3.display[display_position] = COLORS['nothing']

    def draw(self, thing=None):
        if thing:
            self.assert_valid_thing(thing)
            things = {thing}
        else:
            things = self.things

        for thing in things:
            display_position = self.display_position(thing)
            if display_position:
                t3.display[display_position] = thing.color

    def display_position(self, what):
        pos = position(what)
        viewport_pos = (pos[0] - self.viewport[0], pos[1] - self.viewport[1])
        if 0 <= viewport_pos[0] < DISPLAY_WIDTH and 0 <= viewport_pos[1] < DISPLAY_HEIGHT:
            display_pos = viewport_pos
        else:
            display_pos = None
        return display_pos


def main():
    field = Field()

    cursor = Cursor(field, 2, 2)
    field.add(cursor)

    field.draw()

    while True:
        result = yield t3.wait_for_input()
        for direction in t3.up, t3.down, t3.left, t3.right:
            if result.pressed[direction]:
                cursor.move(direction)
