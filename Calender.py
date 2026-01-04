import Calender
def glass(text):
    lines=text.splitlines()
    w =max(len(l) for l in lines)
    print("."+"-"*(w+2)+".")
    for l in lines:
        print("|"+l.ljust(w)+"|")
    print("."+"-"*(w+2)+".")
for m in range(1,13):
    glass(Calender.month(2026,m))
    