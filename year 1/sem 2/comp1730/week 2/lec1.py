print("a", "b", "c")
print("a", "b", "c", sep="---") 
print("a", "b", "c", sep="\n")
print("a", "b", "c", sep="\t")

print(round(3.149, ndigits=2))

#|------ name -----|   |----| parameters 
def change_in_percent(old, new):
    diff = new - old            # -| block
    return (diff/old)*100       # -|   ^

# parameter values are set only when the function is called. 
# `return` is a statement, that when executed, cause the function call to end, and returns the value of the expression.

"""
>>> change_in_percent(100, 120)
"""                 # won't run, but call in console


"""
parameters are defined in the function definition
arguments are values passed to the function when its called.

parameters are what arguments become when they are in the code block of the function.

"""

def kinetic_energy(mass, velocity):
    formula = 1/2 * mass * (velocity)**2
    return formula

print(kinetic_energy(2, 3))

"""
the python interpreter always executes instructions one at a time in sequence, including expression evaluation
to evaluate a function call, the interpreter
-evaluates the argument expressions one at a time, from left to right
-executes the function body with its parameters assigned the values returned by the argument expressions

same with operators: first arguments (left to right), then the operation
"""
m