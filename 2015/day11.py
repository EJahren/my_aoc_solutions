from functools import reduce

start_ord = ord("a")
end_ord = ord("z")
ord_range = end_ord - start_ord


def increment(password: str) -> str:
    """
    >>> increment("a")
    'b'
    >>> increment("b")
    'c'
    >>> increment("z")
    'aa'
    >>> increment("aa")
    'ab'
    """
    passarray = [x for x in password]
    i = len(passarray) - 1
    while True:
        if i < 0:
            passarray = ["a"] + passarray
            break
        a = passarray[i]
        chr_ord = ord(a)
        wrap_around = chr_ord + 1
        if wrap_around > end_ord:
            passarray[i] = "a"
            wrap_around = start_ord
            i -= 1
        else:
            passarray[i] = chr(wrap_around)
            break
    return reduce(lambda a, b: a + b, passarray)


def requirement_one(password):
    """
    >>> requirement_one("hijklmmn")
    True
    >>> requirement_one("abbceffg")
    False
    """
    for i in range(len(password) - 2):
        a = ord(password[i])
        b = ord(password[i + 1])
        c = ord(password[i + 2])
        if a == b - 1 and b == c - 1:
            return True
    return False


def requirement_two(password):
    """
    >>> requirement_two("hijklmmn")
    False
    >>> requirement_two("abbceffg")
    True
    """
    return all(banned not in password for banned in ["i", "o", "l"])


def requirement_three(password):
    """
    >>> requirement_three('abcdffaa')
    True
    >>> requirement_three("abbceffg")
    True
    >>> requirement_three("abbcegjk")
    False
    """
    pair_positions = set()
    for i in range(len(password) - 1):
        a = password[i]
        b = password[i + 1]
        if a == b:
            pair_positions.add(i)
            pair_positions.add(i + 1)

    return len(pair_positions) >= 4


def next_password(password):
    password = increment(password)
    while (
        not requirement_one(password)
        or not (requirement_two(password))
        or not (requirement_three(password))
    ):
        password = increment(password)
    return password


if __name__ == "__main__":
    inp = "hepxxyzz"
    print(next_password(inp))
