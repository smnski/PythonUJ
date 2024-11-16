import unittest

class Polynomial:
    def __init__(self, c: list):
        self.a = c[:]
        self.size = len(c)

    def __str__(self):
        return str(self.a)
    
    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        max_length = max(len(self.a), len(other.a))
        self_extended = self.a + [0] * (max_length - len(self.a))
        other_extended = other.a + [0] * (max_length - len(other.a))

        result = [self_extended[i] + other_extended[i] for i in range(max_length)]
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        return Polynomial(result)
    
    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        max_length = max(len(self.a), len(other.a))
        self_extended = self.a + [0] * (max_length - len(self.a))
        other_extended = other.a + [0] * (max_length - len(other.a))

        result = [self_extended[i] - other_extended[i] for i in range(max_length)]
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        return Polynomial(result)
    
    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        result_length = len(self.a) + len(other.a) - 1
        result = [0] * result_length

        for i in range(len(self.a)):
            for j in range(len(other.a)):
                result[i + j] += self.a[i] * other.a[j]

        while len(result) > 1 and result[-1] == 0:
            result.pop()
    
        return Polynomial(result)
    
    def __pos__(self) -> 'Polynomial':
        return Polynomial([abs(coeff) for coeff in self.a])
    
    def __neg__(self) -> 'Polynomial':
        return Polynomial([-abs(coeff) for coeff in self.a])
    
    def __eq__(self, other: 'Polynomial') -> bool:
        self_trimmed = self.a[:]
        other_trimmed = other.a[:]
        
        while self_trimmed and self_trimmed[-1] == 0:
            self_trimmed.pop()
        while other_trimmed and other_trimmed[-1] == 0:
            other_trimmed.pop()

        return self_trimmed == other_trimmed
    
    def __ne__(self, other: 'Polynomial') -> bool:
        self_trimmed = self.a[:]
        other_trimmed = other.a[:]
        
        while self_trimmed and self_trimmed[-1] == 0:
            self_trimmed.pop()
        while other_trimmed and other_trimmed[-1] == 0:
            other_trimmed.pop()

        return self_trimmed != other_trimmed
    
    def eval(self, point: float) -> float:
        result = 0
        for coef in reversed(self.a):
            result = result * point + coef

        return result
    
    def combine(self, other: 'Polynomial') -> 'Polynomial':
        result = Polynomial([0])
        temp_poly = Polynomial([1])

        for coef in self.a:
            term = temp_poly * Polynomial([coef])
            result = result + term
            temp_poly = temp_poly * other

        return result
    
    def __pow__(self, power: int) -> 'Polynomial':
        result = Polynomial([1])
        for _ in range(power):
            result = result * self

        return result
        
    def diff(self) -> 'Polynomial':
        if len(self.a) <= 1:
            return Polynomial([0])
    
        result = [self.a[i] * i for i in range(1, len(self.a))]
        return Polynomial(result)
    
    def integrate(self, constant: float = 0) -> 'Polynomial':
        result = [constant] + [self.a[i] / (i + 1) for i in range(len(self.a))]
        return Polynomial(result)
    
    def is_zero(self) -> bool:
        return all(coef == 0 for coef in self.a)

class TestPolynomials(unittest.TestCase):
    p0 = Polynomial([0])          # W(x) = 0
    p0_v2 = Polynomial([0, 0, 0]) # W(x) = 0
    p1 = Polynomial([0, 2])       # W(x) = 2x
    p2 = Polynomial([1, 2, 3])    # W(x) = 1 + 2x + 3x^2
    p_neg = Polynomial([0, -1])   # W(x) = -x

    def test_str(self):
        result = str(self.p2)
        self.assertEqual(result, "[1, 2, 3]")

    def test_add(self):
        result = self.p1 + self.p2
        self.assertEqual(result.a, [1, 4, 3])

    def test_sub(self):
        result = self.p2 - self.p1
        self.assertEqual(result.a, [1, 0, 3])

    def test_mul(self):
        result = self.p1 * self.p_neg
        self.assertEqual(result.a, [0, 0, -2])

    def test_pos(self):
        result = +self.p_neg
        self.assertEqual(result.a, [0, 1])

    def test_neg(self):
        result = -self.p1
        self.assertEqual(result.a, [0, -2])

    def test_eq(self):
        self.assertTrue(self.p0 == self.p0_v2)
        self.assertFalse(self.p1 == self.p2)

    def test_ne(self):
        self.assertFalse(self.p0 != self.p0_v2)
        self.assertTrue(self.p1 != self.p2)

    def test_eval(self):
        result = self.p1.eval(4)
        self.assertEqual(result, 8)

    def test_combine(self):
        result = self.p2.combine(self.p1)
        self.assertEqual(result.a, [1, 4, 12])

    def test_pow(self):
        result = self.p2**3
        self.assertEqual(result.a, [1, 6, 21, 44, 63, 54, 27])

    def test_diff(self):
        result = self.p2.diff()
        self.assertEqual(result.a, [2, 6])

    def test_integrate(self):
        result = self.p2.integrate(constant=5)
        self.assertEqual(result.a, [5, 1, 1, 1])

    def test_is_zero(self):
        self.assertTrue(self.p0.is_zero())
        self.assertFalse(self.p1.is_zero())

if __name__ == '__main__':
    unittest.main()