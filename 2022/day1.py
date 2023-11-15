import sys

if __name__ == "__main__":
    totals = []
    current = 0
    for line in sys.stdin:
        if line == "\n":
            totals.append(current)
            current = 0
        else:
            current += int(line[:-1])
    print(max(totals))
    print(sum(sorted(totals)[-3:]))
