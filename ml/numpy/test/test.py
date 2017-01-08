import numpy as np
import pylab as pl

x = np.linspace(0,4*np.pi,100)

print x
#pl.plot(x,np.sin(x))
#pl.show()


a = [[1, 0], [0, 1]]
b = [[4, 1], [2, 2]]

print np.dot(a, b)
print np.dot(b, b)

c = np.linspace(-2, 2, 3)
print c
print c * c
