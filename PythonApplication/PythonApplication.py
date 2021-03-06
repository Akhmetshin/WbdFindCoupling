from ctypes import *
import ctypes
import numpy as np
import os.path

#wbd_name = "D:\\MyProgect\\Python\\329E_1.wbd".encode('cp1251')
#wbd_name = 'C:\\ИНТРОСКОП_v2.5.8\\329E_1.wbd'.encode('cp1251')
#wbd_name = 'D:\\Introskop_v2.5.8\\1547.wbd'.encode('cp1251')
#wbd_name = 'D:/Introskop_v2.5.8/скв_585_к_20_Нижне-Шапшинское.wbd'.encode('cp1251')
#wbd_name = "C:\\ИНТРОСКОП_v2.5.8\\5202.wbd".encode('cp1251')
#wbd_name = "C:\\ИНТРОСКОП_v2.5.8\\11522_1.wbd".encode('cp1251')
#wbd_name = "C:\\ИНТРОСКОП_v2.5.8\\16053.wbd".encode('cp1251')
wbd_name = "C:\\ИНТРОСКОП_v2.5.8\\МИ-51_(15_ОЦ).wbd".encode('cp1251')

print(wbd_name)

dllname = os.path.dirname(__file__) + '\\WbdFindCoupl.dll'
WbdFindCoupDll = cdll.LoadLibrary(dllname)
n = WbdFindCoupDll.WbdMainFindCoupl(wbd_name) # найти муфты в файле. самая нижняя найденная муфта - первая. те нулевая
if n == -2:
    print('File not open')
    exit(-2) # файл не открылся

print(n) # n - число найденных муфт

l = WbdFindCoupDll.WbdFindCouplingGetN()

print(l) # l - число точек записи

c_int_p = ctypes.POINTER(ctypes.c_int)

WbdFindCoupDll.WbdFindCouplingGetP1.argtypes = [c_int_p]
WbdFindCoupDll.WbdFindCouplingGetP5.argtypes = [c_int_p]

p1 = np.arange(n,dtype=np.int) # выделить массив для нижних точек муфты
p5 = np.arange(n,dtype=np.int) # выделить массив для верхних точек муфты

WbdFindCoupDll.WbdFindCouplingGetP1(p1.ctypes.data_as(c_int_p)) # получить точки p1, p5
WbdFindCoupDll.WbdFindCouplingGetP5(p5.ctypes.data_as(c_int_p))

a=0
i=0
while i < n:
    d1=(p5[i] - p1[i]) * 2.5 / 10 # длина муфты в сантиметрах
    d2=(p1[i] - a) * 2.5 / 1000   # длина колонны в метрах
    print("%3d %8d  %8d  %5.2f  %5.2f" %(i, p1[i], p5[i], d1, d2))
    a = p1[i]
    i=i+1

d2=(l - a) * 2.5 / 1000
print("                               %5.2f\n" % d2)

exit(0)
