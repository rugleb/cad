import unittest

from cad import core


class DrawStyleTestCase(unittest.TestCase):

    def test_on_types(self):
        for style in core.DrawStyle:
            self.assertIsInstance(style.width, float)
            self.assertIsInstance(style.color, core.Color)


class ContainerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.container = core.Container([1, 2, 3])

    def test_first_method(self):
        first = self.container.first()
        self.assertEqual(self.container[0], first)

    def test_last_method(self):
        last = self.container.last()
        self.assertEqual(self.container[-1], last)

    def test_all_method(self):
        generator = self.container.all()
        self.assertIsInstance(generator, core.Generator)

        for i, v in enumerate(generator):
            self.assertEqual(self.container[i], v)


if __name__ == '__main__':
    unittest.main()
