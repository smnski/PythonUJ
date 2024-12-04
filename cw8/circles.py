from math import pi, sqrt
from points import Point

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
    
    @classmethod
    def from_points(cls, pts):
        if len(pts) != 3:
            raise ValueError("oczekiwano trzech punktow")

        p1, p2, p3 = pts

        d = 2 * ( p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y) )
        if d == 0:
            raise ValueError("z podanych punktow nie da sie stworzyc okregu")

        Ux = ( (p1.x ** 2 + p1.y ** 2) * (p2.y - p3.y) + (p2.x ** 2 + p2.y ** 2) * (p3.y - p1.y) + (p3.x ** 2 + p3.y ** 2) * (p1.y - p2.y) ) / d
        Uy = ( (p1.x ** 2 + p1.y ** 2) * (p3.x - p2.x) + (p2.x ** 2 + p2.y ** 2) * (p1.x - p3.x) + (p3.x ** 2 + p3.y ** 2) * (p2.x - p1.x) ) / d
        radius = sqrt((Ux - p1.x) ** 2 + (Uy - p1.y) ** 2)

        return cls(Ux, Uy, radius)
    
    @property
    def top(self):
        return self.pt.y + self.radius

    @property
    def bottom(self):
        return self.pt.y - self.radius

    @property
    def left(self):
        return self.pt.x - self.radius

    @property
    def right(self):
        return self.pt.x + self.radius

    @property
    def width(self):
        return self.radius * 2

    @property
    def height(self):
        return self.radius * 2

    @property
    def topleft(self):
        return Point(self.left, self.top)

    @property
    def bottomleft(self):
        return Point(self.left, self.bottom)

    @property
    def topright(self):
        return Point(self.right, self.top)

    @property
    def bottomright(self):
        return Point(self.right, self.bottom)