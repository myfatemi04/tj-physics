import math
import matplotlib.pyplot as plt

def acceleration(t, A=1, hz=1):
    return A * math.cos(t * hz * math.pi * 2)
    
def simulatePosition(targetT, A=1, hz=1, dt=0.001):
    t = 0
    x = 0
    v = 0
    
    plotT = []
    plotX = []
    plotV = []
    plotA = []
    
    while t < targetT:
        a = acceleration(t, A, hz) # m/s^2
        v += a * dt # m/s
        x += v * dt # m
        t += dt
        
        center = 1/((2 * math.pi) ** 2)
        actual = A * math.cos(2 * math.pi * hz * t) / ((2 * math.pi) ** 2)
        
        plotT.append(t)
        plotX.append(x - center + actual)
        plotV.append(v)
        plotA.append(a)
    
    return plotT, plotX, plotV, plotA
    
def getPosition(targetT, A=1, hz=1):
    return -A * math.cos(targetT * hz * math.pi * 2)
    
targetT = float(input("Target T (seconds) [default 1s]: ") or 1)
A = float(input("Amplitude (meters) [default 1m]: ") or 1)
hz = float(input("Cycles/second (Hz) [default 1Hz]: ") or 1)
dt = float(input("dt (seconds) [default 0.001]: ") or 0.001)

plotT, plotX, plotV, plotA = simulatePosition(targetT, A, hz, dt)
print("Simulated value:", plotX[-1])
print("Calculated value:", getPosition(targetT, A, hz))

plt.plot(plotT, plotX, color='r')
plt.plot(plotT, plotV, color='g')
plt.plot(plotT, plotA, color='b')
plt.show()

"""

Analytical Solution

a = Acos(2pi * t)
v = Asin(2pi * t) / 2pi
x = -Acos(2pi * t) / 4pi^2

"""