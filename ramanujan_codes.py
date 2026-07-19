"""
ramanujan_codes.py

A student-friendly Python exploration of several areas of Ramanujan's work
that can be investigated or partially verified with computers.

Topics included:
1. Ramanujan's rapid series for pi
2. Partition numbers and Ramanujan congruences
3. Rogers-Ramanujan identity coefficient check
4. Rogers-Ramanujan continued fraction
5. Divisor sums sigma(n)
6. Highly composite numbers
7. A mock-theta-style q-series coefficient generator

Pure Python, no third-party libraries required.
"""

from decimal import Decimal, getcontext
from math import factorial


# ============================================================
# 1. Ramanujan's rapid series for pi
# ============================================================

def ramanujan_pi(terms=3, precision=80):
    """
    Compute pi using Ramanujan's famous series:
        1/pi = (2*sqrt(2)/9801) * sum_{n>=0} (4n)! (1103+26390n) / ((n!)^4 396^(4n))
    """
    getcontext().prec = precision
    total = Decimal(0)

    for n in range(terms):
        num = Decimal(factorial(4 * n)) * Decimal(1103 + 26390 * n)
        den = (Decimal(factorial(n)) ** 4) * (Decimal(396) ** (4 * n))
        total += num / den

    factor = (Decimal(2) * Decimal(2).sqrt()) / Decimal(9801)
    inv_pi = factor * total
    return Decimal(1) / inv_pi


def demo_ramanujan_pi():
    print("=" * 70)
    print("1. Ramanujan's rapid series for pi")
    print("=" * 70)
    for t in range(1, 6):
        approx = ramanujan_pi(terms=t, precision=100)
        print(f"terms={t}")
        print(approx)
        print()


# ============================================================
# 2. Partition numbers and Ramanujan congruences
# ============================================================

def partition_numbers(n_max):
    """
    Compute partition numbers p(0), p(1), ..., p(n_max)
    using Euler's pentagonal number recurrence.
    """
    p = [0] * (n_max + 1)
    p[0] = 1

    for n in range(1, n_max + 1):
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2

            if g1 > n and g2 > n:
                break

            sign = 1 if k % 2 == 1 else -1

            if g1 <= n:
                total += sign * p[n - g1]
            if g2 <= n:
                total += sign * p[n - g2]

            k += 1

        p[n] = total

    return p


def check_ramanujan_congruences(limit=300):
    """
    Check:
        p(5k+4)  ≡ 0 mod 5
        p(7k+5)  ≡ 0 mod 7
        p(11k+6) ≡ 0 mod 11
    """
    print("=" * 70)
    print("2. Ramanujan partition congruences")
    print("=" * 70)

    p = partition_numbers(limit)
    ok5 = ok7 = ok11 = True

    for n in range(limit + 1):
        if n % 5 == 4 and p[n] % 5 != 0:
            print(f"FAILED mod 5 at n={n}, p(n)={p[n]}")
            ok5 = False
        if n % 7 == 5 and p[n] % 7 != 0:
            print(f"FAILED mod 7 at n={n}, p(n)={p[n]}")
            ok7 = False
        if n % 11 == 6 and p[n] % 11 != 0:
            print(f"FAILED mod 11 at n={n}, p(n)={p[n]}")
            ok11 = False

    print(f"mod 5  result: {ok5}")
    print(f"mod 7  result: {ok7}")
    print(f"mod 11 result: {ok11}")
    print()

    print("Sample partition values:")
    for n in range(min(20, limit + 1)):
        print(f"p({n}) = {p[n]}")
    print()


# ============================================================
# 3. Polynomial helpers for q-series work
# ============================================================

def poly_add(a, b, max_deg):
    out = [0] * (max_deg + 1)
    for i in range(max_deg + 1):
        av = a[i] if i < len(a) else 0
        bv = b[i] if i < len(b) else 0
        out[i] = av + bv
    return out


def poly_mul(a, b, max_deg):
    out = [0] * (max_deg + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            if i + j <= max_deg:
                out[i + j] += ai * bj
    return out


def poly_shift(a, k, max_deg):
    out = [0] * (max_deg + 1)
    for i, coeff in enumerate(a):
        if coeff != 0 and i + k <= max_deg:
            out[i + k] += coeff
    return out


def reciprocal_factor(power, max_deg):
    """
    Expansion of 1/(1 - q^power) up to q^max_deg.
    """
    out = [0] * (max_deg + 1)
    for k in range(0, max_deg // power + 1):
        out[k * power] = 1
    return out


def reciprocal_signed_factor(power, max_deg):
    """
    Expansion of 1/(1 + q^power) = 1 - q^power + q^(2 power) - ...
    """
    out = [0] * (max_deg + 1)
    k = 0
    while k * power <= max_deg:
        out[k * power] = -1 if k % 2 == 1 else 1
        k += 1
    return out


# ============================================================
# 4. Rogers-Ramanujan identity coefficient check
# ============================================================

def rogers_ramanujan_sum_side(max_deg=30, n_terms=20):
    """
    Left-hand side:
        sum_{n>=0} q^(n^2) / ((1-q)(1-q^2)...(1-q^n))
    """
    result = [0] * (max_deg + 1)
    denom_poly = [1] + [0] * max_deg

    for n in range(n_terms):
        if n > 0:
            denom_poly = poly_mul(denom_poly, reciprocal_factor(n, max_deg), max_deg)

        term = poly_shift(denom_poly, n * n, max_deg)
        result = poly_add(result, term, max_deg)

    return result


def rogers_ramanujan_product_side(max_deg=30):
    """
    Right-hand side:
        product_{m>=0} 1 / ((1-q^(5m+1))(1-q^(5m+4)))
    """
    result = [1] + [0] * max_deg
    m = 0

    while True:
        a = 5 * m + 1
        b = 5 * m + 4

        if a > max_deg and b > max_deg:
            break

        if a <= max_deg:
            result = poly_mul(result, reciprocal_factor(a, max_deg), max_deg)
        if b <= max_deg:
            result = poly_mul(result, reciprocal_factor(b, max_deg), max_deg)

        m += 1

    return result


def check_rogers_ramanujan_identity(max_deg=40, n_terms=20):
    print("=" * 70)
    print("3. Rogers-Ramanujan identity coefficient check")
    print("=" * 70)

    left = rogers_ramanujan_sum_side(max_deg=max_deg, n_terms=n_terms)
    right = rogers_ramanujan_product_side(max_deg=max_deg)

    all_ok = True
    for n in range(max_deg + 1):
        ok = left[n] == right[n]
        print(f"q^{n:2d}: left={left[n]:4d}, right={right[n]:4d}, match={ok}")
        if not ok:
            all_ok = False

    print()
    print("All coefficients matched:", all_ok)
    print()


# ============================================================
# 5. Rogers-Ramanujan continued fraction
# ============================================================

def rogers_ramanujan_continued_fraction(q, depth=50):
    """
    Approximate:
        R(q) = q^(1/5) / (1 + q/(1 + q^2/(1 + q^3/(1 + ... ))))
    """
    value = 0.0
    for n in range(depth, 0, -1):
        value = (q ** n) / (1.0 + value)
    return (q ** 0.2) / (1.0 + value)


def demo_rr_continued_fraction(q=0.2):
    print("=" * 70)
    print("4. Rogers-Ramanujan continued fraction")
    print("=" * 70)
    for depth in [5, 10, 20, 50, 100]:
        val = rogers_ramanujan_continued_fraction(q, depth)
        print(f"depth={depth:3d} -> R({q}) = {val}")
    print()


# ============================================================
# 6. Divisor sums and highly composite numbers
# ============================================================

def sigma(n):
    """
    Sum of positive divisors of n.
    """
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
        d += 1
    return total


def tau(n):
    """
    Number of positive divisors of n.
    """
    count = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            count += 1 if d * d == n else 2
        d += 1
    return count


def highly_composite_numbers(limit=100):
    """
    Return all highly composite numbers up to 'limit'.
    A highly composite number has more divisors than any smaller positive integer.
    """
    result = []
    best_so_far = 0
    for n in range(1, limit + 1):
        d = tau(n)
        if d > best_so_far:
            result.append((n, d))
            best_so_far = d
    return result


def demo_divisors_and_hcn(limit=100):
    print("=" * 70)
    print("5. Divisor functions and highly composite numbers")
    print("=" * 70)
    print("Sample sigma(n) values:")
    for n in range(1, min(limit, 20) + 1):
        print(f"n={n:2d}, sigma(n)={sigma(n):3d}, tau(n)={tau(n):2d}")

    print()
    print(f"Highly composite numbers up to {limit}:")
    hcn = highly_composite_numbers(limit)
    for n, d in hcn:
        print(f"{n:3d} has {d:2d} divisors")
    print()


# ============================================================
# 7. Mock-theta-style q-series exploration
# ============================================================

def mock_theta_like_series(max_deg=30, n_terms=15):
    """
    Compute coefficients of a mock-theta-style truncated series:
        sum_{n>=0} q^(n^2) / (-q; q)_n^2
    where (-q; q)_n = (1+q)(1+q^2)...(1+q^n)

    This is not a full theory implementation, but a student-friendly computational exploration.
    """
    result = [0] * (max_deg + 1)

    for n in range(n_terms):
        denom = [1] + [0] * max_deg
        for k in range(1, n + 1):
            factor = reciprocal_signed_factor(k, max_deg)
            denom = poly_mul(denom, factor, max_deg)
            denom = poly_mul(denom, factor, max_deg)  # square it

        shifted = [0] * (max_deg + 1)
        for i, coeff in enumerate(denom):
            if i + n * n <= max_deg:
                shifted[i + n * n] += coeff

        result = poly_add(result, shifted, max_deg)

    return result


def demo_mock_theta_like(max_deg=25, n_terms=12):
    print("=" * 70)
    print("6. Mock-theta-style q-series coefficients")
    print("=" * 70)
    coeffs = mock_theta_like_series(max_deg=max_deg, n_terms=n_terms)
    for i, c in enumerate(coeffs):
        print(f"coefficient of q^{i:2d} = {c}")
    print()


# ============================================================
# 8. Run everything
# ============================================================

def run_all():
    demo_ramanujan_pi()
    check_ramanujan_congruences(100)
    check_rogers_ramanujan_identity(30, 15)
    demo_rr_continued_fraction(0.2)
    demo_divisors_and_hcn(100)
    demo_mock_theta_like(20, 10)
    demo_partition_asymptotic()
    demo_tau_function()


# ============================================================
# 7. Partition asymptotic formula (Hardy--Ramanujan)
# ============================================================

def demo_partition_asymptotic():
    """Compare exact partition numbers against the Hardy-Ramanujan asymptotic."""
    import math
    print("=" * 70)
    print("7. Partition asymptotic formula (Hardy--Ramanujan)")
    print("=" * 70)

    # Exact partition numbers (computed via pentagonal number recurrence)
    p = partition_numbers(50)

    print(f"{'n':>4s}  {'p(n)':>10s}  {'Approx':>14s}  {'Ratio':>8s}")
    print("-" * 45)
    for n in range(2, 51):
        exact = p[n]
        approx = math.exp(math.pi * math.sqrt(2 * n / 3)) / (4 * n * math.sqrt(3))
        ratio = exact / approx
        print(f"{n:4d}  {exact:10d}  {approx:14.2f}  {ratio:8.6f}")

    print()
    print("The ratio approaches 1 as n increases.")
    print()


# ============================================================
# 8. Ramanujan's tau function
# ============================================================

def compute_tau(n_max):
    """
    Compute tau(n) for n = 1, ..., n_max.
    Uses the recurrence from the q-expansion of delta(q) = q * Product(1-q^n)^24.
    
    tau(1) = 1
    For n > 1:
        tau(n) = sigma_11(n) - 24*tau(n-1) - 66*tau(n-2) - 96*tau(n-3) 
                 - 126*tau(n-4) - 146*tau(n-5) - 126*tau(n-6) 
                 - 96*tau(n-7) - 66*tau(n-8) - 24*tau(n-9) - tau(n-11)
    
    where the coefficients come from the expansion of q*Product(1-q^n)^24.
    
    Actually, we use the simpler recurrence:
    tau(n) = sum_{k=1}^{n} k^11 * tau(n-k) is WRONG.
    
    Correct approach: use the Euler pentagonal-type recurrence for the 
    discriminant function.
    """
    tau = [0] * (n_max + 1)
    tau[1] = 1
    
    # Use the recurrence derived from: 
    # Delta(q) = sum tau(n) q^n = q * prod(1-q^n)^24
    # Taking log derivative and matching coefficients gives:
    # n * tau(n) = sum_{k=1}^{n} (sigma_11(k) - k^11) * tau(n-k) ... no.
    
    # Correct recurrence: from the identity
    # q * f'(q) = -24 * q * f(q) * sum_{n=1}^{inf} n*q^n/(1-q^n)
    # where f(q) = prod(1-q^n)^24
    # This gives: n*tau(n) = sum_{k=1}^{n} sigma_11(k) * tau(n-k)
    # but with tau(0) = 0, so for n >= 1:
    # tau(n) = (1/n) * sum_{k=1}^{n} sigma_11(k) * tau(n-k)
    # But tau(0) = 0, so we need a different formulation.
    
    # Actually: Delta = eta^24, and eta = q^(1/24) * prod(1-q^n)
    # The recurrence is:
    # n * tau(n) = sum_{k=1}^{n} sigma_11(k) * tau(n-k)
    # With tau(0) = 0, this means tau(n) = (1/n) * sum_{k=1}^{n-1} sigma_11(k)*tau(n-k) + sigma_11(n)*tau(0)
    # Since tau(0)=0, we get: tau(n) = (1/n) * sum_{k=1}^{n-1} sigma_11(k) * tau(n-k)
    # But this gives tau(1) = 0 which is wrong.
    
    # Let me use the standard recurrence properly:
    # From the differential equation for Delta:
    # sum_{k=0}^{n} (n-k) * tau(n-k) * a_k = 0  where a_k are coeffs of eta^24
    # This is getting complicated. Let me just use the direct product expansion.
    
    # Direct computation: Delta(q) = q * Product_{n=1}^{inf} (1-q^n)^24
    # Expand as polynomial multiplication
    
    # Start with [1] (representing 1)
    # Multiply by (1 - q^n)^24 for n = 1, 2, ...
    # Then shift by q^1
    
    # (1 - q^n)^24 = sum_{k=0}^{24} binomial(24,k) * (-1)^k * q^(n*k)
    
    from math import comb
    
    # Build the product coefficients
    # coeffs[q^k] = coefficient of q^k in Product(1-q^n)^24
    coeffs = [0] * (n_max + 1)
    coeffs[0] = 1  # start with 1
    
    for n in range(1, n_max + 1):
        # Multiply by (1 - q^n)^24
        # (1 - q^n)^24 = 1 - 24*q^n + 276*q^(2n) - ... 
        new_coeffs = coeffs[:]
        for k in range(1, min(25, n_max // n + 1)):
            sign = (-1) ** k
            coeff = comb(24, k) * sign
            for j in range(n_max - k * n + 1):
                if coeffs[j] != 0:
                    new_coeffs[j + k * n] += coeff * coeffs[j]
        coeffs = new_coeffs
        
        # Stop early if we have enough terms
        if n > 1 and coeffs[n] != 0 and n <= n_max:
            pass  # keep going
    
    # Now coeffs[k] is the coefficient of q^k in prod(1-q^n)^24
    # Delta = q * prod(1-q^n)^24, so tau(n) = coeffs[n-1]
    for n in range(1, n_max + 1):
        if n - 1 < len(coeffs):
            tau[n] = coeffs[n - 1]
    
    return tau


def sigma_11(n):
    """Sum of 11th powers of divisors of n."""
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += d ** 11
            if d != n // d:
                total += (n // d) ** 11
        d += 1
    return total


def compute_tau_recurrence(n_max):
    """
    Compute tau(n) using the recurrence:
    n * tau(n) = sum_{k=1}^{n} sigma_11(k) * tau(n-k)
    
    With tau(0) = 0, tau(1) = 1.
    For n=1: 1*tau(1) = sigma_11(1)*tau(0) = 0, but tau(1)=1.
    
    The correct recurrence comes from the Ramanujan identity for the 
    discriminant function. Let me use:
    
    tau(n) = sigma_11(n-1) + ... 
    
    Actually the simplest correct approach:
    n * tau(n) = sum_{k=1}^{n} k^11 * tau(n-k) is WRONG.
    
    CORRECT: From the q-expansion of Delta, using the identity:
    Delta = sum_{n>=1} tau(n) q^n = q * Product(1-q^n)^24
    
    Using the recurrence from the logarithmic derivative:
    n * tau(n) = sum_{k=1}^{n} chi(k) * tau(n-k)
    
    where chi(k) = k^11 if k is odd, 0 if k is even.
    
    Hmm, that's also not quite right. Let me just use the direct product.
    """
    tau = [0] * (n_max + 1)
    tau[1] = 1
    
    # Use the direct product expansion approach
    from math import comb
    
    # We want: Delta(q) = q * Product_{n=1}^{inf} (1 - q^n)^24
    # = sum_{n=1}^{inf} tau(n) q^n
    
    # Build Product(1-q^n)^24 step by step
    # Start with polynomial [1] representing constant 1
    poly = [0] * (n_max + 1)
    poly[0] = 1
    
    for n in range(1, n_max + 1):
        # Multiply poly by (1 - q^n)^24
        # (1 - q^n)^24 = sum_{k=0}^{24} C(24,k)*(-1)^k * q^(n*k)
        
        new_poly = poly[:]
        for k in range(1, 25):
            nk = n * k
            if nk > n_max:
                break
            coeff = comb(24, k) * ((-1) ** k)
            # Convolve: new_poly[j+nk] += coeff * poly[j]
            for j in range(n_max + 1 - nk):
                if poly[j] != 0:
                    new_poly[j + nk] += coeff * poly[j]
        poly = new_poly
        
        # Once we've processed enough terms, we can extract tau
        if n >= 2 and poly[n - 1] != 0:
            pass  # continuing
    
    # tau(n) = poly[n-1] since Delta = q * poly
    for n in range(1, n_max + 1):
        if n - 1 < len(poly):
            tau[n] = poly[n - 1]
    
    return tau


def demo_tau_function():
    """Demonstrate Ramanujan's tau function and its properties."""
    print("=" * 70)
    print("8. Ramanujan's tau function")
    print("=" * 70)
    
    tau = compute_tau_recurrence(30)
    
    print("First 30 values of tau(n):")
    print(f"{'n':>4s}  {'tau(n)':>10s}  {'|tau|':>8s}  {'Bound':>12s}  {'OK'}")
    print("-" * 50)
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    prime_set = set(primes)
    
    all_ok = True
    for n in range(1, 31):
        val = tau[n]
        abs_val = abs(val)
        if n in prime_set:
            bound = 2 * (n ** 5.5)
            ok = abs_val <= bound
            if not ok:
                all_ok = False
            print(f"{n:4d}  {val:10d}  {abs_val:8d}  {bound:12.0f}  {'YES' if ok else 'NO'}")
        else:
            print(f"{n:4d}  {val:10d}")
    
    print()
    print("Checking multiplicativity (tau(mn) = tau(m)*tau(n) for coprime m,n):")
    print(f"{'m':>4s}  {'n':>4s}  {'mn':>5s}  {'tau(mn)':>10s}  {'tau(m)*tau(n)':>15s}  {'Match'}")
    print("-" * 60)
    
    for m in range(2, 10):
        for n in range(m + 1, 10):
            # Check coprime
            a, b = m, n
            while b:
                a, b = b, a % b
            if a == 1:  # coprime
                mn = m * n
                if mn < len(tau):
                    lhs = tau[mn]
                    rhs = tau[m] * tau[n]
                    match = lhs == rhs
                    print(f"{m:4d}  {n:4d}  {mn:5d}  {lhs:10d}  {rhs:15d}  {'YES' if match else 'NO'}")
    
    print()
    print("Ramanujan's bound |tau(p)| <= 2*p^(11/2) holds:", all_ok)
    print()


if __name__ == "__main__":
    run_all()