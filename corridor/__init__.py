# T3 Cartridge

from corridor.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from corridor.game import Cursor, Field
from corridor.ui import Viewport
try:
    import t3
except ImportError:
    pass  # T3 is not available withing tests.


def main():
    viewport = Viewport(field_size=(5, 5),
                        viewport_size=(DISPLAY_WIDTH, DISPLAY_HEIGHT),
                        viewport_pos=(1, 1))
    field = Field(viewport=viewport)

    cursor = Cursor(field, 2, 2)
    field.add(cursor)

    field.draw()

    while True:
        result = yield t3.wait_for_input()
        for direction in t3.up, t3.down, t3.left, t3.right:
            if result.pressed[direction]:
                cursor.move(direction)
