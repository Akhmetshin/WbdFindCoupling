from ctypes import *
import ctypes
import numpy as np
import os.path

str_name = b"D:\\MyProgect\\Python\\329E_1.wbd"
#str_name = b"D:\\Introskop_v2.5.8\\1547.wbd"
#str_name = b"D:\\Introskop_v2.5.8\\скв_585_к_20_Нижне-Шапшинское.wbd"
#str_name = b"C:\\ИНТРОСКОП_v2.5.8\\329E_1.wbd"

print(str_name)

dllname = os.path.dirname(__file__) + '\WbdFindCoupl.dll'
FindCouplings_dll = cdll.LoadLibrary(dllname)
n = FindCouplings_dll.WbdMainFindCoupl(str_name)
if n == -2:
  exit(-2)

print(n)

l = FindCouplings_dll.WbdFindCouplingGetN()

print(l)

c_int_p = ctypes.POINTER(ctypes.c_int)

FindCouplings_dll.WbdFindCouplingGetP1.argtypes = [c_int_p]
FindCouplings_dll.WbdFindCouplingGetP5.argtypes = [c_int_p]

p1 = np.arange(n,dtype=np.int)
p5 = np.arange(n,dtype=np.int)

FindCouplings_dll.WbdFindCouplingGetP1(p1.ctypes.data_as(c_int_p))
FindCouplings_dll.WbdFindCouplingGetP5(p5.ctypes.data_as(c_int_p))

a=0
i=0
while i < n:
    d1=(p5[i] - p1[i]) * 2.5 / 10
    d2=(p1[i] - a) * 2.5 / 1000
    print("%3d %8d  %8d  %5.2f  %5.2f" %(i, p1[i], p5[i], d1, d2))
    a = p1[i]
    i=i+1

d2=(l - a) * 2.5 / 1000
print("                               %5.2f\n" % d2)

exit(0)
