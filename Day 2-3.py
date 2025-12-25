class student:
    def __init__(self,name,marks,P,C,M):
        self.name = name
        self.marks = marks
        self.P= P
        self.C=C
        self.M=M
    print("Generating Details")
s1= student("Ashish Lewate ",100,97,88,96)
print(s1.name)
print(s1.P)
print(s1.C)
print(s1.M)

Average = (s1.P + s1.C + s1.M) / 3
s1.marks = Average
print("Total Marks",s1.marks)