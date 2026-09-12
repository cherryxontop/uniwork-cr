
# 1. Code Quality

## What is code quality?

Writing code that runs is not the same as writing good code.

Good code should be:
- correct
- understandable
- readable
- maintainable

A lot of programming time is spent finding and fixing bugs, so code should be written in a way that makes mistakes easier to find.

> Good code = correct + understandable + maintainable

---

# 2. Main Aspects of Code Quality

Three important areas are:

### 1. Commenting and documentation
Explain what the code does and why.

### 2. Variable and function naming
Names should make the purpose of the code obvious.

### 3. Code organisation
Large programs should be broken into sensible pieces.

Important tools:
- functions
- modules
- classes

---

# 3. PEPs

## What is a PEP?

PEP = Python Enhancement Proposal.

### PEP 8
Python's style guide. It gives recommendations for writing readable Python code.

### PEP 20
"The Zen of Python".

An important idea is:

> Readability counts.

### PEP 257
Deals with docstrings and conventions for writing them.

---

# 4. Comments

A good comment should explain:
- what the code is doing
- why it is doing it
- assumptions being made
- important conditions

A good comment should raise the level of abstraction.

Bad:
```python
x = x + 1
# Add 1 to x
```

Better:
```python
x = x + 1
# Move to the next stop
```

Good comments should be:
- up-to-date
- close to the code they describe
- useful to the reader

---

# 5. Docstrings

A docstring is documentation placed inside a function, module or class.

Example:

```python
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    """
```

A function docstring can describe:
- purpose
- parameters
- optional parameters
- assumptions
- limitations
- side effects
- return value

Think:

> Comments explain code. Docstrings document functions/classes/modules.

---

# 6. Naming

Good names make code easier to understand.

Bad:
```python
def f(x):
```

Better:
```python
def calculate_average(numbers):
```

Avoid names that conflict with Python built-ins:

```python
list = [1, 2, 3]
str = "hello"
sum = 10
```

Python names can be reasonably long:

```python
number_of_students
average_temperature
total_distance_travelled
```

---

# 7. Code Organisation

Good organisation:
- avoids repetition
- separates different problems
- isolates complexity
- makes code easier to read
- makes code easier to modify

Python gives us:
```text
Functions
   ↓
Modules
   ↓
Classes
```

---

# 8. Functions and Abstraction

Functions separate:

> what something does from how it does it.

Example:

```python
average = calculate_average(numbers)
```

The rest of the program does not need to know every step used to calculate the average.

A good function will usually do one thing.

---

# 9. Dictionaries

A dictionary stores data as:

```text
key → value
```

Example:

```python
student_marks = {
    "Alice": 85,
    "Bob": 72,
    "Charlie": 91
}
```

Dictionaries are useful for:
- lookup tables
- associating values with names/IDs
- combining information from datasets

---

# 10. Lists vs Dictionaries

List:
```python
names = ["Alice", "Bob", "Charlie"]
print(names[0])
```

Dictionary:
```python
marks = {
    "Alice": 85,
    "Bob": 72
}
print(marks["Alice"])
```

Think:

```text
List:
index → value

Dictionary:
key → value
```

---

# 11. Creating a Dictionary

Empty dictionary:
```python
numbers = dict()
```

Add values:
```python
numbers[1] = "one"
numbers[2] = "two"
```

Or create it immediately:
```python
numbers = {
    1: "one",
    2: "two",
    3: "three"
}
```

Remember:

```text
{}       → empty dictionary
[]       → used to access a dictionary key
:        → separates key and value
```

---

# 12. Adding and Updating Dictionary Values

```python
marks = {
    "Alice": 80
}
```

Add:
```python
marks["Bob"] = 75
```

Update:
```python
marks["Alice"] = 90
```

Same syntax:
```python
dictionary[key] = value
```

If the key does not exist, a new pair is created.

If the key exists, its value is replaced.

---

# 13. Iterating Through a Dictionary

Loop through keys:
```python
for key in numbers:
    print(key)
```

Access values:
```python
for key in numbers:
    print(numbers[key])
```

Loop through both:
```python
for key, value in numbers.items():
    print(key, value)
```

Useful methods:
```python
numbers.keys()
numbers.values()
numbers.items()
```

---

# 14. Word Frequency Example

For:

```text
cat dog cat bird dog cat
```

we want:

```python
{
    "cat": 3,
    "dog": 2,
    "bird": 1
}
```

Basic approach:

```python
counts = dict()

for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
```

Important pattern:

```text
word → frequency
```

---

# 15. KeyError

If you access a key that does not exist:

```python
numbers = {
    1: "one",
    2: "two"
}

print(numbers[6])
```

Python produces:

```text
KeyError
```

Check first:

```python
if "Alice" in marks:
    print(marks["Alice"])
else:
    print("Student not found")
```

---

# 16. try / except

Another way to handle errors:

```python
try:
    print(numbers["six"])
except:
    print("Key not defined")
```

General structure:

```text
try:
    risky code
except:
    what to do if an error occurs
```

---

# 17. Removing Dictionary Entries

### del
```python
del numbers[key]
```

### pop()
```python
value = numbers.pop(key)
```

This removes the key and returns its value.

### popitem()
```python
numbers.popitem()
```

Removes and returns the last inserted key-value pair.

---

# 18. Copying Dictionaries

Dictionaries are mutable.

To make a shallow copy:

```python
new_dictionary = old_dictionary.copy()
```

This creates a separate dictionary object.

---

# 19. Sets

A set is a collection of distinct values.

```python
numbers = {1, 2, 3, 4}
```

Duplicates are automatically removed.

```python
letters = set("AGATGATT")
```

An empty set is:

```python
set()
```

Important:

```python
{}
```

is an empty dictionary, not an empty set.

---

# 20. Set Operations

Suppose:

```python
A = {1, 2, 3}
B = {3, 4, 5}
```

Union:
```python
A | B
```
Result:
```python
{1, 2, 3, 4, 5}
```

Intersection:
```python
A & B
```
Result:
```python
{3}
```

Difference:
```python
A - B
```
Result:
```python
{1, 2}
```

Symmetric difference:
```python
A ^ B
```
Result:
```python
{1, 2, 4, 5}
```

---

# 21. Files and I/O

I/O means Input / Output.

Files allow data to be stored outside the running program.

Typical workflow:

```text
File
 ↓
Read data
 ↓
Process data
 ↓
Write results
 ↓
File
```

---

# 22. Persistence

Normally:

```text
Program starts
     ↓
Variables stored in memory
     ↓
Program finishes
     ↓
Memory is gone
```

Persistence means storing information so it survives after the program ends.

Examples:
- files
- databases
- Python pickle

---

# 23. CSV Files

CSV = Comma-Separated Values.

Example:

```text
name,age,mark
Alice,19,85
Bob,20,72
Charlie,18,91
```

Commas separate columns.

TSV files use tabs instead of commas.

---

# 24. Text vs Binary Files

Text files:
```text
.txt
.csv
.py
```

Binary files:
```text
.jpg
.png
.pdf
```

At a low level, files contain bytes which programs interpret as different types of data.

---

# 25. Newline Characters

Text files commonly use:

```python
"\n"
```

for a new line.

Tabs use:

```python
"\t"
```

When reading line-by-line, the newline may be included in the returned string.

---

# 26. File Paths

Absolute path:
```text
/Users/chhaya/Documents/data.csv
```

Relative path:
```text
data.csv
```

A relative path is interpreted relative to the current working directory.

---

# 27. Opening Files

Basic syntax:

```python
open(filename, mode)
```

| Mode | Meaning |
|---|---|
| `"r"` | read |
| `"w"` | write |
| `"x"` | create/write only if file doesn't exist |
| `"a"` | append |

---

# 28. Reading a File

```python
fin = open("data.txt", "r")

line = fin.readline()

fin.close()
```

`readline()` reads the next line.

The returned line is a string and normally contains its ending newline.

---

# 29. Writing to a File

```python
fout = open("output.txt", "w")

fout.write("Hello")

fout.close()
```

---

# 30. File Objects

When Python opens a file, it creates a file object.

You use it to:
- read
- write
- close
- perform other file operations

General pattern:

```text
open
 ↓
use
 ↓
close
```

---

# ⭐ Lecture 07 — Things to Remember

## Code quality
```text
Good code
= correct
+ readable
+ maintainable
```

## Dictionaries
```python
dictionary[key] = value
```

## Dictionary loop
```python
for key, value in dictionary.items():
```

## Missing key
```text
KeyError
```

## Sets
```python
A | B     # union
A & B     # intersection
A - B     # difference
A ^ B     # symmetric difference
```

## Files
```python
open(filename, mode)
```

Modes:
```text
r = read
w = write
x = create
a = append
```
