'''
A trial implementation of Barnsley Fern (https://en.wikipedia.org/wiki/Barnsley_fern) in Python.
'''

import sys
import random
import matplotlib.pyplot as draw

# f2 as described in the Wikipage -- it maps any point inside the red triangle leaflet to
#     a point inside the opposite smaller blue triangle leaflet.  It is chosen 85% of the time.
def transformation_0(p):
    x = p[0]
    y = p[1]
    x1 = 0.85*x + 0.04*y
    y1 = -0.04*x + 0.85*y + 1.6
    return x1, y1

# f3 as described in the Wikipage -- it maps any point inside the blue triangle leaflet to
#     a point inside the alternating corresponding triangle across the stem (with flipping).
#     It is chosen 7% of the time.
def transformation_1(p):
    x = p[0]
    y = p[1]
    x1 = 0.2*x - 0.26*y
    y1 = 0.23*x + 0.22*y + 1.6
    return x1, y1

# f4 as described in the Wikipage -- it maps any point inside the blue triangle leaflet to
#     a point inside the alternating corresponding triangle across the stem (without flipping).
#     It is chosen 7% of the time.
def transformation_2(p):
    x = p[0]
    y = p[1]
    x1 = -0.15*x + 0.28*y
    y1 = 0.26*x + 0.24*y + 0.44
    return x1, y1

# f1 as described in the Wikipage -- it maps any point to another point at the base of the
#     stem.  It is chosen 1% of the time.
def transformation_3(p):
    x = p[0]
    y = p[1]
    x1 = 0
    y1 = 0.16*y
    return x1, y1

def get_index(probability):
    x = random.random()
    cumulated_prob = 0
    sum_probability = []

    # We seem to evaluate cumulated_prob and sum_probability every time we call get_index.
    # Can it be avoided?
    for p in probability:
        cumulated_prob += p
        sum_probability.append(cumulated_prob)
    for item, sp in enumerate(sum_probability):
        if x <= sp:
            return item
    return len(probability) - 1

def transform(p):
    transformations = [transformation_0, transformation_1, transformation_2,
                       transformation_3]
    prob_transformations = [0.85, 0.07, 0.07, 0.01]

    # Choosing the transformation function as selected by their probabilities.
    tindex = get_index(prob_transformations)
    t = transformations[tindex]
    x, y = t(p)
    return x, y

def draw_fern(n):
    # The Barnsley Fern starts with (0, 0)
    x = [0]
    y = [0]
    x1, y1 = 0, 0

    # The following loop iterates n times and build up the lists of x and y, to be drawn later
    for i in range(n):
        x1, y1 = transform((x1, y1))
        x.append(x1)
        y.append(y1)
    return x, y

if __name__ == '__main__':
    # We wil take the number of points (n) as a command-line argument.  At this time the
    # error handling of n is not implemented.
    n = int(sys.argv[1])
    x, y = draw_fern(n)
    draw.plot(x, y, '.', color='green')
    draw.title('Barnsley fern with {0} points'.format(n))
    draw.show()
