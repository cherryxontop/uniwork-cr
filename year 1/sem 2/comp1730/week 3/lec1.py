"""
ITERATION
iteration is the ability to repeatedly run a block a statements in a controlled manner- whe to start/stop/repeat
    `while` loops
        repeats a block of statements as long as a condition remains true.
        useful for looping an indeterminate number of times, until a condition is satisfied
    `for` loops
        iterates through the elements of a collection or sequence
        useful for looping a defined number of times
    `break` to exit a loop
    `continue` to go around again
    `pass` to do nothing

STRING VARIABLES AND LISTS ARE SEQUENCES- to access each character in a string, we use index values enclosed in []. starts from 0

`for` statement syntax: its liek hthe `while` statement syntax, except it has a list to work thru. they are bounded, unlike `while` which can be an infinite loop

"""

hello_world = "Hello, World!"

for letter in hello_world:
    print(letter)

list = ['a', 'b', 'c', 1.1, 3, 500]
for value in list:
    print(str(value))



def is_word_a_color(word):
    colors = ['red', 'green', 'yellow', 'blue']
    for c in colors:
        if word == c:
            return True
    return False

print(is_word_a_color('red'))
print(is_word_a_color('cyan'))


"""
`for` with `range()`
"""

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, ' equals ', x, ' * ', int(n/x))
            break
    else:
        print(n, ' is a prime number')


for num in range(2,10):
    if num % 2 == 0:
        print("found an even number", num)
        continue
    print("found an odd number", num)

"""escape characters for quotation marks etc. \n for new line, \t for tab, etc"""

fact = "The world's largest rubber duck was 54'2\" by 65'7\" by 105'"
print(fact)

palindrome = 'a man, \na plan, \na canal, \npanama'
print(palindrome)


"""string connection(1) and interpolation(2)"""
name = "chhaya"
age = 18
print('hello, my name is ' + name + ', and i\'m ' + str(age) + ' years old.')
print('hello, my name is %s, and i\'m %s years old' %(name, age)) 

# strings are immutable. once it is assigned, we need to reassign the entire thing to change it
greeting = 'Hello, world!'
new_greeting = 'J' + greeting[1: ]
print(new_greeting)