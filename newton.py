
def horner(x, *polynomial):
    "Use Horner's method to evaluate a polynomial at x. "
    answer = 0
    for coefficient in polynomial:
        answer = answer * x + coefficient
    return answer


def derivative(polynomial):
    "Return the derivative of a polynomial. "
    degree = len(polynomial) - 1
    return [polynomial[n] * (degree - n) for n in range(degree)]


def scale(polynomial, factor):
    "Scale all coefficients in the polynomial by a factor. "
    return [factor * p for p in polynomial ]


def newton(f, theta = 0, iterations = 20):
    '''Run Newton's method on function f for a given number of iterations
    starting at value theta. '''
    df = derivative(f)

    for i in range(iterations):
        theta -= horner(theta, *f) / horner(theta, *df)
    return theta
 

if __name__ == '__main__':
    # (x^7 - 14x^5 + 49x^3 - 36x) / 25
    f = scale([1, 0, -14, 0, 49, 0, -36, 0], 1/25)

    # Witness chaos in action! Hail eris
    print(newton(f, theta = 1.548740046328))
    print(newton(f, theta = 1.548740046327))


