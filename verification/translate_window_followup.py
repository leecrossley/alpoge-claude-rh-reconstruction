"""Outward bounds for the zeta ramp and its four-twist sum on [9^4, 27^4]."""

from decimal import Decimal, getcontext
from fractions import Fraction
from functools import cache
from itertools import accumulate
from math import ceil, floor, isqrt


Q = 10**24
RATIO_SCALE = 10**9
getcontext().prec = 60


def ceil_div(a, b):
    return -((-a) // b)


@cache
def log_bounds(n):
    """Integer endpoints in units of 1/Q; Decimal.ln is correctly rounded."""
    if n == 1:
        return 0, 0
    middle = int(Decimal(n).ln() * Q)
    return middle - 1, middle + 2


def euler_constant():
    m = 10**6
    harmonic = sum(Q // n for n in range(1, m + 1))
    low, high = log_bounds(m)
    # The trapezoid remainders for 1/t have total in [0, 1/m^2].
    return (harmonic - high - ceil_div(Q, 2 * m),
            harmonic + m - low - Q // (2 * m) + ceil_div(Q, m * m))


def legendre(n, p):
    value = pow(n % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def period_sums(period):
    """Enclose sums of a(n)/n and a(n)log(n)/n for a zero-mean signed period."""
    q = len(period)
    prefix = list(accumulate(period))
    if not prefix or prefix[-1] != 0:
        raise ValueError("The signed period must be nonempty and have sum zero.")
    mean = Fraction(sum(prefix), q)
    discrepancy = max(abs(v) for v in accumulate(a - mean for a in prefix))
    m = ceil_div(100_000, q) * q
    l_low = l_high = f_low = f_high = 0
    for n in range(1, m + 1):
        sign = period[(n - 1) % q]
        if not sign:
            continue
        low, high = log_bounds(n)
        if sign == 1:
            l_low += Q // n
            l_high += ceil_div(Q, n)
            f_low += low // n
            f_high += ceil_div(high, n)
        else:
            l_low -= ceil_div(Q, n)
            l_high -= Q // n
            f_low -= ceil_div(high, n)
            f_high -= low // n

    # Partial summation twice. f is 1/t or log(t)/t and f(t)-f(t+1)
    # is positive decreasing here. The first periodic mean is kept exactly.
    t = m + 1
    low, high = (Fraction(value, Q) for value in log_bounds(t))
    l = (Fraction(l_low, Q) + mean / t - discrepancy / t**2,
         Fraction(l_high, Q) + mean / t + discrepancy / t**2)
    f = (Fraction(f_low, Q) + min(mean * low, mean * high) / t - discrepancy * high / t**2,
         Fraction(f_high, Q) + max(mean * low, mean * high) / t + discrepancy * high / t**2)
    return l, f


def log_derivative(period):
    """Enclose L'(1)/L(1) for the real, nonprincipal periodic character."""
    l, f = period_sums(period)
    if l[0] <= 0:
        raise ArithmeticError("The lower bound for L(1) must be positive.")
    ratios = [-v / w for v in f for w in l]
    return floor(Q * min(ratios)), ceil(Q * max(ratios))


def prime_powers(limit):
    sieve = bytearray(b'\x01') * (limit + 1)
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes((limit - p * p) // p + 1)
    bases = {}
    for p in range(2, limit + 1):
        if sieve[p]:
            r = p
            while r <= limit:
                bases[r] = p
                r *= p
    return bases


def verify_ramp(name, bases, fourth_powers, center, coefficient, *, absolute_character=False):
    a = min(fourth_powers)
    slope_low, slope_high = center
    mass_low = mass_high = 0
    sample_lower = None
    max_upper = gaps = 0
    previous = None
    knots = set(fourth_powers)
    knots.update(r for r in bases if coefficient(r))
    for x in sorted(knots):
        if x in bases:
            c = coefficient(x)
            low, high = log_bounds(bases[x])
            lower_mass, upper_mass = sorted((c * low, c * high))
            slope_low += lower_mass // x
            slope_high += ceil_div(upper_mass, x)
            mass_low += lower_mass
            mass_high += upper_mass
        if x < a:
            continue
        log_low, log_high = (0, 0) if absolute_character else log_bounds(x)
        low = x * (slope_low - log_high) - mass_high
        high = x * (slope_high - log_low) - mass_low
        if x in (19**4, 20**4, 21**4, 24**4) and not absolute_character:
            print(f"  at {x}: [{Decimal(low) / Q}, {Decimal(high) / Q}]")
        if absolute_character:
            low, high = max(low, -high, 0), max(-low, high)
        root = isqrt(x * Q**2)
        if low > 0:
            knot_lower = RATIO_SCALE * low // (root + 1)
            if sample_lower is None or knot_lower > sample_lower[0]:
                sample_lower = knot_lower, x
        knot_upper = ceil_div(RATIO_SCALE * max(high, 0), root)
        if previous is not None:
            left, left_root, left_upper = previous
            curvature = 0 if absolute_character else ceil_div(
                RATIO_SCALE * (x - left)**2 * Q, 8 * left * left_root)
            max_upper = max(max_upper, max(left_upper, knot_upper) + curvature)
            gaps += 1
        previous = x, root, knot_upper
    if sample_lower is None or sample_lower[0] > max_upper:
        raise ArithmeticError(f"The lower witness for {name} is missing or exceeds the upper bound.")
    print(f"{name}: {gaps} adjacent intervals, bounds on the supremum of the normalized ramp")
    print(f"  [{Decimal(sample_lower[0]) / RATIO_SCALE}, "
          f"{Decimal(max_upper) / RATIO_SCALE}], lower witness x={sample_lower[1]}")
    return max_upper


def main():
    knots = {n**4 for n in range(9, 28)}
    bases = prime_powers(max(knots))
    gamma = euler_constant()
    center = (Q + gamma[0], Q + gamma[1])
    zeta_upper = verify_ramp("zeta", bases, knots, center, lambda _: 1)
    if 1000 * zeta_upper >= 35 * RATIO_SCALE:
        raise ArithmeticError("The zeta upper bound must be strictly below 35/1000.")
    q, d = 3, 23
    lq = log_derivative([legendre(n, q) for n in range(1, q + 1)])
    ld = log_derivative([legendre(n, d) for n in range(1, d + 1)])
    lqd = log_derivative([legendre(n, q) * legendre(n, d) for n in range(1, q * d + 1)])
    characters = (
        (q, lq, lambda n: legendre(n, q)),
        (d, ld, lambda n: legendre(n, d)),
        (q * d, lqd, lambda n: legendre(n, q) * legendre(n, d)),
    )
    for modulus, (low, high), char in characters:
        print(f"L'/L, conductor {modulus}: [{Decimal(low) / Q}, {Decimal(high) / Q}]")
        verify_ramp(f"|G|, conductor {modulus}", bases, knots, (low, high), char,
                    absolute_character=True)
    four_center = (center[0] + lq[0] - ld[1] - lqd[1],
                   center[1] + lq[1] - ld[0] - lqd[0])

    def selected(n):
        return (1 + legendre(n, q)) * (1 - legendre(n, d))

    four_upper = verify_ramp("four twists (3,23)", bases, knots, four_center, selected)
    if 100 * four_upper >= 107 * RATIO_SCALE:
        raise ArithmeticError("The four-twist upper bound must be strictly below 107/100.")


if __name__ == "__main__":
    main()
