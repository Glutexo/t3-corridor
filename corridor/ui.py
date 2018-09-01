class Viewport:
    """
    Provides a view on a field of different size like looking through a window.
    Something like this:
    XXXXXXXXXX
    XOOOXXXXXX
    XOOOXXXXXX
    XOOOXXXXXX
    XXXXXXXXXX
    XXXXXXXXXX
    """

    def __init__(self, field_size, viewport_size, viewport_pos):
        """
        Field is the physical thing, viewport is the window.
        Example:
        XXXXXXXXXX
        XOOOXXXXXX
        XOOOXXXXXX
        XOOOXXXXXX
        XXXXXXXXXX
        XXXXXXXXXX
        field_size is (10, 6), display_size is (3, 3), display_pos is (1, 1)
        """
        self.field_size = field_size
        self.viewport_size = viewport_size
        self.viewport_pos = viewport_pos

    def field_to_viewport(self, field_pos):
        """
        Converts the absolute coordinates in the physical field to relative coordinates to the viewport. It doesn’t
        check whether the coordinates are actually inside the viewport.
        XXXXXXXXXX
        XOPOXXXXXX
        XOOOXXXXXX
        XOOOXXXXXX
        XXXXXXXXXX
        XXXXXXXXXX
        The viewport position is (1, 1). The P here has absolute field coordinates (2, 1), its relative viewport
        coordinates are (1, 0).
        """
        return (field_pos[0] - self.viewport_pos[0],
                field_pos[1] - self.viewport_pos[1])

    def is_viewport_pos_visible(self, viewport_pos):
        """
        Checks whether the given relative viewport coordinates are inside the window.
        XXXXXXXXXX
        XPOOXXXXXX
        XOOOXXXXXX
        XOOOXXXXXX
        XXXXXXXXXX
        XXXXXXXXXX
        True
        XXXXXXXXXX
        POOOXXXXXX
        XOOOXXXXXX
        XOOOXXXXXX
        XXXXXXXXXX
        XXXXXXXXXX
        False
        """
        return 0 <= viewport_pos[0] < self.viewport_size[0] and 0 <= viewport_pos[1] < self.viewport_size[1]
