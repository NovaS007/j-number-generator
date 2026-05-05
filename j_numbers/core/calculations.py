from functools import lru_cache
from . import factorizations as f


@lru_cache(maxsize=1000000)
def _get_cached_factors_and_is_prime(j_num):
    """
    Cache prime factorization and primality. Computes both at once.
    Returns (prime_factors_tuple, is_prime_flag)
    """
    if j_num < 2:
        return (), 0

    factors_tuple = f.findPrimeFactors(j_num)
    is_prime = 1 if len(factors_tuple) == 1 else 0
    return factors_tuple, is_prime


def _precompute_base_powers(base, max_repeat):
    """Pre-compute powers of base to avoid recalculation."""
    return {k: base ** k for k in range(max_repeat + 2)}


def getAllJNums(max_repeat, base=10):
    """
    Returns all unique J_k(a,b,c) values for every 3-digit seed abc in the given base.

    OPTIMIZATIONS:
    - Pre-computed base powers
    - Cached factorization with @lru_cache
    - Efficient digit extraction
    """
    if max_repeat < 0:
        raise ValueError("max_repeat must be >= 0")
    if base < 2:
        raise ValueError("base must be >= 2")

    results = {}
    base_powers = _precompute_base_powers(base, max_repeat)
    upper_index = base**3 - 1
    base_squared = base ** 2
    divisor = base - 1

    for index in range(upper_index + 1):
        a = index // base_squared
        b = (index // base) % base
        c = index % base

        for k in range(max_repeat + 1):
            base_k = base_powers[k]
            base_k_plus_1 = base_powers[k + 1]

            repeated_c = c * (base_k - 1) // divisor if k > 0 else 0
            j_num = a * base_k_plus_1 + b * base_k + repeated_c

            if j_num not in results:
                prime_factors, is_prime = _get_cached_factors_and_is_prime(j_num)

                results[j_num] = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "k": k,
                    "prime_factors": list(prime_factors),
                    "is_prime": is_prime,
                }

    return results


def getJNumsForSeed(a, b, c, max_repeat, base=10):
    """Compute J_k(a,b,c) for k = 0..max_repeat for a single seed."""
    if max_repeat < 0:
        raise ValueError("max_repeat must be >= 0")
    if base < 2:
        raise ValueError("base must be >= 2")

    for name, v in (("a", a), ("b", b), ("c", c)):
        if not isinstance(v, int):
            raise TypeError(f"{name} must be an int in [0, {base-1}]")
        if v < 0 or v >= base:
            raise ValueError(f"{name} must be in range 0..{base-1} for base {base}")

    results = {}
    base_powers = _precompute_base_powers(base, max_repeat)
    divisor = base - 1

    for k in range(max_repeat + 1):
        base_k = base_powers[k]
        base_k_plus_1 = base_powers[k + 1]

        repeated_c = c * (base_k - 1) // divisor if k > 0 else 0
        j_num = a * base_k_plus_1 + b * base_k + repeated_c

        if j_num not in results:
            prime_factors, is_prime = _get_cached_factors_and_is_prime(j_num)

            results[j_num] = {
                "a": a,
                "b": b,
                "c": c,
                "k": k,
                "prime_factors": list(prime_factors),
                "is_prime": is_prime,
            }
    return results


def getJNumsForAB(a, b, max_repeat, base=10):
    """Fast path when a and b are fixed and c ranges over 0..base-1."""
    if max_repeat < 0:
        raise ValueError("max_repeat must be >= 0")
    if base < 2:
        raise ValueError("base must be >= 2")

    for name, v in (("a", a), ("b", b)):
        if not isinstance(v, int):
            raise TypeError(f"{name} must be an int in [0, {base-1}]")
        if v < 0 or v >= base:
            raise ValueError(f"{name} must be in range 0..{base-1} for base {base}")

    results = {}
    base_powers = _precompute_base_powers(base, max_repeat)
    divisor = base - 1

    for c in range(base):
        for k in range(max_repeat + 1):
            base_k = base_powers[k]
            base_k_plus_1 = base_powers[k + 1]

            repeated_c = c * (base_k - 1) // divisor if k > 0 else 0
            j_num = a * base_k_plus_1 + b * base_k + repeated_c

            if j_num not in results:
                prime_factors, is_prime = _get_cached_factors_and_is_prime(j_num)

                results[j_num] = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "k": k,
                    "prime_factors": list(prime_factors),
                    "is_prime": is_prime,
                }
    return results