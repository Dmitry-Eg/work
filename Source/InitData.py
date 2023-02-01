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

def initDat(ax):
    T = [1.66, 8, 10, 15, 20, 25, 30, 35,40,50,60]
    #ax.set_ylim(0,2.5)
    pathOfData = 'F:\\Work\\NON_LOCAL\\MonteCarlo\\14-12\\' # Путь до файлов с экспериментальными данными
    print(listdir(pathOfData))
    onlyfiles = [f for f in listdir(pathOfData) if isfile(join(pathOfData, f))] # Получение имен файлов
    # Отрисовка экспериментальных данных 
    for name in onlyfiles:
        f = open(pathOfData+name, 'r')
        data = np.loadtxt(f, delimiter = '\t', usecols=(0,1))
        B = data[:, 0]
        V = data[:, 1]
        start = 0 # выделение нужной части данных
        end = -1
        #V = [(v + (b-B[-1])*(V[0]-V[-1])/(B[-1]-B[0])) for b, v in zip(B,V)] # Вычитание линейного тренда
        B = B[start:end]
        V = V[start:end]
        #V = V - V[0]
        #V = V - (V[0]-V[-1])/(B[0]-B[-1]) *B    # Снова вычитание линейного тренда (уже в выделенной части)
        ax.set_xlim(2.5,10)
        ax.plot((-6*49)/(B*1000), V, '.')
        #ax.plot(B, V, '.')  
