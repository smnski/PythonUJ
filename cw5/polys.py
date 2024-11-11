import unittest

class Polynomial:
    def is_zero(poly: list) -> bool:
        return all(coef == 0 for coef in poly)
    
    def eq_poly(poly1: list, poly2: list) -> bool:
        return poly1 == poly2
    
    def add_poly(poly1: list, poly2: list) -> list:
        max_length = max(len(poly1), len(poly2))
        poly1_extended = poly1 + [0] * (max_length - len(poly1))
        poly2_extended = poly2 + [0] * (max_length - len(poly2))
    
        result = [poly1_extended[i] + poly2_extended[i] for i in range(max_length)]
        return result
    
    def sub_poly(poly1: list, poly2: list) -> list:
        max_length = max(len(poly1), len(poly2))
        poly1_extended = poly1 + [0] * (max_length - len(poly1))
        poly2_extended = poly2 + [0] * (max_length - len(poly2))
    
        result = [poly1_extended[i] - poly2_extended[i] for i in range(max_length)]
        return result
    
    def mul_poly(poly1: list, poly2: list) -> list:
        result_length = len(poly1) + len(poly2) - 1
        result = [0] * result_length

        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i + j] += poly1[i] * poly2[j]
    
        return result
    
    def pow_poly(poly: list, pow: int) -> list:
        result = [1]

        for _ in range(pow):
            result = Polynomial.mul_poly(result, poly)

        return result
    
    def eval_poly(poly: list, point: float):
        result = 0
        for coef in reversed(poly):
            result = result * point + coef

        return result
    
    def diff_poly(poly: list) -> list:
        derivative = [i * poly[i] for i in range(1, len(poly))]
        return derivative
    
    def combine_poly(poly1: list, poly2: list) -> list:
        result = [0]
        temp_poly = [1]
        for coef in poly1:
            term = [c * coef for c in temp_poly]
            result = Polynomial.add_poly(result, term)
            temp_poly = Polynomial.mul_poly(temp_poly, poly2)

        return result
    
class TestPolynomials(unittest.TestCase):
    p0 = [0, 0, 0]   # W(x) = 0
    p1 = [0, 1]      # W(x) = x
    p2 = [0, 0, 1]   # W(x) = x^2
    p3 = [1, 2, 3]   # W(x) = 1 + 2x + 3x^2

    def test_add_poly(self):
        result = Polynomial.add_poly(self.p1, self.p2)
        self.assertEqual(result, [0, 1, 1])

    def test_sub_poly(self):
        result = Polynomial.sub_poly(self.p3, self.p2)
        self.assertEqual(result, [1, 2, 2])

    def test_mul_poly(self):
        result = Polynomial.mul_poly(self.p1, self.p2)
        self.assertEqual(result, [0, 0, 0, 1])

    def test_is_zero(self):
        self.assertTrue(Polynomial.is_zero(self.p0))
        self.assertFalse(Polynomial.is_zero(self.p1))

    def test_eq_poly(self):
        self.assertTrue(Polynomial.eq_poly(self.p1, self.p1))
        self.assertFalse(Polynomial.eq_poly(self.p1, self.p3))

    def test_eval_poly(self):
        result = Polynomial.eval_poly(self.p2, 3)
        self.assertEqual(result, 9)

        result = Polynomial.eval_poly(self.p3, 2)
        self.assertEqual(result, 17)

    def test_combine_poly(self):
      result = Polynomial.combine_poly(self.p3, self.p1)
      self.assertEqual(result, [1, 2, 3])
    
      result = Polynomial.combine_poly(self.p3, self.p2)
      self.assertEqual(result, [1, 0, 2, 0, 3])

    def test_pow_poly(self):
      result = Polynomial.pow_poly(self.p2, 2)
      self.assertEqual(result, [0, 0, 0, 0, 1])

      result = Polynomial.pow_poly(self.p3, 3)
      self.assertEqual(result, [1, 6, 21, 44, 63, 54, 27])

    def test_diff_poly(self):
        result = Polynomial.diff_poly(self.p3)
        self.assertEqual(result, [2, 6])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()