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

# views vs copies
- view = shared memory, copy = new memory allocation (similar idea in dictionaries)
- modifying a view changes the original!
```python
original = np.array([1, 2, 3, 4, 5])
view = original[1:4]        # slicing makes a VIEW
view[0] = 999
print(original)             # [1 999 3 4 5] - original changed

copy = original[1:4].copy() # .copy() makes independent memory
copy[0] = 0                 # original unaffected
```
## which operations make which
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# VIEWS
view1 = arr[1:3, :]      # slicing
view2 = arr.reshape(1, 9)  # reshape
view3 = arr.T            # transpose
# COPIES
copy1 = arr[arr > 5]     # boolean indexing
copy2 = arr[[0, 2], :]   # fancy indexing
copy3 = arr + 1          # arithmetic

np.shares_memory(arr, view1)  # True
np.shares_memory(arr, copy1)  # False
```
## best practice
- when you want to modify safely, copy first
```python
def process_array(data):
    working_data = data.copy()
    working_data[working_data < 0] = 0
    return working_data

original_data = np.array([-1, 2, -3, 4, -5])
processed = process_array(original_data)
# original_data -> [-1 2 -3 4 -5], processed -> [0 2 0 4 0]
```

# array operations and broadcasting
## element-wise ops
```python
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([10, 20, 30, 40])
arr1 + arr2    # [11 22 33 44]
arr2 - arr1    # [9 18 27 36]
arr1 * arr2    # [10 40 90 160]  (element-wise, NOT matrix mult)
arr2 / arr1    # [10. 10. 10. 10.]
arr1 ** 2      # [1 4 9 16]
arr2 > arr1    # [True True True True]
arr1 == arr2   # [False False False False]
```
- !!! cannot use `==` directly in if statements (gives an array of bools, not one bool)
- use `np.array_equal(arr1, arr2)` or `np.all(arr1 == arr2)`
## scalar ops
- all element-wise
```python
arr = np.array([1, 2, 3, 4])
arr * 5      # [5 10 15 20]
arr + 10     # [11 12 13 14]
arr ** 0.5   # [1. 1.414 1.732 2.]
```
## broadcasting
- allows operations between arrays of different shapes
```python
# 1D with scalar
np.array([1, 2, 3]) + 5     # [6 7 8]

# 2D with column vector
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
col_vector = np.array([[1], [2]])   # shape (2, 1)
arr2d + col_vector
# [[2 3 4]
#  [6 7 8]]

# more complex
arr3d = np.random.random((2, 3, 4))  # (2, 3, 4)
arr1d = np.array([1, 2, 3, 4])       # (4,)
arr3d + arr1d                        # (2, 3, 4)
```

# vectorisation
- applying operations to entire arrays at once instead of explicit loops
- this is where numpy's speed advantage shows up
```python
size = 1000000
python_list = list(range(size))
numpy_array = np.arange(size)

# method 1: pure python loop (SLOW)
def python_square(lst):
    result = []
    for x in lst:
        result.append(x ** 2)
    return result

# method 2: numpy vectorised (FAST)
def numpy_square(arr):
    return arr ** 2
```
- shorter, more readable code, closer to math notation
- IMPORTANT(!): cannot use `math.sin` and `math.exp` on entire arrays, must use `np.sin` and `np.exp`

# array manipulation
## reshaping
```python
arr = np.arange(12)            # [0 1 2 ... 11]
reshaped = arr.reshape(3, 4)   # 3x4 matrix
flattened = reshaped.flatten() # back to 1D
```
## joining and splitting
```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
combined = np.concatenate([arr1, arr2])  # [1 2 3 4 5 6]
stacked = np.stack([arr1, arr2])         # [[1 2 3]
                                         #  [4 5 6]]
split_arrays = np.split(combined, 2)     # [array([1, 2, 3]), array([4, 5, 6])]
```

# numpy summary
- much faster than lists (if vectorisation is used wisely)
- broadcasting enables powerful array operations
- views vs copies is crucial for memory management
- rich indexing for data selection
- extensive math and stats functions

---

# pandas overview
- python library for data manipulation and analysis
- built on top of numpy at its core
- pandas = "Panel Data System" (concept from econometrics)
- one of the most popular libs for data scientists
- docs + "10 minutes to pandas" tutorial recommended for new users
- two main data structures:
  - **Series**: 1D labeled data
  - **DataFrame**: 2D (tabular) labeled data, like a spreadsheet
- DataFrame is the primary one, but need Series too since restricting a DataFrame to one column or row gives a Series

# Series
- 1D mutable type, usually same-type elements (ints/floats)
- can technically mix types but not recommended (storage + performance)
- elements stored in a 1-rank numpy array
- unlike numpy arrays, has an **index** = sequence of labels for each element
- access by label OR integer position

## creating a series
```python
import pandas as pd
data = pd.Series([0.0, 0.25, 0.5])                    # default index 0,1,2
data1 = pd.Series([0.0, 0.25, 0.5], ['a', 'b', 'c'])  # custom index
data2 = pd.Series([0.0, 0.25, 0.5], [2, 1, 0])
```
- can create from list or numpy array
- no index passed -> integers from 0 assigned automatically

## accessing series elements
```python
data = pd.Series([0.0, 0.25, 0.5], ['a', 'b', 'c'])
data['b']     # 0.25 - by label
data[2]       # 0.5 - by integer position
data[0:2]     # slicing returns a new Series (a 0.00, b 0.25)
```
- if the index is integers, must use `.iloc` for position
```python
data = pd.Series([0.0, 0.25, 0.5], [2, 1, 0])
data[2]        # 0.0 - treated as LABEL
data.iloc[2]   # 0.5 - integer POSITION
```
- boolean sequence filters elements (same length as series)
```python
data[[False, True, True]]  # new Series: 1 0.25, 0 0.50
```

## operations with series
- descriptive stats
- sorting (by value or by index)
- comparison with a number (useful for filtering)
- vectorised ops (like numpy arrays)

# DataFrame
## creating
```python
data = pd.DataFrame([[184, 81.2], [175, 87.0], [162, 61.5]],
                    index=['P001', 'P002', 'P003'],
                    columns=['height', 'weight'])
```
- from list of lists or 2D numpy array
- index and columns optional, default to integers from 0
- `data.shape` -> (3, 2)
- **read_csv** is a flagship feature
```python
ppt_data = pd.read_csv("data.csv")
```
- also supports Excel, JSON, HDF5
- column labels taken from header (first row), index = integers from 0 by default
- lots of options, `help(pd.read_csv)`

## accessing (columns)
```python
data                          # all the data
data['weight']                # single column -> Series
data[['height', 'weight']]    # multiple columns -> DataFrame
data[1:3]                     # row slice -> new DataFrame
data[1:3]['weight']           # -> new Series
```
## accessing (rows by label) - needs `.loc`
```python
data.loc["P001"]               # single row -> Series
data.loc[["P001", "P002"]]     # multiple rows -> DataFrame
data.loc[["P002", "P003"]]["weight"]  # rows + column -> Series
```
## accessing (by position) - `.iloc`
- row or row+column integer positions, slicing works
- very similar logic to 2D numpy arrays
```python
data.iloc[1]        # row at position 1 -> Series
data.iloc[1, 0]     # row 1, col 0 -> single value
data.iloc[0:2, 0:2] # rows 0-1, cols 0-1 -> DataFrame
```

## operations with dataframe
- descriptive stats (same methods as Series)
- mixed numeric + non-numeric columns: `data.mean(numeric_only=True)`
```python
data.sort_values(by="height", ascending=False)  # sort by column values
data.sort_index(axis=0, ascending=False)        # sort by index
data.sort_index(axis=1, ascending=True)         # sort by column labels
```

# pandas take home
- powerful lib for data manipulation and analysis
- two main structures: Series and DataFrame
- import/export CSV, Excel etc
- only covered basics; other features: missing data handling, data cleaning, feature engineering for ML, time series

# computational thinking (Anderson 2016)
1. decomposition - break problem into manageable steps
2. pattern recognition - find repetitive patterns to design a solution more efficiently
3. abstraction - represent the patterns in a generalised form
4. algorithm design - systematic design of the solution
5. evaluation - check all steps give a comprehensive solution (some writers include debugging here)