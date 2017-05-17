import sys

from matplotlib import pylab as pl
import numpy as np
import datetime

x = []
y = []

for line in sys.stdin:
    t = line.split(',')
    date = t[0]
    appid = int(t[1])
    tz = int(t[2])
    h = int(t[3])
    send_suc = int(t[4])
    ctr = float(t[5])
    date = datetime.datetime.strptime(date, '%Y%m%d')
    local_date = date + datetime.timedelta(hours=(h+tz/3600))
    local_date_h = int(local_date.strftime('%d%H'))
    if send_suc > 100000:
        x.append(local_date_h)
        y.append(ctr)

#x = range(len(y))
print x, y
pl.plot(x, y, 'o-')
pl.show()

