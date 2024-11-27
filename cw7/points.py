class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return (self.x * self.x + self.y * self.y)**0.5
    
    def __repr__(self):
        return str(self)

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5