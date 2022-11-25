# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 05:32:27 2022

@author: CIL
"""
g = "*"
b1 = 'P99999261B\P@@@@j0VjS8@Sl@A@#@Sl3@DBp@V4Dq5Dr5DX6ae-7@@m<BJ 2@A}@uF"@A~<BG TSmE@J@J@J@J@J@I'
b2 = 'P99999261B\P@@@@j0VjS8@Sl@A@#@Sl3@DBp@V4Dq5Dr5DX6ae-7@@m<BJ TSmE@J@J@J@J@J@I'
b3 = 'P99999261B\P@@@@j0VjS8@Sl@A@#@Sl3@DBp@V4Dq5Dr5DX6ae-7@@m<BJ 2@A}@uF"@A~<BG '
b4 = 'P99999261B\P@@@@j0VjS8@Sl@A@#@Sl3@DBp@V4Dq5Dr5DX6ae-7@@m<BJ '
b5= 'P99999261B\P@@@@j0VjS8@Sl@A@#@Sl3@DBp@V4Dq5Dr5DX6ae-7@@m<BJ'
def addon(b, g):
    idx_f = b.rfind(" ")
    cnt = b.count(" ")
    print(cnt)
    if idx_f == -1:
        print(b)
        pass
    else:
        b = b[:idx_f + 1] + g + b[idx_f + 1:]
        if cnt == 2:
            b = b.replace(" ", "", 1)
    return b

b1 = addon(b1, g)
b2 = addon(b2, g)
b3 = addon(b3, g)
b4 = addon(b4, g)
b4 = addon(b5, g)