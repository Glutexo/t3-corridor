# T3 Cartridge

import t3
from corridor.game import Cursor, Field

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
