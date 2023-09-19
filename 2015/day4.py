import hashlib


def find_hash_starting_with(puzzle_input: str, prefix="00000"):
    i = 0
    while (
        not hashlib.md5((puzzle_input + str(i)).encode()).hexdigest().startswith(prefix)
    ):
        i += 1
    return i


def test_examples_given_in_part1():
    assert hashlib.md5("abcdef609043".encode()).hexdigest().startswith("00000")
    assert find_hash_starting_with("abcdef") == 609043
    assert find_hash_starting_with("pqrstuv") == 1048970


if __name__ == "__main__":
    puzzle_input = "bgvyzdsv"
    print(find_hash_starting_with(puzzle_input, prefix="000000"))
