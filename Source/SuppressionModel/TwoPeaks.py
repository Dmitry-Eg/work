from cmath import exp, pi, sqrt
from glob import glob
from random import gauss
import scipy as sp
import copy
import numpy as np
import matplotlib.pyplot as pypl
from os import listdir
from os.path import isfile, join
from matplotlib.widgets import Slider, TextBox
import random
import InitData
random.seed(version=2)

def get_nearest_value(iterable, value):
    return min(enumerate(iterable), key=lambda x: abs(x[1] - value))[0]


N = 20000
countOfPoints = 30
dcArray = np.linspace(3, 10, countOfPoints)
rArray = dcArray/2 
fig, ax = pypl.subplots()
ax.set_xlim(-9,-2)
lowestTempDc, lowestTempV = InitData.initData(ax)

xGauss = copy.copy(lowestTempDc)
AMPL = 1e-6
SIG = 1
NUL = -3.8
yGauss = (AMPL/SIG) * np.exp(-((xGauss-NUL)/SIG)**2)
#lowestTempV = lowestTempV - yGauss
ax.plot(lowestTempDc, lowestTempV)

ax.set_ylim(-5e-6,9e-6)
Temperatures = [1.66, 8, 10, 15, 20, 30, 35, 40, 50, 60, 80, 100]
Lee1 = 2400
ax.grid(True)
for t in range(0, len(Temperatures)):
    suppressedDc = lowestTempDc
    suppressedV = lowestTempV * np.exp(-np.pi*np.abs(suppressedDc) * Temperatures[t]**2 / (2*Lee1))
    #ax.plot(suppressedDc, suppressedV)

ax.plot(xGauss, yGauss)
pypl.show()