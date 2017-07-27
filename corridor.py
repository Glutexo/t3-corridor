# T3 Cartridge

import t3


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dimensions:

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Thing:

    def __init__(self, field, position):
        self.field = field
        self.position = position
        self.color = COLORS['nothing'] # Default. To be overridden.


class Color:

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class Cursor(Thing):

    def __init__(self, field, position):
        super().__init__(field, position)
        self.color = COLORS['cursor']

    def move(self, direction):
        if direction == t3.left:
            position = Position(self.position.x - 1, self.position.y)
        elif direction == t3.right:
            position = Position(self.position.x + 1, self.position.y)
        elif direction == t3.up:
            position = Position(self.position.x, self.position.y - 1)
        elif direction == t3.down:
            position = Position(self.position.x, self.position.y + 1)
        else:
            raise ValueError('Invalid direction.')

        # Stay inside the field.
        if self.field.validate_position(position):
            self.field.clear(self.position)
            self.position = position
            self.field.draw(self)


class Field:

    def __init__(self, dimensions, viewport):
        self.things = set()
        self.dimensions = dimensions
        self.viewport = viewport

    def assert_valid_thing(self, thing):
        if thing not in self.things:
            raise ValueError('Can’t draw an unregistered Thing.')

    def add(self, thing):
        if thing.field != self:
            raise ValueError('Can’t add a Thing from another field.')
        self.things.add(thing)

    def clear(self, position):
        display_position = self.display_position(position)
        if display_position:
            display(display_position, COLORS['nothing'])

    def draw(self, thing=None):
        if thing:
            self.assert_valid_thing(thing)
            things = {thing}
        else:
            things = self.things

        for thing in things:
            display_position = self.display_position(thing.position)
            if display_position:
                display(display_position, thing.color)

    def display_position(self, actual_position):
        display_position = Position(actual_position.x - self.viewport.x, actual_position.y - self.viewport.y)
        if 0 <= display_position.x < DISPLAY_DIMENSIONS.width and 0 <= display_position.y < DISPLAY_DIMENSIONS.height:
            valid_display_position = display_position
        else:
            valid_display_position = None
        return valid_display_position

    def validate_position(self, position):
        return 0 <= position.x < self.dimensions.width and 0 <= position.y < self.dimensions.height


def display(position, color):
    t3.display[position.x, position.y] = (color.red, color.green, color.blue)


COLORS = {
    'nothing': Color(0, 0, 0),  # Black.
    'cursor':  Color(255, 255, 255)  # White.
}

DISPLAY_DIMENSIONS = Dimensions(3, 3)
FIELD_DIMENSIONS = Dimensions(5, 5)
INITIAL_VIEWPORT = Position(1, 1)
INITIAL_CURSOR_POSITON = Position(2, 2)

def main():
    field = Field(FIELD_DIMENSIONS, INITIAL_VIEWPORT)

    cursor = Cursor(field, INITIAL_CURSOR_POSITON)
    field.add(cursor)

    field.draw()

    while True:
        result = yield t3.wait_for_input()
        for direction in t3.up, t3.down, t3.left, t3.right:
            if result.pressed[direction]:
                cursor.move(direction)
