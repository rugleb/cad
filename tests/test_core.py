import unittest

from cad import core


class DrawStyleTestCase(unittest.TestCase):

    def test_on_types(self):
        for style in core.DrawStyle:
            self.assertIsInstance(style.width, float)
            self.assertIsInstance(style.color, core.Color)


if __name__ == '__main__':
    unittest.main()
