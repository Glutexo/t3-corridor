# T3 Cartridge

import t3


class OutOfBoundError(ValueError):
    """"""


class Field:

    EMPTY  = 0
    CURSOR = 1

    COLORS = {
        CURSOR: (255, 255, 255),  # White.
        EMPTY: (0, 0, 0)  # Black.
    }

    state = [
        [EMPTY, EMPTY,  EMPTY],
        [EMPTY, CURSOR, EMPTY],
        [EMPTY, EMPTY,  EMPTY]
    ]
    WIDTH  = len(state[0])
    HEIGHT = len(state)

    def each(self):
        for y, row in enumerate(self.state):
            for x, value in enumerate(row):
                yield x, y, value

    def set_by_position(self, position, value):
        self.state[position[1]][position[0]] = value

    def get_by_position(self, position):
        return self.state[position[1]][position[0]]

    def display(self):
        for x, y, value in self.each():
            t3.display[x, y] = self.COLORS[value]

    def cursor_position(self):
        cursor_position = None

        for x, y, value in self.each():
            print(x, y, value)
            if value == self.CURSOR:
                cursor_position = [x, y]
                # break

        if cursor_position is None:
            raise RuntimeError('Cursor not found in state!')

        return cursor_position

    def move_cursor(self, direction):
        old_position = self.cursor_position()
        new_position = list(old_position)

        if direction == t3.left:
            new_position[0] -= 1
        elif direction == t3.right:
            new_position[0] += 1
        elif direction == t3.up:
            new_position[1] -= 1
        elif direction == t3.down:
            new_position[1] += 1
        else:
            raise ValueError('Invalid direction.')

        try:
            if new_position[0] < 0 or new_position[0] > self.WIDTH - 1 or new_position[1] < 0 or new_position[1] > self.HEIGHT - 1:
                raise OutOfBoundError

            self.set_by_position(old_position, self.EMPTY)
            self.set_by_position(new_position, self.CURSOR)
            self.display()
        except OutOfBoundError:
            """"""


def main():
    field = Field()
    field.display()

    while True:
        result = yield t3.wait_for_input()
        for direction in t3.up, t3.down, t3.left, t3.right:
            if(result.pressed[direction]):
                field.move_cursor(direction)
