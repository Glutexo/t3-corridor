from corridor.constants import COLORS, DISPLAY_WIDTH, DISPLAY_HEIGHT
try:
    from t3 import display, down, left, right, up
except ImportError:
    pass  # T3 is not available withing tests.

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
        if direction == left:
            position = (self.position[0] - 1, self.position[1])
        elif direction == right:
            position = (self.position[0] + 1, self.position[1])
        elif direction == up:
            position = (self.position[0], self.position[1] - 1)
        elif direction == down:
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

    def __init__(self, viewport):
        self.things = set()
        self.viewport = viewport

    def add(self, thing):
        if thing.field != self:
            raise ValueError('Can’t add a Thing from another field.')
        self.things.add(thing)

    def clear(self, what):
        viewport_pos = self.viewport.field_to_viewport(what.position)
        if self.viewport.is_viewport_pos_visible(viewport_pos):
            display[viewport_pos] = COLORS['nothing']

    def draw(self, thing=None):
        if thing:
            things = {thing}
        else:
            things = self.things

        for thing in things:
            viewport_pos = self.viewport.field_to_viewport(thing.position)
            if self.viewport.is_viewport_pos_visible(viewport_pos):
                display[viewport_pos] = thing.color
