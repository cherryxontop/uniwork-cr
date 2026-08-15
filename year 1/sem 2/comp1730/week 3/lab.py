import math

#ex 1 ahhh
def babylonian_sqrt(a):
    if a <0:
        return "cannot compute square of a -ve number"
    if a ==0:
        return 0

    #take a guess
    x = a/2
    while abs(x**2 - a) > 1e-6:
        x = 0.5 * (x + a / x)
        
    return x

print(babylonian_sqrt(19))

#ex 2 ?
def sum_odd_digits(number):
    total=0
    while number > 0:
        digit = number % 10     #extracts last digit
        if digit % 2 != 0:      #checks odd or even
            total += digit      #adds to total if odd
        number //= 10           #shift every digit pe position to the right
    return total          #removes last digit
    pass

def sum_even_digits(number):
    total = 0
    while number > 0:
        digit = number % 10
        if digit % 2 == 0:
            total += digit
        number //= 10
    return total
    pass

def sum_all_digits(number):
    total = 0
    while number > 0:
        total += number % 10
        number //= 10
    return total
    pass

num = 30142
print(f"1: {sum_all_digits(num)}")    
print(f"2: {sum_odd_digits(num)}")     
print(f"3: {sum_even_digits(num)}")

#ex 3

def sum_all_digits(number):
    if number == 0:
        return 0
    return (number % 10) + sum_all_digits(number//10)

print(sum_all_digits(3029))

#ex 4
""" rewrite using `for` loop
def count_negative(sequence):
    count = 0
    index = 0
    while index < len(sequence):
        if sequence[index] < 0:
            count = count + 1
        index = index + 1
    return count 
"""
def count_negative(sequence):
    count = 0
    for item in sequence:
        if item < 0:
            count += 1
    return count


test1 = [-1, 0, -2, 1, -3, 2]
test2 = [i for i in range(-10, 10, 3)]
test3 = [-1, -1, -1, -1, -1]
test4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print(f"test 1 ({test1}): {count_negative(test1)}")
print(f"test 2 ({test2}): {count_negative(test2)}")
print(f"test 3 ({test3}): {count_negative(test3)}")
print(f"test 4 ({test4}): {count_negative(test4)}")

#ex5

def is_increasing(sequence):
    for i in range(len(sequence)-1):
        if sequence[i] > sequence[i+1]:
            return False
    return True
    pass

print(is_increasing([1, 5, 9]))      
print(is_increasing([3, 3, 4]))      
print(is_increasing([3, 4, 2]))      
print(is_increasing([]))            
print(is_increasing([7]))

#ex 6 lowk bum
def most_average(numbers):
    avg = sum(numbers) / len(numbers)
    return min(numbers, key=lambda x: abs(x-avg))
    pass

print(most_average([1, 2, 4, 6, 8, 10]))

#ex 7 idk fi this is allowed
def smallest_greater(seq, value):
    greater = [x for x in seq if x > value]
    return min(greater) if greater else None
    pass

def greatest_smaller(seq, value):
    smaller = [x for x in seq if x < value]
    return max(smaller) if smaller else None
    pass

print(smallest_greater([13, -3, 22, 14, 2, 18, 17, 6, 9], 4))
print(greatest_smaller([13, -3, 22, 14, 2, 18, 17, 6, 9], 4))

#ex 8
def count_duplicates(sequence):
    seen = []
    dup = 0
    for item in sequence:
        if item in seen:
            dup += 1
        else:
            seen.append(item)
    return dup
    pass  

print(count_duplicates([-1, 2, 4, 2, 0, 4]))
print(count_duplicates("this should work methinks")) # why is it 10?        oh i get it

#ex 9 bum
def count_capitals(string):
    caps = 0
    for i in string:
        if 'A' <= i <= 'Z':
            caps += 1
    return caps
    pass
print(count_capitals("Its 2A.M. You and I oh fuck no im not doing this need sleep"))

#ex 10 magic 
def general_count(sequence, condition_function):
    count = 0
    for i in sequence:
        if condition_function(i):
            count += 1
    return count
    pass
def is_positive(x):
    return x>0
print(general_count([1,-1,2,3,5,-2], is_positive))

