#Take a number and check whether it is a 2-digit or 3-digit number
Num = int(input("Enter numbers :"))
if Num <= 10:
    print("1 digit", Num)
elif Num <= 100:
    print("2 digit", Num)
elif Num >= 1000:
    print("4 digit", Num)
else:
    print("3 digit",Num)