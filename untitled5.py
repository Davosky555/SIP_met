# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 09:26:19 2022

@author: CIL
"""
import numpy as np
import matplotlib.pyplot as plt
ts = 1.0 
t = np.arange(-50, 50, 1)

y = t ** 2 + t ** 3 + t ** 4 + t ** 5 + t ** 6
plt.plot(t, y)
plt.show()
