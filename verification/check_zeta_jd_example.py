"""Reproduce the ordinary class number in the (3, J_d) example using integers."""

from math import gcd, isqrt


def prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n) + 1))


def reduced_ideal_cycles(discriminant):
    """For the odd fundamental discriminant here, use (b + sqrt(D)) / (2a)."""
    root = isqrt(discriminant)
    ideals = set()
    for b in range(1, root + 1, 2):
        # Reduced means sqrt(D) - b < 2a < sqrt(D) + b.
        first = (root - b) // 2 + 1
        last = (root + b) // 2
        for a in range(first, last + 1):
            c, remainder = divmod(discriminant - b * b, 4 * a)
            if remainder == 0 and gcd(a, b, c) == 1:
                ideals.add((a, b))

    def successor(ideal):
        a, b = ideal
        quotient = (root + b) // (2 * a)
        next_b = 2 * a * quotient - b
        next_a, remainder = divmod(discriminant - next_b * next_b, 4 * a)
        if remainder:
            raise ArithmeticError(f"The successor of {ideal} has a nonintegral coefficient.")
        return next_a, next_b

    if {successor(ideal) for ideal in ideals} != ideals:
        raise ArithmeticError("Reduction must permute the reduced ideals.")
    remaining = set(ideals)
    cycles = []
    while remaining:
        start = min(remaining)
        ideal = start
        length = 0
        while ideal in remaining:
            remaining.remove(ideal)
            length += 1
            ideal = successor(ideal)
        if ideal != start:
            raise ArithmeticError(f"The cycle starting at {start} ended at {ideal}.")
        cycles.append((start, length))
    return len(ideals), cycles


if __name__ == "__main__":
    q, d, t, e = 43, 325079, 10, 3
    if not (prime(q) and prime(d) and d != 3):
        raise ValueError("The example requires primes q and d with d distinct from 3.")
    if q % 8 != 3 or d % 16 != 7:
        raise ValueError("The prime residues must be q = 3 modulo 8 and d = 7 modulo 16.")
    if any((d + 1) % p for p in (3, 5, 7, q)):
        raise ValueError("Each of 3, 5, 7 and q must divide d + 1.")
    if d + 1 != 2**3 * 3**3 * 5 * 7 * q:
        raise ArithmeticError("The factorisation of d + 1 differs from the example.")
    if not (2 * t + 1 < min(q, d) and 3 <= e < t and e % 2 == 1):
        raise ValueError("The small-prime cutoff and odd exponent must satisfy the host bounds.")
    discriminant = 3 * d
    count, cycles = reduced_ideal_cycles(discriminant)
    if count != 332:
        raise ArithmeticError(f"Expected 332 reduced ideals, found {count}.")
    if cycles != [((1, 987), 96), ((7, 975), 118), ((7, 985), 118)]:
        raise ArithmeticError(f"The reduced ideal cycles differ from the example: {cycles}")
    print(f"D = {discriminant}, reduced ideals = {count}")
    for start, length in cycles:
        print(f"cycle starting at {start}, length = {length}")
    print(f"ordinary class number = {len(cycles)}")
    host_modulus = 16 * q * d
    test_level = (max(192 * host_modulus, 1728) - 1).bit_length()
    if test_level != 36 or not (2 ** (test_level - 1) < 192 * host_modulus <= 2**test_level):
        raise ArithmeticError(f"The host modulus falls outside the expected dyadic level 36 (found {test_level}).")
    print(f"normalized length = 1; Case II level at dyadic layer two = {test_level}")
