import sys

vowels = ("a", "e", "i", "o", "u")


def three_vowels(string: str) -> bool:
    # It contains at least three vowels (aeiou only),
    return len([x for x in string if x in vowels]) >= 3


def test_three_vowels():
    assert three_vowels("aei")
    assert three_vowels("xazegov")
    assert three_vowels("aeiouaeiouaeiou")


# It contains at least one letter that appears twice in a row
def contains_repeat(string: str) -> bool:
    for i in range(1, len(string)):
        if string[i - 1] == string[i]:
            return True
    return False


def test_contains_repeat():
    assert contains_repeat("xx")
    assert contains_repeat("abcdde")
    assert contains_repeat("dd")
    assert contains_repeat("aabbccdd")


# It does not contain the strings ab, cd, pq, or xy,
# even if they are part of one of the other requirements.
def does_not_contain_substr(string: str) -> bool:
    return not any([substr for substr in ["ab", "cd", "pq", "xy"] if substr in string])


def is_nice_string_part1(string: str) -> bool:
    return (
        three_vowels(string)
        and contains_repeat(string)
        and does_not_contain_substr(string)
    )


def test_examples_given_in_part1():
    assert is_nice_string_part1("ugknbfddgicrmopn")
    assert is_nice_string_part1("aaa")
    assert not is_nice_string_part1("jchzalrnumimnmhp")
    assert not is_nice_string_part1("haegwjzuvuyypxyu")
    assert not is_nice_string_part1("dvszwmarrgswjxmb")


# It contains a pair of any two letters that appears at least twice in the
# string without overlapping
def contains_pair_twice(string: str) -> bool:
    for i in range(1, len(string)):
        first_pair = (string[i - 1], string[i])
        for j in range(i + 2, len(string)):
            second_pair = (string[j - 1], string[j])
            if first_pair == second_pair:
                return True
    return False


def test_contains_pair_twice():
    assert contains_pair_twice("xyxy")
    assert contains_pair_twice("aabcdefgaa")
    assert not contains_pair_twice("aaa")


# It contains at least one letter which repeats with exactly one letter between
def repeats_separated(string: str) -> bool:
    for i in range(1, len(string) - 1):
        if string[i - 1] == string[i + 1]:
            return True
    return False


def test_repeats_separated():
    assert repeats_separated("xyx")
    assert repeats_separated("abcdefeghi")
    assert repeats_separated("aaa")


def is_nice_string_part2(string: str) -> bool:
    return contains_pair_twice(string) and repeats_separated(string)


def test_is_nice_string_part2():
    assert is_nice_string_part2("qjhvhtzxzqqjkmpb")
    assert is_nice_string_part2("xxyxx")
    assert not is_nice_string_part2("uurcxstgmygtbstg")
    assert not is_nice_string_part2("ieodomkazucvgmuy")


if __name__ == "__main__":
    num = 0
    for line in sys.stdin:
        if is_nice_string_part2(line):
            num += 1
    print(num)
