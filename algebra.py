from functools import reduce
from itertools import combinations
from copy import deepcopy
import operator as op


def combine(eq, end):
    '''Combine like terms given an eq of two forms:
    
    Form 1 (end):
        [ c0, a, c1, [c2, b, c3, a]] -> [ c0 + c1 * c3, a, c1 * c2, b]
        
    Form 2
        [ c0, [c1, a, c2, b], c3, b] -> [ c0 * c1, a, c0 * c2 + c3, b]'''
    if end:
        return [eq[0] + eq[2] * eq[3][2], eq[1], eq[2] * eq[3][0], eq[3][1]]
    else:
        return [eq[0] * eq[1][0], eq[1][1], eq[0] * eq[1][2] + eq[2], eq[3]]

def backprop(a, b):
    '''Given two integers a and b (a >= b), 
    return their gcd and Z-linear combination. That is, (g, linear)
    where g = gcd(a,b) and linear = [x, a, y, b] satisfying
    g = ax + by. We compute x and y using backpropagation on the 
    Euclidean algorithm. Note that x and y are not necessarily unique. '''
    assert a >= b, "b cannot be greater than a"

    g, eq = euclid(a, b, backprop = True)
    linear = eq[g][:]

    # End means replace end spot in combo
    end = 1
    while linear[1] != a or linear[-1] != b:
        index = -1 if end else 1
        linear[index] = eq[linear[index]][:]
        linear = combine(linear, end)
        end = (end + 1) % 2

    return (g, linear) 

def euclid(a, b, backprop = False):
    '''Return the GCD of a and b using the Euclidean algorithm. Includes
    intermediate steps for backpropagation. '''
    r, d = [a,b] , []
    while b:
        d.append(a // b)
        r.append(a % b)
        a, b  = b, a % b

    if backprop:
        eq = { r[i + 2]: [1, r[i], -d[i], r[i + 1]] for i in range(len(d))}
        return (a, eq)
    else:
        return a

def prod(*nums):
    "Return the product of some numbers. "
    return reduce(op.mul, nums)

def fact(n):
    "Return the factorial of n. "
    return prod(*[i for i in range(1, n + 1)])

def gcd(*nums):
    "Return the GCD for an arbitrary number of integers. "
    return reduce(euclid, nums)

def lcm(*nums):
    "Return the LCM for an arbitrary number of integers. "
    pairs = combinations(nums, 2)
    return prod(*nums) // prod(*[ gcd(*pair) for pair in pairs]) 

def phi(n):
    '''Euler's phi/totient function: Return the number of positive 
    integers less than or equal to n that are relatively prime to n. '''
    return sum([euclid(n, i) == 1 for i in range(1, n)])
  
def phi2(n):
    "Euler's phi function computed using product formula. "
    return int(n * prod(*[ 1 - 1/p for p in primes(n) if n % p == 0]))

def pfactor(n):
    '''Return the prime factorization of integer n as a dictionary.
    Example: 20 returns { 2: 2, 5: 1} which means 2^2 * 5^1 = 20 '''
    assert n > 1
   
    factors = {}
    ps = primes(n + 1)
    k = n

    # n is prime
    if n in ps:
        return {n : 1}

    while k != 1:
        if n != k:
            ps = list(filter(lambda p: p <= k, ps))
        for p in ps:
            if k % p == 0:
                k = k // p
                if p in factors:
                    factors[p] += 1
                else:
                    factors[p] = 1
    return factors

def isprime(n):
    "Return true if n is prime. "
    return n in primes(n + 1)

def primes(n):
    "Return a list of all prime numbers less than integer n. "
    sieve = [True] * (n // 2)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[ i * i // 2 :: i] = [False] * ((n- i*i - 1) // (2*i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]

def modpairs(n, k = 1):
    '''Return the residue classes with a partner such that their product is
    k in Z mod n. By default, k = 1 for units. Another common use is k = 0,
    for zero divisors. '''
    assert n > 1
    u = []

    for i in range(0, n):
        if i in u:
            pass
        else:
            for j in range(0, n):
                if (i * j) % n == k:
                    u.append(i)
                    if i != j:
                        u.append(j)
    return list(set(u))

# TODO: Add a size attribute to permutation
def decompose(perm):
    '''Return the cycle decomposition for a given permutation (represented as 
    a dictionary). '''
    p = deepcopy(perm)
    
    cycle = []
    while p:
        s = min(p.keys()) 
        if p[s] == s:
            del p[s]
        else:
            c, k = [], s
            while p[k] != s:
                c.append(k)
                k = p.pop(k)
            
            c.append(k)
            del p[k]
            cycle.append(c)

    return cycle

def perm2dict(perm):
    '''Return the dictionary representation of a permutation (written as a
    cycle decomposition. '''

    d = {}

    for cycle in perm:
        length = len(cycle)
        for i in range(length):
            d[cycle[i]] = cycle[(i + 1) % length]

    m = max([elem for cycle in perm for elem in cycle])
    singles = set([ i for i in range(1, m + 1)]) - set(d)
    for s in singles:
        d[s] = s

    return d

def compose(perm1, perm2):
    '''Return the composition of two permutations (passed in as cycles). 
    If your permutations are dictionaries, call decompose() first. '''
    
    p1, p2 = perm2dict(perm1), perm2dict(perm2)

    p = {}
    for elem in p2.keys():
        if p2[elem] not in p1:
            p[elem] = p2[elem]
        else:
            p[elem] = p1[p2[elem]]
    return decompose(p)

    




