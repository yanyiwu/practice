from matplotlib import pylab as pl
import numpy as np
import sys

x_list = []
y_list = []
for line in sys.stdin:
    x, y = line.split()
    x = float(x)
    y = float(y)
    x_list.append(x)
    y_list.append(y)

pl.plot(x_list, y_list, 'og')
pl.plot([0, 1], [0, 1], 'r')
pl.show()
