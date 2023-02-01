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


N = 20000
countOfPoints = 30
dcArray = np.linspace(3, 10, countOfPoints)
rArray = dcArray/2 
k = 2700
T = [1.66, 8, 10, 15, 20, 25, 30, 35,40,50,60]
fig, ax = pypl.subplots()
#ax.set_ylim(0,2.5)
pathOfData = 'D:\\NON_LOCAL\\Model\\data\\' # Путь до файлов с экспериментальными данными
print(listdir(pathOfData))
onlyfiles = [f for f in listdir(pathOfData) if isfile(join(pathOfData, f))] # Получение имен файлов
# Отрисовка экспериментальных данных 
for name in onlyfiles:
    f = open(pathOfData+name, 'r')
    data = np.loadtxt(f, delimiter = '\t', usecols=(0,1))
    B = data[:, 0]
    V = data[:, 1]
    start = 315 # выделение нужной части данных
    V = [(v + (b-B[-1])*(V[0]-V[-1])/(B[-1]-B[0])) for b, v in zip(B,V)] # Вычитание линейного тренда
    B = B[start:]
    V = V[start:]
    V = V - V[0]
    V = V - (V[0]-V[-1])/(B[0]-B[-1]) *B    # Снова вычитание линейного тренда (уже в выделенной части)
    ax.set_xlim(0,10)
    ax.plot((-6*54)/(B*1000), V, '.') 
maxArr = np.zeros(11)
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
                counter+=np.exp(-(2*alpha*r*t*t)/(k)) * np.sin(alpha)
        amplArray[index] = (3*np.pi/2)*counter/(N)
        #print((3*np.pi/2)*counter/(N))
        index+=1
    #print('\n')
    print(k/(t*t))
    #print('\n')
    ax.plot(dcArray, amplArray/160000)
    maxArr[tempIndex] = max(amplArray)
    tempIndex+=1

print(maxArr)
print(amplArray)
pypl.show()