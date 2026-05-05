import sympy as sp

def findPrimeFactors(num):
    if num < 2:
        return []
    factors = []
    for prime, exp in sp.factorint(num).items(): # This returns a dictionary of prime factors and their exponents
        factors.extend([prime] * exp) # This adds the prime factor to the list as many times as its exponent
    return factors

def identifyPrime(num):
    factors = findPrimeFactors(num)
    if sp.isprime(num):
        return 1
    else:
        return 0

