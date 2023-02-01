from cmath import exp, pi, sqrt
from glob import glob
from random import gauss
import scipy as sp
import numpy as np
import matplotlib.pyplot as pypl
from os import listdir
from os.path import isfile, join
from matplotlib.widgets import Slider, TextBox

# Константы
dc = 3
numberToChange = 0 # Номер кривой, у которой меняем lee
amplitude = 1 # Амплитуда
sigmaAmpl = 0.2 # Сигма

# Гауссиан
def gaussian(x, sigma):
    return amplitude*exp(-(x*x)/(2*sigma*sigma))/(sqrt(2*pi)*sigma)

# Треугольник
def triangle1(x):
    if x<=dc or x>=3*dc:
        return 0
    if x>dc and x<=2*dc:
        return (x-dc)/dc
    if x>2*dc and x<3*dc:
        return (-x+3*dc)/dc


# Массивы lee и температур
l_eeArr = [300, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
tempsArr = [1.66, 8,10,15,20,25,30,35,40,50,60]

# Отрисовка
def drawAll():
    ax.clear()
    pathOfData = 'H:\\NON_LOCAL\\Model\\data\\' # Путь до файлов с экспериментальными данными
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
        ax.plot((-6*51)/(B*1000), V, '.') 

    # Отрисовка теоретических моделей
    t = np.linspace(0, 10, 200) # Получение массивов переменных (промежуток от 0 до 10 делим на 200 участков)
    u = np.linspace(0, 10, 200) 
    gaussianF = np.vectorize(gaussian, otypes=[np.complex]) # Векторизация функций (для того, чтобы можно было вызывать их от numpy-массивов)
    triangle1F = np.vectorize(triangle1, otypes=[np.complex])
    for i in range(0,11): 
        sigma = sigmaAmpl*sqrt(tempsArr[i]) # Температурная зависимость сигмы
        sver = [sp.integrate.trapz(gaussianF(x-u, sigma)*triangle1F(u)*np.exp(-(pi*u)/(2*l_eeArr[i])), t) for x in t] # Свертка
        sver = np.asarray(sver) # приведение массива к numpy-массиву
        ax.plot(t, sver)
    pypl.draw()

# Далее - интерфейс

fig, ax = pypl.subplots()
axfreq = fig.add_axes([0.1, 0.02, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='AMPL',
    valmin=0,
    valmax=2e-4,
    valinit=1,
)

def update(val):
    global amplitude
    amplitude = val
    drawAll()

def submitNumber(text):
    global numberToChange
    numberToChange = int(text)
    print(numberToChange)
    print('sub')
    
def submitL_ee(text):
    global l_eeArr
    l_ee = float(text)
    if numberToChange!=0:
        l_eeArr[numberToChange - 1] = l_ee
        drawAll()  
        print(l_eeArr)

def submitSigma(text):
    global sigmaAmpl
    sigmaAmpl = float(text)
    drawAll()

axbox1 = pypl.axes([0.9, 0.3, 0.1, 0.075])
numberOfSublineBox = TextBox(axbox1, 'Number', initial='')
numberOfSublineBox.on_submit(submitNumber)

axbox2 = pypl.axes([0.9, 0.2, 0.1, 0.075])
l_eeBox = TextBox(axbox2, 'l_ee', initial='')
l_eeBox.on_submit(submitL_ee)

axbox3 = pypl.axes([0.9, 0.4, 0.1, 0.075])
sigmaBox = TextBox(axbox3, 'sigma', initial='')
sigmaBox.on_submit(submitSigma)


freq_slider.on_changed(update)
pypl.show()
