#exercise 1
## procedure to print two overlapping brick rows:
def print_bricks():
  print("--+-----+---")
  print("  |     |")
  print("-----+-----+")
  print("     |     |")
  

## repeat the two rows three times to make a higher wall:
print_bricks()
print_bricks()
print_bricks()

#exercise 2
amount = 1000
years = 3
rate = 5

final_amount = amount * ( 1 + (rate/100))**years
print(final_amount)

#exercise 3
import math

radius1 = 7
radius2 = 5.5

circumference1 = 2*math.pi*radius1
circumference2 = 2*math.pi*radius2

print(circumference1)
print(circumference2)

#exercise 4
interest = 0.058/365
loan_amount = 600000
years = 20
days = years*365

numerator = interest * ((1 + interest) ** days)
denominator = ((1 + interest) ** days) - 1

daily_payment = loan_amount * (numerator / denominator)
print(daily_payment)
