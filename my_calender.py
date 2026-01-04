import calendar

def glass(text):
    lines = text.splitlines()
    w = max(len(line) for line in lines)

    print("+" + "-" * (w + 2) + "+")
    for line in lines:
        print("| " + line.ljust(w) + " |")
    print("+" + "-" * (w + 2) + "+")

for m in range(1, 13):
    glass(calendar.month(2026, m))
