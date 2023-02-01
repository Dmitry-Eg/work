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
k = 2000
fig, ax = pypl.subplots()
ax.set_xlim(2.5,10)
lastDc, lastV = InitData.initData(ax)
#ax.set_ylim(0,2.5)
Temperatures = [1.66, 8, 10, 15, 20, 30, 35, 40, 50, 60, 80, 100]
maxArr = np.zeros(len(Temperatures))
tempIndex = 0
newLastV = copy.copy(dcArray)

for i in range(len(dcArray)):
    newLastV[i] = lastV[get_nearest_value(lastDc, dcArray[i])] # вытаскиваем нужные точки из подавленного графика

print(newLastV)
for t in Temperatures:
    index = 0
    amplArray = np.zeros(countOfPoints)
    for r in rArray:
        counter = 0
        for i in range(0, N):
            alpha = random.random()*np.pi/2
            x = random.random()*3
            if (r*(1-np.cos(alpha))<=3) and ((2*r*np.sin(alpha)+x)>=6) and ((2*r*np.sin(alpha)+x)<=9):
                counter+=np.exp(-(2*alpha*r*t*t)/(k))
        amplArray[index] = (3*np.pi/2)*counter/(N)
        #print((3*np.pi/2)*counter/(N))
        index+=1
    print(k/(t*t))
    print(amplArray)
    ax.plot(dcArray, amplArray/420000 + newLastV) # ищем нужную амплитуду и вы
    maxArr[tempIndex] = max(amplArray)
    tempIndex+=1

print(maxArr)
print(amplArray)
pypl.show()