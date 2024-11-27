from math import pi
from points import Point
import unittest

class Circle:
    def __init__(self, x, y, radius):
        if radius < 0:
            raise ValueError("promień ujemny")
        self.pt = Point(x, y)
        self.radius = radius

    def __repr__(self):
        return f"Circle({self.pt.x}, {self.pt.y}, {self.radius})"

    def __eq__(self, other):
        return self.pt == other.pt and self.radius == other.radius

    def __ne__(self, other):
        return not self == other

    def area(self):
        return pi * self.radius**2

    def move(self, x, y):
        self.pt.x += x
        self.pt.y += y

    def cover(self, other):
        if not isinstance(other, Circle):
            raise ValueError("argument musi być typu Circle")
        
        dist = self.pt.distance(other.pt)
        if max(self.radius, other.radius) >= dist + min(self.radius, other.radius):
            bigger = self if self.radius >= other.radius else other
            return Circle(bigger.pt.x, bigger.pt.y, bigger.radius)
        
        new_radius = (dist + self.radius + other.radius) / 2
        new_x = self.pt.x + ( (other.pt.x - self.pt.x) * (new_radius - self.radius) ) / dist
        new_y = self.pt.y + ( (other.pt.y - self.pt.y) * (new_radius - self.radius) ) / dist

        return Circle(new_x, new_y, new_radius)

class TestCircle(unittest.TestCase):
    def setUp(self):
        self.c1 = Circle(0, 0, 2)
        self.c2 = Circle(0, 0, 3)
        self.c3 = Circle(2, 2, 4)
        self.c4 = Circle(1, 1, 3)

    def test_repr(self):
        self.assertEqual(repr(self.c1), "Circle(0, 0, 2)")

    def test_eq(self):
        self.assertTrue(self.c1 == Circle(0, 0, 2))
        self.assertFalse(self.c1 == self.c3)

    def test_ne(self):
        self.assertFalse(self.c1 != Circle(0, 0, 2))
        self.assertTrue(self.c1 != self.c3)

    def test_area(self):
        self.assertAlmostEqual(self.c1.area(), 4*pi)

    def test_move(self):
        self.c1.move(4, 2)
        self.assertEqual(self.c1.pt, Point(4, 2))
        self.c3.move(-2, -2)
        self.assertEqual(self.c2.pt, Point(0, 0))

    def test_cover(self):
        result = self.c1.cover(self.c2)
        self.assertEqual(result, Circle(0, 0, 3))

        result = self.c2.cover(self.c4)
        self.assertAlmostEqual(result.pt.x, 0.5, places=4)
        self.assertAlmostEqual(result.pt.y, 0.5, places=4)
        self.assertAlmostEqual(result.radius, 3.7071, places=4)

if __name__ == "__main__":
    unittest.main()