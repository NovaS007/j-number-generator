from . import factorizations as f


def getAllJNums(max_repeat, base=10):
    """
    Returns all unique J_k(a,b,c) values for every 3-digit seed abc in the given base,
    for every k from 0 up to max_repeat.

    J_k(a,b,c) = ab followed by c repeated k times

    Examples in base 10:
        k = 0 -> ab
        k = 1 -> abc
        k = 2 -> abcc
        k = 3 -> abccc
    """
    if max_repeat < 0:
        raise ValueError("max_repeat must be >= 0")
    if base < 2:
        raise ValueError("base must be >= 2")

    results = {}
    upper_index = base**3 - 1  # indices for seeds from 0 .. base^3 - 1

    index = 0
    while index <= upper_index:
        a = index // base**2
        b = (index // base) % base
        c = index % base

        for k in range(0, max_repeat + 1):
            repeated_c = c * (base**k - 1) // (base - 1) if k > 0 else 0
            j_num = a * base**(k + 1) + b * base**k + repeated_c

            if j_num not in results:
                results[j_num] = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "k": k,
                    "prime_factors": f.findPrimeFactors(j_num),
                    "is_prime": f.identifyPrime(j_num),
                }

        index += 1

    return results


def getJNumsForSeed(a, b, c, max_repeat, base=10):
    """
    Compute J_k(a,b,c) for k = 0..max_repeat for a single seed (a,b,c) in the given base.
    Returns a dict keyed by j_num with the same structure as getAllJNums.
    """
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
    for k in range(0, max_repeat + 1):
        repeated_c = c * (base**k - 1) // (base - 1) if k > 0 else 0
        j_num = a * base**(k + 1) + b * base**k + repeated_c

        if j_num not in results:
            results[j_num] = {
                "a": a,
                "b": b,
                "c": c,
                "k": k,
                "prime_factors": f.findPrimeFactors(j_num),
                "is_prime": f.identifyPrime(j_num),
            }
    return results


def getJNumsForAB(a, b, max_repeat, base=10):
    """
    Fast path when a and b are fixed and c ranges over 0..base-1.
    Returns same output shape as getAllJNums but only for seeds with given a and b.
    """
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
    for c in range(0, base):
        for k in range(0, max_repeat + 1):
            repeated_c = c * (base**k - 1) // (base - 1) if k > 0 else 0
            j_num = a * base**(k + 1) + b * base**k + repeated_c

            if j_num not in results:
                results[j_num] = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "k": k,
                    "prime_factors": f.findPrimeFactors(j_num),
                    "is_prime": f.identifyPrime(j_num),
                }
    return results
