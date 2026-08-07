#exercise 1
def print_grade(mark):
    if mark >= 80:
        print("High Distinction")
    elif mark >= 70:
        print("Distinction")
    elif mark >= 60:
        print("Credit")
    elif mark >= 50:
        print("Pass")
    else:
        print("Fail")

print(print_grade(48))
print(print_grade(78))
print(print_grade(52))

#exercise 2
def income_tax(income):
    if income <= 18200:
        return 0.0
    elif income <= 45000:
        return (income-18200)*0.16
    elif income <= 135000:
        return 4288 + (income - 45000)*0.3
    elif income <= 190000:
        return 31288 + (income - 135000)*0.37
    else:
        return 51638 + (income - 190000)*0.45
    pass

print(income_tax(500000))

#exercise 3
"""
The median of three numbers, a, b and c, is the one that ends up in the middle when the numbers are sorted in increasing order. 
For example, the median of -2, 7 and 9 is 7, and the median of 7, 9 and -2 is also 7. 
Write a function median with three parameters a,b, and c, which returns the median of its three arguments. 

"""
def median(a, b, c):
    if (a >= b and a <= c) or (a <= b and a >= c):
        return a
    elif (b >= a and b <= c) or (b <= a and b >= c):
        return b
    else:
        return c
    pass

print(median(3, 1, 2))
print(median(1, 2, 3))

#exercise 4
"""
The price of a book is $24.95, but an online book seller is offering a 40% discount. 
The shipping cost is $3 for the first copy and $0.75 for each additional copy.
Write a function, total_price(n), that takes the number of copies ordered and returns the total price.

"""
def total_price(n):
    og_price = 24.95
    discounted_price = 24.95*0.6
    if n<=0:
        return 0
    else:
        shipping = 3 + (n-1)*0.75
        total = (discounted_price*n) + shipping
        return total
    pass

print(total_price(1))
print(total_price(2))
print(total_price(10))