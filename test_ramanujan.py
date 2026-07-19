import unittest
from decimal import Decimal, getcontext
import math

from ramanujan_codes import (
    ramanujan_pi,
    partition_numbers,
    poly_add,
    poly_mul,
    poly_shift,
    reciprocal_factor,
    reciprocal_signed_factor,
    rogers_ramanujan_sum_side,
    rogers_ramanujan_product_side,
    rogers_ramanujan_continued_fraction,
    sigma,
    tau,
    highly_composite_numbers,
    mock_theta_like_series,
    compute_tau,
    compute_tau_recurrence,
)


class TestRamanujanCodes(unittest.TestCase):

    def test_ramanujan_pi(self):
        # 4 terms of Ramanujan's pi series should yield over 30 correct decimal places.
        # Check against standard math.pi digits up to 30 places.
        approx = ramanujan_pi(terms=4, precision=60)
        expected_pi_str = "3.141592653589793238462643383279"
        self.assertTrue(str(approx).startswith(expected_pi_str))

    def test_partition_numbers(self):
        # Compute partitions up to n=20
        p = partition_numbers(20)
        # Expected partition values for p(0) to p(10) and p(20)
        expected_small = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
        self.assertEqual(p[:11], expected_small)
        self.assertEqual(p[20], 627)

    def test_partition_congruences(self):
        p = partition_numbers(100)
        for n in range(101):
            if n % 5 == 4:
                self.assertEqual(p[n] % 5, 0, f"Congruence mod 5 failed at n={n}")
            if n % 7 == 5:
                self.assertEqual(p[n] % 7, 0, f"Congruence mod 7 failed at n={n}")
            if n % 11 == 6:
                self.assertEqual(p[n] % 11, 0, f"Congruence mod 11 failed at n={n}")

    def test_poly_add(self):
        a = [1, 2, 3]
        b = [0, 5]
        res = poly_add(a, b, 4)
        self.assertEqual(res, [1, 7, 3, 0, 0])

    def test_poly_mul(self):
        # (1 + q) * (1 - q) = 1 - q^2
        a = [1, 1]
        b = [1, -1]
        res = poly_mul(a, b, 3)
        self.assertEqual(res, [1, 0, -1, 0])

    def test_poly_shift(self):
        a = [2, 3]
        res = poly_shift(a, 2, 4)
        self.assertEqual(res, [0, 0, 2, 3, 0])

    def test_reciprocal_factor(self):
        # 1 / (1 - q^2) = 1 + q^2 + q^4 + q^6 + ...
        res = reciprocal_factor(2, 5)
        self.assertEqual(res, [1, 0, 1, 0, 1, 0])

    def test_reciprocal_signed_factor(self):
        # 1 / (1 + q^2) = 1 - q^2 + q^4 - q^6 + ...
        res = reciprocal_signed_factor(2, 5)
        self.assertEqual(res, [1, 0, -1, 0, 1, 0])

    def test_rogers_ramanujan_identities(self):
        # Check Rogers-Ramanujan coefficients up to q^20
        max_deg = 20
        left = rogers_ramanujan_sum_side(max_deg=max_deg, n_terms=10)
        right = rogers_ramanujan_product_side(max_deg=max_deg)
        self.assertEqual(left, right)

    def test_rogers_ramanujan_cf(self):
        # Depth 50 convergence at q=0.2
        val = rogers_ramanujan_continued_fraction(0.2, depth=50)
        self.assertAlmostEqual(val, 0.6078498293966815, places=12)

    def test_divisors_sigma_tau(self):
        # divisors of 6 are 1, 2, 3, 6 (sum = 12, count = 4)
        self.assertEqual(sigma(6), 12)
        self.assertEqual(tau(6), 4)
        # divisors of 12 are 1, 2, 3, 4, 6, 12 (sum = 28, count = 6)
        self.assertEqual(sigma(12), 28)
        self.assertEqual(tau(12), 6)

    def test_highly_composite_numbers(self):
        hcn = highly_composite_numbers(100)
        expected = [
            (1, 1), (2, 2), (4, 3), (6, 4), (12, 6),
            (24, 8), (36, 9), (48, 10), (60, 12)
        ]
        self.assertEqual(hcn, expected)

    def test_mock_theta_like_series(self):
        # Check first 5 coefficients of mock-theta-like series
        coeffs = mock_theta_like_series(max_deg=5, n_terms=5)
        expected = [1, 1, -2, 3, -3, 3]
        self.assertEqual(coeffs, expected)

    def test_tau_function(self):
        # First 10 expected values of tau(n):
        expected_tau = [
            1, -24, 252, -1472, 4830, -6048, -16744, 84480, -113643, -115920
        ]
        # Test direct product computation method
        tau_prod = compute_tau(10)
        self.assertEqual(tau_prod[1:11], expected_tau)

        # Test recurrence-based computation method
        tau_rec = compute_tau_recurrence(10)
        self.assertEqual(tau_rec[1:11], expected_tau)

    def test_tau_multiplicativity_and_bounds(self):
        tau_vals = compute_tau(30)
        # Multiplicativity: tau(2 * 3) = tau(2) * tau(3) since 2 and 3 are coprime
        self.assertEqual(tau_vals[6], tau_vals[2] * tau_vals[3])
        self.assertEqual(tau_vals[15], tau_vals[3] * tau_vals[5])

        # Prime bounds: |tau(p)| <= 2 * p^(11/2) for prime p=2, 3, 5
        for p in [2, 3, 5]:
            bound = 2 * (p ** 5.5)
            self.assertTrue(abs(tau_vals[p]) <= bound)


if __name__ == "__main__":
    unittest.main()
