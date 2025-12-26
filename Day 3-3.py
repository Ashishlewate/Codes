#Take cost price and selling price and find profit or loss
CP = int(input("CP:"))
SP = int(input("SP:"))

if SP <= CP:
    print("Loss")
    Loss = CP - SP
    print(Loss)
else:
    print("Profit")
    Profit = SP - CP
    print(Profit)
