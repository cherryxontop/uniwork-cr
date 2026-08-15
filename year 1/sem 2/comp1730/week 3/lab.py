import math

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

#ex 2
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

if __name__ == "__main__":
    num = 30142
    print(f"{num}")
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

if __name__ == "__main__":
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

if __name__ == "__main__":
    print(is_increasing([1, 5, 9]))      
    print(is_increasing([3, 3, 4]))      
    print(is_increasing([3, 4, 2]))      
    print(is_increasing([]))            
    print(is_increasing([7]))

#ex 6
print("the possesive form of 'it' is 'its'")