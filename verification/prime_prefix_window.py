"""Certify a continuous window for the cyclic quartic target of conductor 15."""

from decimal import Decimal
from fractions import Fraction
from math import ceil, floor, isqrt

from translate_window_followup import (
    Q, ceil_div, euler_constant, legendre, log_bounds, log_derivative,
    period_sums, prime_powers,
)


def quartic_phase(n):
    if n % 3 == 0 or n % 5 == 0:
        return None
    phase = {1: 0, 2: 1, 4: 2, 3: 3}[n % 5]
    return (phase + 2 * (n % 3 == 2)) % 4


def centre():
    real, imag = (1, 0, -1, 0), (0, 1, 0, -1)
    phases = [quartic_phase(n) for n in range(1, 16)]
    u, v = period_sums([real[j] if j is not None else 0 for j in phases])
    w, s = period_sums([imag[j] if j is not None else 0 for j in phases])
    # -(v*u+s*w)/(u^2+w^2) is the real part of L'/L.
    def product(a, b):
        bounds = [x * y for x in a for y in b]
        return min(bounds), max(bounds)

    def square(a):
        return (0 if a[0] <= 0 <= a[1] else min(x*x for x in a),
                max(x*x for x in a))

    vu, sw = product(v, u), product(s, w)
    uu, ww = square(u), square(w)
    numer = -vu[1] - sw[1], -vu[0] - sw[0]
    denom = uu[0] + ww[0], uu[1] + ww[1]
    if denom[0] <= 0:
        raise ArithmeticError("The lower bound on the squared L-value must be positive.")
    bounds = [a / b for a in numer for b in denom]
    quad = log_derivative([legendre(n, 5) for n in range(1, 6)])
    gamma = euler_constant()
    return (Q + gamma[0] + floor((2*Q*min(bounds) + quad[0])/13),
            Q + gamma[1] + ceil((2*Q*max(bounds) + quad[1])/13))


def weights(p):
    """Return 13*A(p) and the exact sum of A(p^j)/p^j for j >= 2."""
    if p == 3:
        return 12, Fraction(1, p*(p-1)) + Fraction(1, 13*p*(p+1))
    if p == 5:
        return 13, Fraction(1, p*(p-1))
    order = (1, 4, 2, 4)[quartic_phase(p)]
    periodic = Fraction(1, p**order - 1)
    if order == 1:
        periodic -= Fraction(1, p)
    return 12 + 4*(order == 1), (Fraction(12, p*(p-1)) + 4*periodic)/13


def verify_curve(left, right, k, center_hi, knots, name):
    kq = int(k*Q)
    if kq != k*Q or kq % 4:
        raise ValueError("The coefficient times Q must be an integer divisible by four.")
    tl = th = mh = 0
    tested = []

    def test(a, b, label):
        # a/Q <= x <= b/Q. All quantities in the upper bound are in units 1/Q.
        log_lo = log_bounds(Decimal(a)/Q)[0]
        sqrt_hi = isqrt(b*Q) + 1
        upper = mh + center_hi - log_lo - tl*Q//b - kq*Q//sqrt_hi
        tested.append((upper, label))
        if upper >= 0:
            raise ArithmeticError(f"{name} has upper bound {Decimal(upper)/Q} at {label}.")

    crossings = 0
    quarter = kq//4
    for i, (n, lo, hi) in enumerate(knots):
        tl += lo//13
        th += ceil_div(hi, 13)
        mh += ceil_div(hi, 13*n)
        a = max(n, left)
        b = knots[i+1][0] if i+1 < len(knots) else right
        if a >= b:
            continue
        if a == left:
            test(left*Q, left*Q, "left endpoint")
        if b == right:
            test(right*Q, right*Q, "right endpoint")
        # The maximum inside this prime gap occurs at sqrt(x)=k/4+sqrt(t+k^2/16).
        sl = quarter + isqrt(tl*Q + quarter**2)
        sh = quarter + isqrt(th*Q + quarter**2) + 1
        zl, zh = sl**2//Q, ceil_div(sh**2, Q)
        if zl <= b*Q and zh >= a*Q:
            test(max(a*Q, zl), min(b*Q, zh), f"gap [{n},{b}]")
            crossings += 1
    if len(tested) != crossings + 2:
        raise ArithmeticError("The upper bound must cover both endpoints and every stationary candidate.")
    upper, where = max(tested)
    print(f"{name}: {len(knots)} knots <= {right}, {crossings} stationary candidates and two endpoints.")
    print(f"sup(({name}(x)-({k})*sqrt(x))/x) <= {Decimal(upper)/Q} ({where}).")


def main():
    left, right = 10_000, 1_000_000
    if left**3 != right**2:
        raise ValueError("The right endpoint must equal the left endpoint to the power 3/2.")
    primes = sorted(n for n, p in prime_powers(right).items() if n == p)
    cl, ch = centre()
    bl = bh = 0
    first, higher = [], []
    for p in primes:
        weight, tail = weights(p)
        lo, hi = log_bounds(p)
        bl += lo*tail.numerator // tail.denominator
        bh += ceil_div(hi*tail.numerator, tail.denominator)
        first.append((p, weight*lo, weight*hi))
        j, n = 2, p*p
        while n <= right:
            if p == 3:
                w = 13 + (-1)**j
            elif p == 5:
                w = 13
            else:
                w = 12 + 4*((j*quartic_phase(p)) % 4 == 0)
            higher.append((n, w*lo, w*hi))
            j, n = j+1, n*p
    print(f"C_psi in [{Decimal(cl)/Q}, {Decimal(ch)/Q}]")
    print(f"b_Z in [{Decimal(bl)/Q}, {Decimal(bh)/Q}]")
    verify_curve(left, right, 3, ch+bh, first, "W_Z")
    verify_curve(left, right, Fraction(1, 4), ch, sorted(first+higher), "F_psi")
    print(f"Both estimates hold for every real x in [{left}, {right}].")


if __name__ == "__main__":
    main()
