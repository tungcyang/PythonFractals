'''
A trial implementation of Barnsley Fern (https://en.wikipedia.org/wiki/Barnsley_fern) in Python.
'''

import sys
import random
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import csv

DEFAULT_NUM_POINTS = 65536
DEFAULT_NUM_COLORSHADES = 64
EPSILON = 1.0e-7                # allowed relative difference between two floating numbers to be considered equal.

# sum_probability is used as global here.
sum_probability = []
# The following a, b, c, d, e, f and p coefficients refer to the original Barnsley fern
a = ( 0.0,  0.85,  0.20, -0.15)
b = ( 0.0,  0.04, -0.26,  0.28)
c = ( 0.0, -0.04,  0.23,  0.26)
d = (0.16,  0.85,  0.22,  0.24)
e = ( 0.0,   0.0,   0.0,   0.0)
f = ( 0.0,  1.60,  1.60,  0.44)
p = (0.01,  0.85,  0.07,  0.07)

# f1 as described in the Wikipage -- it maps any point to another point at the base of the
#     stem.  It is chosen 1% of the time.
def transformation_1(p):
    x = p[0]
    y = p[1]
    x1 = a[0]*x + b[0]*y + e[0]
    y1 = c[0]*x + d[0]*y + f[0]
    return x1, y1

# f2 as described in the Wikipage -- it maps any point inside the red triangle leaflet to
#     a point inside the opposite smaller blue triangle leaflet.  It is chosen 85% of the time.
def transformation_2(p):
    x = p[0]
    y = p[1]
    x1 = a[1]*x + b[1]*y + e[1]
    y1 = c[1]*x + d[1]*y + f[1]
    return x1, y1

# f3 as described in the Wikipage -- it maps any point inside the blue triangle leaflet to
#     a point inside the alternating corresponding triangle across the stem (with flipping).
#     It is chosen 7% of the time.
def transformation_3(p):
    x = p[0]
    y = p[1]
    x1 = a[2]*x + b[2]*y + e[2]
    y1 = c[2]*x + d[2]*y + f[2]
    return x1, y1

# f4 as described in the Wikipage -- it maps any point inside the blue triangle leaflet to
#     a point inside the alternating corresponding triangle across the stem (without flipping).
#     It is chosen 7% of the time.
def transformation_4(p):
    x = p[0]
    y = p[1]
    x1 = a[3]*x + b[3]*y + e[3]
    y1 = c[3]*x + d[3]*y + f[3]
    return x1, y1

def initialize_get_index():
    global sum_probability
    # probability = [0.85, 0.07, 0.07, 0.01]
    cumulated_prob = 0
    sum_probability = []
    for probability in p:
        cumulated_prob += probability
        sum_probability.append(cumulated_prob)
    if math.fabs(cumulated_prob - 1) > EPSILON:
        s = "The given probabilities p do not add up to 1!"
        sys.stderr.write(s)
        quit()


def get_index():
    x = random.random()
    for item, sp in enumerate(sum_probability):
        if x <= sp:
            return item
    return len(sum_probability) - 1

def transform(p):
    transformations = [transformation_1, transformation_2, transformation_3,
                       transformation_4]
    # Choosing the transformation function as selected by their probabilities.
    # Here we have a list of functions.
    tindex = get_index()
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

def parse_fern():
    global a, b, c, d, e, f, p
    try:
        with open(sys.argv[2], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rownum = 0
            for row in reader:
                a[rownum] = float(row[0])
                b[rownum] = float(row[1])
                c[rownum] = float(row[2])
                d[rownum] = float(row[3])
                e[rownum] = float(row[4])
                f[rownum] = float(row[5])
                p[rownum] = float(row[6])
                rownum += 1
    except:
        s = "Error occurred during parsing CSV file " + sys.argv[2] + " Default fern used."
        sys.stderr.write(s)
        quit()

def main():
    # Printing module information. It is fine if some modules do not provide __version__.
    try:
        print('===== sys module version ' + sys.__version__ + ' =====')
        print('===== random module version ' + random.__version__ + ' =====')
        print('===== math module version ' + math.__version__ + ' =====')
        print('===== matplotlib module version ' + matplotlib.__version__ + ' =====')
        print('===== csv module version ' + csv.__version__ + ' =====')
    except:
        pass
    
    # Two ways to call fern.py:
    # fern.py [NumPoints]
    if len(sys.argv) == 1:
        # The user does not provide any command arguments; using defaults.
        n = DEFAULT_NUM_POINTS
    else:
        try:
            n = int(sys.argv[1])
        except ValueError:
            # Check for Python exceptions in https://docs.python.org/2/library/exceptions.html
            s = "You should provide an integer number as the number of points: " + sys.argv[1]
            sys.stderr.write(s)
            quit()
        except:
            s = "An unexpected error occurred."
            sys.stderr.write(s)
            quit()
        finally:
            if len(sys.argv) == 3:
                parse_fern()
            elif len(sys.argv) > 3:
                s = "Too many command arguments given."
                sys.stderr.write(s)
                quit()

    if n > 0:
        initialize_get_index()
        x, y = draw_fern(n)
        # Now there should be (n + 1) data points for x and y.  We like to draw them
        # in different shades of green.  We referenced the page
        #     "Using Colormaps to set color of line in matplotlib" in
        # http://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
        values = range(DEFAULT_NUM_COLORSHADES)
        cm = plt.get_cmap('Greens')
        cNorm = colors.Normalize(vmin = 0, vmax = values[-1])
        scalarMap = cmx.ScalarMappable(norm = cNorm, cmap = cm)
        for index in values:
            colorVal = scalarMap.to_rgba(values[index])
            # We only want to plot a part of x and y
            idxrange = range(int(n*index/DEFAULT_NUM_COLORSHADES),
                             int(n*(index + 1)/DEFAULT_NUM_COLORSHADES))
            subx = [x[idx] for idx in idxrange]
            suby = [y[idx] for idx in idxrange]
            plt.plot(subx, suby, '.', color = colorVal)
        plt.title('Barnsley fern with {0} points'.format(n))
        plt.show()
    return 0

if __name__ == '__main__':
    sys.exit(main())



