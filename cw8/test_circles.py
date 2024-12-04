from circles import Circle
from points import Point

from math import pi
import pytest

@pytest.fixture
def circles():
    c1 = Circle(0, 0, 2)
    c2 = Circle(0, 0, 3)
    c3 = Circle(2, 2, 4)
    c4 = Circle(1, 1, 3)
    return c1, c2, c3, c4

def test_repr(circles):
    c1, _, _, _ = circles
    assert repr(c1) == "Circle(0, 0, 2)"

def test_eq(circles):
    c1, _, c3, _ = circles
    assert c1 == Circle(0, 0, 2)
    assert c1 != c3

def test_ne(circles):
    c1, _, c3, _ = circles
    assert not (c1 != Circle(0, 0, 2))
    assert c1 != c3

def test_area(circles):
    c1, _, _, _ = circles
    assert pytest.approx(c1.area(), rel=1e-6) == 4 * pi

def test_move(circles):
    c1, _, c3, _ = circles
    c1.move(4, 2)
    assert c1.pt == Point(4, 2)
    c3.move(-2, -2)
    assert c3.pt == Point(0, 0)

def test_cover(circles):
    c1, c2, _, c4 = circles
    result = c1.cover(c2)
    assert result == Circle(0, 0, 3)

    result = c2.cover(c4)
    assert pytest.approx(result.pt.x, rel=1e-5) == 0.5
    assert pytest.approx(result.pt.y, rel=1e-5) == 0.5
    assert pytest.approx(result.radius, rel=1e-5) == 3.7071

def test_from_points():
    circle = Circle.from_points([Point(0, 2), Point(1, 1), Point(2, 2)])
    assert circle == Circle(1, 2, 1)

    circle = Circle.from_points([Point(2, 3), Point(3, 1), Point(2, 2)])
    assert pytest.approx(circle.pt.x) == 3.5
    assert pytest.approx(circle.pt.y) == 2.5
    assert pytest.approx(circle.radius, rel=1e-5) == 1.5811388300841898

def test_properties(circles):
    c1, c2, _, _ = circles

    assert pytest.approx(c1.top, rel=1e-6) == 2
    assert pytest.approx(c1.bottom, rel=1e-6) == -2
    assert pytest.approx(c1.left, rel=1e-6) == -2
    assert pytest.approx(c1.right, rel=1e-6) == 2
    assert pytest.approx(c1.width, rel=1e-6) == 4
    assert pytest.approx(c1.height, rel=1e-6) == 4
    assert pytest.approx(c1.topleft.x, rel=1e-6) == -2
    assert pytest.approx(c1.topleft.y, rel=1e-6) == 2
    assert pytest.approx(c1.bottomleft.x, rel=1e-6) == -2
    assert pytest.approx(c1.bottomleft.y, rel=1e-6) == -2
    assert pytest.approx(c1.topright.x, rel=1e-6) == 2
    assert pytest.approx(c1.topright.y, rel=1e-6) == 2
    assert pytest.approx(c1.bottomright.x, rel=1e-6) == 2
    assert pytest.approx(c1.bottomright.y, rel=1e-6) == -2

    assert pytest.approx(c2.top, rel=1e-6) == 3
    assert pytest.approx(c2.bottom, rel=1e-6) == -3
    assert pytest.approx(c2.left, rel=1e-6) == -3
    assert pytest.approx(c2.right, rel=1e-6) == 3
    assert pytest.approx(c2.width, rel=1e-6) == 6
    assert pytest.approx(c2.height, rel=1e-6) == 6
    assert pytest.approx(c2.topleft.x, rel=1e-6) == -3
    assert pytest.approx(c2.topleft.y, rel=1e-6) == 3
    assert pytest.approx(c2.bottomleft.x, rel=1e-6) == -3
    assert pytest.approx(c2.bottomleft.y, rel=1e-6) == -3
    assert pytest.approx(c2.topright.x, rel=1e-6) == 3
    assert pytest.approx(c2.topright.y, rel=1e-6) == 3
    assert pytest.approx(c2.bottomright.x, rel=1e-6) == 3
    assert pytest.approx(c2.bottomright.y, rel=1e-6) == -3