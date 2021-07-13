import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b,c):
    # return a*np.sqrt(x)*(b*np.square(x)+c)
    return a*np.square(x) + b*x + c

x = [2,3,4,5,6,7,8,9,10]
x = np.array(x)
num = [0.019,0.036,0.062,0.123, 0.210, 0.292, 0.386, 0.482, 0.681]
y = np.array(num)

popt, pcov = curve_fit(func, x, y)

print(popt)
a = popt[0]
b = popt[1]
c = popt[2]
yvals = func(x,a,b,c)
print('popt:', popt)
print('a:', a)
print('b:', b)
print('c:', c)
print('pcov:', pcov)
print('yvals:', yvals)
def data(num):
    return 0.009076839737007063*num*num - 0.02887207684345916*num + 0.040509521211436667
print(data(2), data(10), data(20), data(30), data(40), data(50))
print(a,b,c)