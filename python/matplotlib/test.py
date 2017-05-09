from matplotlib import pylab as pl
import numpy as np

x = [0.1, 0.2, 0.3, 0.5, 0.1]
y = [0.1, 0.2, 0.3, 0.9, 0.2]

pl.plot(x, y, 'og')
pl.plot([0, 1], [0, 1], 'r')
pl.show()
