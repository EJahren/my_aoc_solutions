import sys

sys.setrecursionlimit(1000)


def look_and_say(inp: str) -> str:
    if inp == "":
        return ""

    output = ""
    first_digit = inp[0]
    num_copies = 1
    inp = inp[1:]
    for c in inp:
        if c == first_digit:
            num_copies += 1
        else:
            output += str(num_copies) + first_digit
            num_copies = 1
            first_digit = c
    output += str(num_copies) + first_digit
    return output


def test_look_and_say():
    assert look_and_say("211") == "1221"
    assert look_and_say("111") == "31"
    assert look_and_say("1") == "11"
    assert look_and_say("11") == "21"
    assert look_and_say("21") == "1211"
    assert look_and_say("1211") == "111221"
    assert look_and_say("111221") == "312211"


if __name__ == "__main__":
    inp = next(sys.stdin)[:-1]
    for i in range(50):
        inp = look_and_say(inp)
    print(len(inp))
