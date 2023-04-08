# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:47:03 2023

@author: ishik
"""

import numpy as np

A = np.array([[3.0,3.0],[3.0,3.0]])
B = np.array([[3.0,3.0],[3.0,3.0]])


A[0][0]=1.0
A[0][1]=3.0
A[1][0]=-2.0
A[1][1]=1.0

B[0][0]=-2.0
B[0][1]=1.0
B[1][0]=2.0
B[1][1]=3.0

C = np.dot(A,B)
D = np.add(A,B)
E = np.multiply(A,B)



print(A)
print ('\n')
print(B)
print ('\n')
print(C)
print ('\n')
print(D)
print ('\n')
print(E)



