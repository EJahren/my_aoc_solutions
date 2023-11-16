import sys

N = 14  # 4 for part1
if __name__ == "__main__":
    inp = next(sys.stdin)
    for i in range(len(inp)):
        if len(set(inp[i : i + N])) == N:
            print(i + N)
            break
