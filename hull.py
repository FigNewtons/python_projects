import random as rand
import matplotlib.pyplot as plot
import pylab


def rep(item, n = 1):
    "Return a list containing item duplicated n times. "
    return [ item for i in range(n) ]


def validrange(r):
    """Return true if range r is valid. That is r = [a, b] where a and b
    are numbers and a < b. """
    assert len(r) == 2
    return r[0] < r[1]


def generate(n = 10, dim = 2, *kcell):
    """Return a list of n tuples with dimension dim. Each tuple
    represents a geometric point whose coordinates are within
    a specified k-cell. """
    interval = [0,5]
    KCELL = rep(interval, dim)

    if not any(kcell):
        kcell = KCELL
    else:
        for i in range(len(kcell)):
            if not validrange(kcell[i]):
                kcell[i] = interval
        if len(kcell) > dim:
            kcell = list(kcell[:dim])
        elif len(kcell) < dim:
            kcell = list(kcell) + rep(interval, dim - len(kcell))
        
    r = [[kcell[i][0], kcell[i][1] - kcell[i][0]] for i in range(len(kcell))]

    return [tuple([r[j][1] * rand.random() + r[j][0] for j in range(dim)]) for i in range(n)]


def show(points, convex = True):
    """Display 2D scatterplot of generated points. Red points indicate min 
    and max point under dictionary order. If convex, then the plot also
    displays the resulting polygon containing all given points. """
    
    points = sorted(points)
    color = ['red'] + ['blue'] * (len(points) - 2) + ['red']
    
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plot.scatter(x,y, c = color)

    if convex:
        hull = convex_hull(points)
        for i in range(1, len(hull)):
            x = [hull[i - 1][0], hull[i][0]]
            y = [hull[i - 1][1], hull[i][1]]
            plot.plot(x, y)

        x = [hull[-1][0], hull[0][0]]
        y = [hull[-1][1], hull[0][1]]
        plot.plot(x, y)

    plot.show()


def counterclockwise(p1, p2, p3):
    """Return True if three points form a counterclockwise angle. This is 
    found by taking the cross product of the points (setting z = 1) for 
    each 2D point (This works because of the 'right-hand rule'). """
    cross = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    return cross <= 0

def half(p):
    "Return half of the convex hull given a sorted list of points. "
    order = [p[0], p[1]]
    for i in range(2, len(p)):
        order.append(p[i])
        while len(order) > 2 and not counterclockwise(order[-1], order[-2], order[-3]):
            del order[-2]
    return order

def convex_hull(points): 
    """Return a list of points in counterclockwise order that form the
    convex hull of the given list of 2D points. The algorithm used is
    called Graham's scan. """
    assert len(points) > 2

    p = sorted(points)
    
    upper = half(p)
    lower = half(p[::-1])[1: -1]

    return upper + lower





