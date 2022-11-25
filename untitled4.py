# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:40:35 2022

@author: CIL
"""
import math
A1 = 9.371e-4
B1 = 2.208e-4
C1 = 1.276e-4
A2 = 0.000935401
B2 = 0.00022106
C2 = 0.000000127472
x = 1.95209
def happy(A,B,C, x):
    return 1/(A + B*math.log(x) +C*(math.log(x)**3)) - 273.15


ans1 = happy(A1,B1,C1, x)
ans2 = happy(A2,B2,C2, x)
