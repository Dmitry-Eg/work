from cmath import exp, pi, sqrt
from glob import glob
from random import gauss
import scipy as sp
import numpy as np
import matplotlib.pyplot as pypl
from os import listdir
from os.path import isfile, join
from matplotlib.widgets import Slider, TextBox
import random

random.seed(version=2)


N = 25000
countOfPoints = 30
dcArray = np.linspace(3, 10, countOfPoints)
rArray = dcArray/2 
k = 5000
T = [0, 1.66, 8, 10, 15, 20, 25, 30, 35,40,50,60]
fig, ax = pypl.subplots()
ax.set_ylim(0,2.5)
for t in T:
    index = 0
    amplArray = np.zeros(countOfPoints)
    for r in rArray:
        counter = 0
        for i in range(0, N):
            alpha = random.random()*np.pi/2
            x = random.random()*3
            if (r*(1-np.cos(alpha))<=3) and ((2*r*np.sin(alpha)+x)>=6) and ((2*r*np.sin(alpha)+x)<=9) :
                counter+=np.exp(-(2*alpha*r*t*t)/(k))
        amplArray[index] = (3*np.pi/2)*counter/(N)
        print((3*np.pi/2)*counter/(N))
        index+=1
    ax.plot(dcArray, amplArray)

print(amplArray)
pypl.show()