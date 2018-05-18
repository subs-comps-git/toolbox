"""Find primes up to n"""


def primes(n):
    mroot = int(n**0.5)
    sieve = list(range(n + 1))

    for i in range(2, mroot+1):
        if sieve[i]:
            m = n//i - i
            sieve[i*i: n+1:i] = [0] * (m + 1)

    return [i for i in sieve[2:] if sieve[i]]
