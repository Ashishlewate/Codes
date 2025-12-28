# Find the sum of numbers from 1 to n
n = int(input("Enter a number: "))

i = 1
total = 0

while i <= n:
    total = total + i
    i += 1

print("Sum is:", total)
