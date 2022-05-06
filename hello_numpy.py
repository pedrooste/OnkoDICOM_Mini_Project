"""Numpy provides two basic objects: ndarray (N-dimensional Array Object) and ufunc (Universal Function Object).
ndarray is a multidimensional array that stores a single data type, while ufunc is a function that can manipulate arrays.


What is it used for?
    Creating n-dimensional arrays (matrices)
    Performing functions on arrays and is very convenient as there is no need to write loops
    Numerical integration, linear algebra operations, Fourier transforms
    ndarray is a fast, space-saving multi-dimensional array that provides array-based arithmetic operations and advanced broadcasting capabilities

Object
    The core object in NumPy is the ndarray
    The ndarray can be thought of as an array, holding similar elements
    All the functions in NumPy are based around the ndarray

    The ndarray consists internally of the following.
        - A pointer to the data (a piece of data in memory or a memory mapped file).
        - A data type, or dtype, describing a grid of fixed size values in the array.
        - A tuple that represents the shape (shape) of the array, indicating the size of each dimension. The shape is (row x col)
"""
import matplotlib.pyplot as plt
import numpy as np

# Using lists to generate arrays
lst = [1, 2, 3, 4]
nd1 = np.array(lst)
print(nd1, type(nd1))

# Generating arrays with the random module
# 0 to 1 standard normal distribution
arr1 = np.random.randn(3, 3)
# 0 to 1 evenly distributed
arr2 = np.random.rand(3, 3)
# Uniformly distributed random numbers (float), the first two parameters indicate the range of
# random numbers and the third indicates the number of random numbers generated
arr3 = np.random.uniform(0, 10, 2)
# Uniformly distributed random numbers (integers), the first two parameters indicate the range of random numbers and
# the third indicates the number of random numbers generated
arr4 = np.random.randint(0, 10, 3)
print(f'arr1 : {arr1}\narr2 : {arr2}\narr3 : {arr3}\narr4 : {arr4}')

# Specify a random seed so that the same data is generated each time
# np.random.seed()
# Disrupting the array
# np.random.shuffle()

# Creating an array of specific shapes
# uninitialized array
arr1 = np.empty((2, 3))
# Array elements filled with zeros
arr2 = np.zeros((2, 3))
# Array elements are padded with 1
arr3 = np.ones((2, 3))
# Array is padded by the specified number, here is example 3
arr4 = np.full((2, 3), 3)
# Generate units with elements on the diagonal as 1 and others as 0
arr5 = np.eye(2)
'''Two-dimensional matrix outputs the elements of the matrix diagonal, one-dimensional matrix forms a matrix with a
one-dimensional array as the diagonal elements'''
arr6 = np.diag(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
'''When creating an equal series of a given length, it is important to note that the array formed by np.linspace must 
include the first two elements of the range, so the step size is (end - start) / (length - 1). np.array is a 
self-specified step (the default is 1), which means that the array formed does not necessarily include the last number 
'''
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
a[0, 1: 3] = 100, 101  # a[0 , 1 : 3] means the second column of the first row and the second column i.e. [2, 3]
a

# Slicing of multidimensional arrays
x = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
rows = np.array([[0, 0], [3, 3]])  # for rows 1 and 4
cols = np.array([[0, 2], [0, 2]])  # for columns 1 and 3
y = x[rows, cols]
y

# Boolean Index
x = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
print(x[x > 5])  # out : [ 6  7  8  9 10 11]
b = x > 5
b

# Find element
a = np.array([2, 4, 6, 8, 10, 3]).reshape(2, 3)
c = np.where(a > 5)  # out : (array([0, 1, 1], dtype=int64), array([2, 0, 1], dtype=int64))
a[c]  # get element

# Delete element
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
np.delete(arr, [1], 0)  # represent delete 2nd row

# Splicing
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.hstack((a, b))  # equivalent to np.concatenate((a, b), axis = 1)
# out : array([[1, 2, 5, 6], [3, 4, 7, 8]])

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.vstack((a, b))  # is equivalent to np.concatenate((a, b), axis = 0)
# out : array([[1, 2], [3, 4], [5, 6], [7, 8]])

# Splitting
x = np.arange(12).reshape(3, 4)
np.split(x, 3)
# out : [array([[0, 1, 2, 3]]), array([[4, 5, 6, 7]]), array([[ 8,  9, 10, 11]])]

y = np.arange(9).reshape(1, 9)
np.split(y, 3, axis=1)
# out : [array([[0, 1, 2]]), array([[3, 4, 5]]), array([[6, 7, 8]])]

# Numpy numerical calculations(ufunc)
# sum
a = np.array([[6, 3, 7, 4, 6], [9, 2, 6, 7, 4], [3, 7, 7, 2, 5], [4, 1, 7, 5, 1]])
np.sum(a, axis=0)
# out : array([22, 13, 27, 18, 16])
np.sum(a, axis=1)
# out : array([26, 28, 24, 18]

# min
arr = np.array([[10, 11, 12], [13, 14, 15]])
np.min(arr, axis=0)
# out : array([10, 11, 12]) Min by row, i.e. columns stay the same, rows change
np.min(arr, axis=1)
# out : array([10, 13]) Minimize by column, i.e. rows stay the same, columns change

# argmin
arr = np.array([[10, 14, 12], [13, 11, 15]])
np.argmin(arr, axis=0)
# out : array([0, 1, 0], dtype=int64) min by row, i.e. columns stay the same, rows change
np.argmin(arr, axis=1)
# out : array([0, 1], dtype=int64) Minimize by column, i.e. rows stay the same, columns change

# sort and argsort
arr = np.array([1, 3, 5, 2, 4])
np.sort(arr)
# out : array([1, 2, 3, 4, 5])
np.argsort(arr)
# out : array([0, 3, 1, 4, 2], dtype=int64)

# Matrix operations
# Element-Wise Product
a = np.array([[1, 0], [0, 1]])
b = np.array([[4, 1], [2, 2]])
np.multiply(a, b)
# equivalent to a * b, out : array([[4, 0], [0, 2]])
'''
| 1  2|   |2  0|   | 2  0 |
|     | * |    | = |      |
|-1  4|   |3  4|   |-3  16|
'''

# Dot Product
a = np.array([[1, 0], [0, 1]])
b = np.array([[4, 1], [2, 2]])
np.dot(a, b)
# equivalent to np.matmul(a, b) out : array([[4, 1], [2, 2]])

# Calculating the value of a determinant
arr = np.array([[1, 2], [3, 4]])
np.linalg.det(arr)
# out : -2.0000000000000004

# inverse
np.linalg.inv(arr)
# out : array([[-2. ,  1. ], [ 1.5, -0.5]])

# eigenvalues and eigenvectors
A = np.random.randint(-10, 10, (4, 4))
C = np.dot(A.T, A)
vals, vecs = np.linalg.eig(C)
print(f'eigenvalues : {vals}, eigenvectors : {vecs}')

# Interpolation operations
x = np.linspace(0, 2 * np.pi, 10)
y = np.sin(x)

xvals = np.linspace(0, 2 * np.pi, 10000)
yinterp = np.interp(xvals, x, y)

plt.plot(x, y, 'r-', xvals, yinterp, 'b-')
plt.show()

# Curve Fitting
x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
# Get the coefficients of the polynomial
z = np.polyfit(x, y, 3)
z2 = np.polyfit(x, y, 5)
#Get the polynomial function
f = np.poly1d(z)
f2 = np.poly1d(z2)
#Fit with two functions
xval = np.linspace(0, 10, 50)
yval1 = f(xval)
yval2 = f2(xval)
#plot
plt.plot(xval, yval1, 'r--o', xval, yval2, 'b-o')
plt.legend(['The deg is 3', 'The deg is 5'])
plt.show()

print(f)
print(f2)

#Numpy IO
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# Save data
np.save('test.npy', arr)
# Download the data
np.load('test.npy')
# out : array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

