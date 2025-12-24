with open("Practicefile.txt","r") as f:
    data = f.read()
    data_change = data.replace("java","python")
    print(data_change)
