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
import InitData
random.seed(version=2)


N = 20000
countOfPoints = 30
dcArray = np.linspace(3, 10, countOfPoints)
rArray = dcArray/2 
k = 1500
fig, ax = pypl.subplots()
InitData.initData(ax)
#ax.set_ylim(0,2.5)
T = [1.66, 8, 10, 15, 20, 30, 35,40,50,60, 80, 100]
maxArr = np.zeros(len(T))
tempIndex = 0
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
        #print((3*np.pi/2)*counter/(N))
        index+=1
    #print('\n')
    print(k/(t*t))
    #print('\n')
    ax.plot(dcArray, amplArray/400000 + 511.93746539E-9	)
    maxArr[tempIndex] = max(amplArray)
    tempIndex+=1

print(maxArr)
print(amplArray)
pypl.show()