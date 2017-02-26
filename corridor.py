# T3 Cartridge

import t3

COLORS = {
    'nothing': (0, 0, 0),  # Black.
    'cursor':  (255, 255, 255)  # White.
}


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

    WIDTH  = 3
    HEIGHT = 3

    def __init__(self):
        self.things = set()

    def add(self, thing):
        if thing.field != self:
            raise ValueError('Trying to add a thing from another field.')
        self.things.add(thing)

    def clear(self, what):
        try:
            position = what.position
        except AttributeError:
            position = what

        t3.display[position] = COLORS['nothing']

    def draw(self, thing=None):
        if thing:
            things = {thing}
        else:
            things = self.things

        for thing in things:
            t3.display[thing.position] = thing.color


def main():
    field = Field()

    cursor = Cursor(field, 1, 1)
    field.add(cursor)

    field.draw()

    while True:
        result = yield t3.wait_for_input()
        for direction in t3.up, t3.down, t3.left, t3.right:
            if result.pressed[direction]:
                cursor.move(direction)
