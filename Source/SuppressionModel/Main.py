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
ax.set_xlim(0,10)
lowestTempDc, lowestTempV = InitData.initData(ax)
ax.set_ylim(-1e-5,2e-5)
Temperatures = [1.66, 4.2, 7, 10, 15, 20, 25, 30, 35, 40, 50, 60, 80]
Lee1 = 2000
ax.grid(True)
print(np.sqrt(2*Lee1/(np.pi*6)))
for t in range(0, len(Temperatures)):
    suppressedDc = lowestTempDc
    suppressedV = lowestTempV * np.exp(-np.pi*np.abs(suppressedDc) * Temperatures[t]**2 / (2*Lee1))
    print(Lee1/Temperatures[t]**2)
    #ax.plot(suppressedDc, suppressedV, 'b', linestyle='dashed')

pypl.show()