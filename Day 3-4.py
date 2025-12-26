class BANK :
    bank_name = "HDFC BANK"

    def __init__(self,Balance,Account):
        self.Balance = Balance
        self.Account = Account

Acc1 = BANK(10000,12345)
print("Total Balance is:",Acc1.Balance)
print("Acc Details is :",Acc1.Account)

ATM = input("Deposit or Withdraw:")
if ATM == "Deposit":
    credit=Acc1.Balance + int(input("Enter amount:"))
    print(credit)
else:
    debit = Acc1.Balance - int(input("Enter amount:"))
    print(debit)    


