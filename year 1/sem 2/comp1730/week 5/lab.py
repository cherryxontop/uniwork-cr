# activity 1

# task1
print("Hello, and welcome to the course!")

def foo():
    print("Hello, and welcome to the course!")

# task 2
"""
def foo(i):
  if i % 2 == 0:
    return True
  else:
    return False
"""
def is_even(i):
    if i % 2 == 0:
        return True
    else:
        return False


# activity 2

def count_occurrences (seq, target):
    """
    counts how many times target appears in sequence
    args:
        seq: a sequence (list) of int
        target (int): th valye to count occurences of
    returns:
        int: the number of times target appears in sequence
    """
    count = 0 #starts at 0
    for element in seq:
        if element == target:
            count += 1
    return count

def most_frequent_element(seq):
    """
    find the element that occurs most frequently in sequence
    args:
        seq: a non_empty sequent of int
    returns:
        int: the element with the highest number of occurences
    """
    most_frequent = None
    highest_count = 0
    for char in seq:
        char_count = count_occurrences(seq, char)
        if char_count > highest_count:
            highest_count = char_count
            most_frequent = char
    return most_frequent

# activity 3

# task 1
def is_prime_inline(n):
    # Step 1: reject non-int values
    if not isinstance(n, int) or isinstance(n, bool):
        return False
    # Step 2: if n is less than 2, it cannot be prime, so return False
    if n < 2:
        return False
    # Step 3: loop through possible divisors from 2 up to the square root of n
    for divisor in range(2, int(n ** 0.5) + 1):
        # Step 4: if n is divisible by any of these numbers, return False
        if n % divisor == 0:
            return False
    # Step 5: if no divisors were found, return True
    return True


# task 2
def is_prime_docstring(n):
    """
    determine whether n is a prime number.
    args: n (int): the number to check
    returns: bool: True if n is prime, False otherwise
    rejects non-int values
    Examples:
    is_prime_docstring(2) True
    is_prime_docstring(9) False
    is_prime_docstring(1) False
    is_prime_docstring(-5) False
    """
    if not isinstance(n, int) or isinstance(n, bool):
        return False
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True

# task 3
def is_prime_recursion(n, divisor=2):
    if not isinstance(n, int) or isinstance(n, bool):
        return False
    if n < 2:
        return False
    if divisor * divisor > n:
        return True
    if n % divisor == 0:
        return False
    return is_prime_recursion(n, divisor + 1)


# activity 4

def is_perfect_square(n):
    """
    determine whether n is a perfect square.
    args:
        n (int): the number to check
    returns:
        bool: True if n is a perfect square, False otherwise
    """
    # reject non-integer inputs (e.g. strings, lists, floats) before comparing
    if not isinstance(n, int) or isinstance(n, bool):
        return False
    # negative numbers can never be perfect squares
    if n < 0:
        return False
    # take the integer square root and check it maps back to n exactly,
    # avoiding floating-point rounding issues with n ** 0.5
    root = int(n ** 0.5)
    # the rounded root might be off by one due to floating-point error,
    # so check the values around it
    for candidate in (root - 1, root, root + 1):
        if candidate >= 0 and candidate * candidate == n:
            return True
    return False
