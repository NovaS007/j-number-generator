import sympy as sp
from functools import lru_cache


@lru_cache(maxsize=1000000)
def findPrimeFactors(num):
    """
    Returns a list of prime factors (with repetition for exponents).
    Results are cached for performance.
    Example: 12 -> [2, 2, 3]
    """
    if num < 2:
        return ()  # Return tuple for hashability with lru_cache

    factors = []
    # sp.factorint returns dict of {prime: exponent}
    for prime, exp in sp.factorint(num).items():
        factors.extend([prime] * exp)

    return tuple(factors)  # Return tuple (immutable, hashable)
