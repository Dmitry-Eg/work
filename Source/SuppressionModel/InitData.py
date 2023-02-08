from cmath import exp, pi, sqrt
from glob import glob
from random import gauss
import scipy as sp
import numpy as np
import matplotlib.pyplot as pypl
from os import listdir
from os.path import isfile, join, abspath
from matplotlib.widgets import Slider, TextBox
import random

random.seed(version=2)

hPlanck = 6.62607015e-34 / (2*np.pi) # концентрация
n = 7e15 # концентрация 
e = 1.6e-19 # заряд электрона


def initData(ax):
    #ax.set_ylim(0,2.5)
    pathOfData = 'D:\\Lab\\work\\Source\\SuppressionModel\TempData\\' # Путь до файлов с экспериментальными данными
    print(listdir(pathOfData))
    onlyfiles = [f for f in listdir(pathOfData) if isfile(join(pathOfData, f))] # Получение имен файлов
    # Отрисовка экспериментальных данных
    lowestTemp = (0, 0) 
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
        #V = V - (V[0]-V[-1])/(B[0]-B[-1]) *B    # Снова вычитание линейного тренда (уже в выделенной части)
        ax.plot((1e6)*2*np.sqrt(2*np.pi*n)*hPlanck/(e*B), V, '.')
        if name == 'I15-3_U16-4_Non-local_T1,66':
            lowestTemp = ((1e6)*2*np.sqrt(2*np.pi*n)*hPlanck/(e*B), V)
    return lowestTemp
        #ax.plot(B, V, '.')  