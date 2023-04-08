# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 14:02:48 2023

@author: ishik
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:11:06 2020

@author: eessrp
"""

import numpy as np  # abbreviates calls to np.
import time

start_time=time.time() # time at the start of execution
a=np.random.random((500,500))
b=np.random.random((2000,2000))

init_time=time.time() # time after initialising the two arrays

np.savetxt('Np_a.txt', a)  # writes a single numpy array to file
AA=np.loadtxt('Np_a.txt')  # reads in a single numpy array from file
diff=a-AA           # element by element difference between what was sent to the file and what is read back in
sum_diff=diff.sum() # add all of the difference elements together
if (sum_diff==0.0):
    print("Array a savetxt and loadtxt OK")
else:
    print("Array a savetxt and loadtxt failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
atxt_time=time.time()      # time after writing and reading  back a
np.savetxt('Np_b.txt', b)  # writes a single numpy array to file
BB=np.loadtxt('Np_b.txt')
diff=b-BB
sum_diff=diff.sum()
if (sum_diff==0.0):
    print("Array b savetxt and loadtxt OK")
else:
    print("Array b savetxt and loadtxt failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
btxt_time=time.time()        # time after writing and reading  back b


np.save('Np_a.npy', a)  # writes creates a file my_file.npy. .npy file contains a single numpy array
AA=np.load('Np_a.npy')
diff=a-AA
sum_diff=diff.sum()
if (sum_diff==0.0):
    print("Array a save and load OK")
else:
    print("Array a save and load failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
anpy_time=time.time()       # time after writing and reading back a in binary
np.save('Np_b.npy', b)  # writes creates a file my_file.npy. .npy file contains a single numpy array
AA=np.load('Np_b.npy')
diff=b-BB
sum_diff=diff.sum()
if (sum_diff==0.0):
    print("Array b save and load OK")
else:
    print("Array b save and load failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
bnpy_time=time.time()      # time after writing and reading back b in binary
#
#
np.savez('Np_ab.npz', a=a, b=b)
data = np.load('Np_ab.npz')   # all of the file is then in data
AA=data['a']   # find variable a in data
diff=a-AA
sum_diff=diff.sum()
if (sum_diff==0.0):
    print("Array a savez and load OK")
else:
    print("Array a savez and load failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
BB=data['b']
diff=b-BB
sum_diff=diff.sum()
if (sum_diff==0.0):
    print("Array b savez and load OK")
else:
    print("Array b savez and load failed")
    min_diff=diff.min()
    max_diff=diff.max()
    print("Diff range [%g : %g]")
abz_time=time.time()      # time after writing and reading back a and b in single binary file

#ZZ=data['z'] - returns an error as z is not in the file

data.close()   # data is opened as a file, so needs to be closed

# find the differences in the times to identify how long each part of the code took
print("Init took %g secs"%(init_time-start_time))
print("Atxt took %g secs"%(atxt_time-init_time))
print("Btxt took %g secs"%(btxt_time-atxt_time))
print("Anpy took %g secs"%(anpy_time-btxt_time))
print("Bnpy took %g secs"%(bnpy_time-anpy_time))
print("ABnpz took %g secs"%(abz_time-bnpy_time))
print("Whole program took %g secs"%(abz_time-start_time))
#
#a=np.array([[1.0, 2, 3.5], [4, 5.2, 6]])
#b=np.array([[8.0, 6, 1.5], [3, 1.2, 5.6]])
#arr = [20, 2, 7, 1, 34] 
#ab=np.array([[6.0, 5], [-3.5,-2], [1.2, 4.6]])
#
#tot = np.add(b,a)        # Addition of arrays
#diff = np.subtract(a,b)  # Subtraction of arrays
#prod = np.multiply(a,b)  # Multiplication of arrays
#ratio= np.divide(a,b)    # Division of arrays
#
#eb = np.exp(b)        # Exponentiation - element by element
#rt = np.sqrt(b)       # Square root - element by element
#SS = np.sin(a)        # Sine - element by element 
#CC = np.cos(b)        # Cosine - element by element 
#ln = np.log(a)        # Natural Logarithm - element by element 
#dotp = a.dot(ab)      # Dot product e.f - row by column
#
#S = a.sum()           # Array-wise sum of all elements
#Mi = a.min()          # Array-wise minimum value
#Ma = b.max(axis=0)    # Maximum value of an array row[0]
#Cs = b.cumsum(axis=1) # Cumulative sum of the elements in row[1]
#Mn = a.mean()         # mean of the array
#Me = np.median(arr)    # Median of the array
#Co = np.corrcoef(arr)  # Correlation coefficient of the array
#St = np.std(arr)       # Standard deviation of the array