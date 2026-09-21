# numpy arrays
- arrays are a generisation of vectors where we can have more than one index.
- the number of indices is the number of dimensions of the array (vectors are 1D and matrices are 2D)
- must be homogeneous data and not nested lists(for computational efficiency)
- can represent only elements of same type like int float etc
- have a fixed size
- can have arbitrary dimensions
- code written on numpy arrays can be vectorized- rewritten using operations on entire arrays 

# creating numpy arrays
## from lists
```python
arr_1d = np.array([1,2,3,4,5])
arr_2d = np.array([[1,2,3], [4,5,6]])
```
## built-in funcs
```python
# arrays of zeros and ones
zeros = np.zeros((3, 4)) # 3x4 array of zeros
ones = np.ones((2, 3)) # 2x3 array of ones
empty = np.empty((2, 2)) # uninitialized array
# ranges
range_arr = np.arange(0, 10, 2) # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5) # [O. 0.25 0.5 0.75 1.0]
# random arrays
random_arr = np.random.random((3, 3)) # 3x3 random
```
# array attributes and data types
## array attributes
```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape) # (2, 3) - dimensions 
print(arr.size) # 6 - total elements 
print(arr.ndim) # 2 - num of dimensions 
print(arr.dtype) # int64 - data type
```
## data types
```python
# integer types
int_arr = np.array([1, 2, 3], dtype=np.int32)
# float types
float_arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
# boolean
bool_arr = np.array([True, False, True])
# converting types
arr_float = int_arr.astype(np.float64)
```

# array indexing and slicing
## 1D arrays
exact same way as lists
## 2D arrays
```python
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# single element
print(arr2d[1, 2]) # 6
# rows and columns
print(arr2d[0, :]) print(arr2d[:, 1]) print(arr2d[O]) 
# [1 2 3] - first row
# [2 5 8] - second column
# [1 2 3] - first row

# slicing
print(arr2d[:2, 1:]) # [1 2 3]
                     # [5 6]
print(arr2d[2,:-1]) # [9 8 7]
```
## boolean indexing
```python
arr = np.array([1, 2, 3, 4, 5, 6])
# boolean condition
mask = arr > 3
print(mask) print(arr[mask]) # [4 5 6]
# [False False False True True True]
# direct boolean indexing
print(arr[arr > 3]) # [4 5 6] 
print(arr[arr % 2 == O]) # [2 4 6]
```
as opposed to lists, legal to assign single number to array slice
```python
x = np.linspace(0, 1, 5) # [0. 0.25 0.5 0.75, 1.]
[1:3] = 10.0
print(x) # array ([O., 10., 10., 0.75, 1.])
```

