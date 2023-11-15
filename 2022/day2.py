import sys


def points1(elf, you):
    match (elf, you):
        case ("A", "X"):
            return 1 + 3
        case ("A", "Y"):
            return 2 + 6
        case ("A", "Z"):
            return 3 + 0
        case ("B", "X"):
            return 1 + 0
        case ("B", "Y"):
            return 2 + 3
        case ("B", "Z"):
            return 3 + 6
        case ("C", "X"):
            return 1 + 6
        case ("C", "Y"):
            return 2 + 0
        case ("C", "Z"):
            return 3 + 3


def points2(elf, you):
    match (elf, you):
        case ("A", "X"):
            return 3 + 0
        case ("A", "Y"):
            return 1 + 3
        case ("A", "Z"):
            return 2 + 6
        case ("B", "X"):
            return 1 + 0
        case ("B", "Y"):
            return 2 + 3
        case ("B", "Z"):
            return 3 + 6
        case ("C", "X"):
            return 2 + 0
        case ("C", "Y"):
            return 3 + 3
        case ("C", "Z"):
            return 1 + 6


if __name__ == "__main__":
    print(sum(points2(*line.split()) for line in sys.stdin))
