from collections import namedtuple
from corridor.ui import Viewport
from unittest import main, TestCase

FieldToDisplayTestData = namedtuple('FieldToDisplayTestData', ['field_size',
                                                               'viewport_size',
                                                               'viewport_pos',
                                                               'point_pos_in_field',
                                                               'point_pos_in_viewport'])
IsViewportPosVisibleTestData = namedtuple('IsViewportPosVisibleTestData', ['field_size',
                                                                           'viewport_size',
                                                                           'viewport_pos',
                                                                           'point_pos_in_viewport',
                                                                           'visible'])


class TestFieldToDisplay(TestCase):
    """
    Tests the Viewport.field_to_display method, whether it correctly translates absolute field coordinates to relative
    viewport coordinates.
    """

    def run_tests(self, tests):
        """
        Tests the field_to_display method with given test data containing all the constructor arguments, method
        arguments and an expected result.
        """
        for index, test_data in enumerate(tests):
            with self.subTest(index=index):
                viewport = Viewport(test_data.field_size,
                                    test_data.viewport_size,
                                    test_data.viewport_pos)
                actual_point_pos_in_viewport = viewport.field_to_viewport(test_data.point_pos_in_field)
                expected_point_pos_in_viewport = test_data.point_pos_in_viewport
                self.assertEqual(actual_point_pos_in_viewport, expected_point_pos_in_viewport)

    def test_inside_the_window(self):
        """
        The viewport coordinates are calculated correctly when the point is inside the window.
        """
        tests = [
            # XXXXXXXXXX
            # XXOOOOXXXX
            # XXOOPOXXXX
            # XXOOOOXXXX
            # XXXXXXXXXX
            # XXXXXXXXXX
            FieldToDisplayTestData(field_size=(10, 6),
                                   viewport_size=(4, 3),
                                   viewport_pos=(2, 1),
                                   point_pos_in_field=(4, 2),
                                   point_pos_in_viewport=(2, 1)),
            # XXXXXXXXXX
            # XXPOOOXXXX
            # XXOOOOXXXX
            # XXOOOOXXXX
            # XXXXXXXXXX
            # XXXXXXXXXX
            FieldToDisplayTestData(field_size=(10, 6),
                                   viewport_size=(4, 3),
                                   viewport_pos=(2, 1),
                                   point_pos_in_field=(2, 1),
                                   point_pos_in_viewport=(0, 0)),

            # XXXXXXXXXX
            # XXOOOOXXXX
            # XXOOOOXXXX
            # XXOOO1XXXX
            # XXXXXXXXXX
            # XXXXXXXXXX
            FieldToDisplayTestData(field_size=(10, 6),
                                   viewport_size=(4, 3),
                                   viewport_pos=(2, 1),
                                   point_pos_in_field=(5, 3),
                                   point_pos_in_viewport=(3, 2)),

            # POXXXXXX
            # OOXXXXXX
            # XXXXXXXX
            FieldToDisplayTestData(field_size=(8, 3),
                                   viewport_size=(2, 2),
                                   viewport_pos=(0, 0),
                                   point_pos_in_field=(0, 0),
                                   point_pos_in_viewport=(0, 0)),

            # XXXXXXXX
            # XXXXXXOO
            # XXXXXXOP
            FieldToDisplayTestData(field_size=(8, 3),
                                   viewport_size=(2, 2),
                                   viewport_pos=(6, 1),
                                   point_pos_in_field=(7, 2),
                                   point_pos_in_viewport=(1, 1)),
        ]
        self.run_tests(tests)

    def test_outside_the_window(self):
        """
        The viewport coordinates are calculated correctly when the point is outside the window.
        """
        tests = [
            # XXXXX
            # OOXXX
            # OOXXX
            # OOXXX
            # PXXXX
            # XXXXX
            FieldToDisplayTestData(field_size=(5, 6),
                                   viewport_size=(2, 3),
                                   viewport_pos=(0, 1),
                                   point_pos_in_field=(0, 4),
                                   point_pos_in_viewport=(0, 3)),

            # XXXXX
            # OOXPX
            # OOXXX
            # OOXXX
            # XXXXX
            # XXXXX
            FieldToDisplayTestData(field_size=(5, 6),
                                   viewport_size=(2, 3),
                                   viewport_pos=(0, 1),
                                   point_pos_in_field=(3, 1),
                                   point_pos_in_viewport=(3, 0)),

            # PXXXX
            # XXXXX
            # XXXXX
            # XXXXX
            # XXOXX
            # XXXXX
            FieldToDisplayTestData(field_size=(5, 6),
                                   viewport_size=(1, 1),
                                   viewport_pos=(2, 4),
                                   point_pos_in_field=(0, 0),
                                   point_pos_in_viewport=(-2, -4)),
        ]
        self.run_tests(tests)


class TestIsViewportPosVisible(TestCase):
    """
    Tests the Viewport.field_to_display method, whether it correctly determines that relative viewport coordinates are
    inside the window.
    """

    def run_tests(self, tests):
        """
        Tests the is_viewport_pos_visible method with given test data containing all the constructor arguments, method
        arguments and an expected result.
        """
        for index, test_data in enumerate(tests):
            with self.subTest(index=index):
                viewport = Viewport(field_size=test_data.field_size,
                                    viewport_size=test_data.viewport_size,
                                    viewport_pos=test_data.viewport_pos)
                actual_visible = viewport.is_viewport_pos_visible(test_data.point_pos_in_viewport)
                expected_visible = test_data.visible
                self.assertEqual(actual_visible, expected_visible)

    def test_is_visible(self):
        """
        The viewport coordinates are correcly recognized as inside the window.
        """
        tests = [
            # XXXX
            # XXPX
            # XXXX
            IsViewportPosVisibleTestData(field_size=(4, 3),
                                         viewport_size=(1, 1),
                                         viewport_pos=(2, 1),
                                         point_pos_in_viewport=(0, 0),
                                         visible=True),

            # XXXXXX
            # XXOPOX
            # XXXXXX
            # XXXXXX
            # XXXXXX
            IsViewportPosVisibleTestData(field_size=(6, 5),
                                         viewport_size=(3, 1),
                                         viewport_pos=(2, 1),
                                         point_pos_in_viewport=(1, 0),
                                         visible=True)
        ]
        self.run_tests(tests)

    def test_is_not_visible(self):
        """
        The viewport coordinates are correctly recognized as outside the window.
        """
        tests = [
            # XXXX
            # PXOX
            # XXXX
            IsViewportPosVisibleTestData(field_size=(4, 3),
                                         viewport_size=(1, 1),
                                         viewport_pos=(2, 1),
                                         point_pos_in_viewport=(-2, 0),
                                         visible=False),

            # XXXXXX
            # XXOOOX
            # XXOOOX
            # XXXPXX
            # XXXXXX
            IsViewportPosVisibleTestData(field_size=(6, 5),
                                         viewport_size=(3, 2),
                                         viewport_pos=(3, 1),
                                         point_pos_in_viewport=(1, 2),
                                         visible=False)
        ]
        self.run_tests(tests)


if __name__ == "__main__":
    main()
