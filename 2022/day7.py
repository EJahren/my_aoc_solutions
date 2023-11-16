import sys
from collections import defaultdict
from dataclasses import dataclass, field
from os.path import dirname
from typing import Dict, List, Optional


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    files: List[File] = field(default_factory=list)
    sub_directories: Dict[str, "Directory"] = field(default_factory=dict)
    parent: Optional["Directory"] = None
    abs_path: Optional[str] = None


all_directories = defaultdict(lambda: Directory())
all_directories["/"] = Directory([], {}, None, "/")


def read_listing(lines: List[str], current_directory: Directory) -> List[str]:
    if lines == []:
        current_directory.files = []
        current_directory.sub_directories = {}
        return []

    rest_of_lines = lines
    next_line = rest_of_lines[0]

    current_directory.files = []
    while not next_line.startswith("$"):
        if next_line.startswith("dir"):
            dir_name = next_line[4:]
            if dir_name not in current_directory.sub_directories:
                current_directory.sub_directories[dir_name] = Directory()
        else:
            size, name = next_line.split(" ")
            current_directory.files.append(File(name, int(size)))
        rest_of_lines = rest_of_lines[1:]
        if rest_of_lines == []:
            return []
        next_line = rest_of_lines[0]

    return rest_of_lines


def read_directories(lines: List[str], current_directory: Directory) -> Directory:
    if lines == []:
        return current_directory
    next_line = lines[0]
    rest_of_lines = lines[1:]
    if next_line.startswith("$ cd /"):
        change_to_dir_name = next_line[5:]
        to_dir = all_directories[change_to_dir_name]
        to_dir.abs_path = change_to_dir_name
        to_dir.parent = dirname(change_to_dir_name)
        return read_directories(rest_of_lines, to_dir)
    elif next_line.startswith("$ cd .."):
        if current_directory.parent is None:
            raise ValueError("Went beyond root directory")
        else:
            return read_directories(rest_of_lines, current_directory.parent)
    elif next_line.startswith("$ cd "):
        abs_dir = current_directory.abs_path
        change_to_dir_name = next_line[5:]
        if abs_dir is not None:
            change_to_dir_abs = abs_dir + change_to_dir_name + "/"
        else:
            change_to_dir_abs = None
        sub_dir = current_directory.sub_directories.get(change_to_dir_name, Directory())
        sub_dir.abs_path = change_to_dir_abs
        sub_dir.parent = current_directory
        return read_directories(rest_of_lines, sub_dir)
    elif next_line.startswith("$ ls"):
        rest_of_lines = read_listing(rest_of_lines, current_directory)
        return read_directories(rest_of_lines, current_directory)
    else:
        raise ValueError(f"Did not understand line '{next_line}'")


inp = [l[:-1] for l in sys.stdin]
# inp = """
# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k"""
# inp = [l for l in inp.split("\n") if len(l) > 0]
read_directories(inp, all_directories["/"])

sizes = {}


def calc_sizes(current_directory):
    if current_directory.abs_path in sizes:
        return sizes[current_directory.abs_path]
    size = 0
    for value in current_directory.sub_directories.values():
        sizes[value.abs_path] = calc_sizes(value)
        size += sizes[value.abs_path]
    for file in current_directory.files:
        size += file.size
        # sizes[current_directory.abs_path + file.name] = file.size
    sizes[current_directory.abs_path] = size
    return size


calc_sizes(all_directories["/"])
print(sum(v for v in sizes.values() if v <= 100000))
used_space = sizes["/"]
total_capacity = 70000000
needed_space = 30000000
remaining_capacity = total_capacity - used_space
target_to_delete = needed_space - remaining_capacity

closest = total_capacity
for value in sizes.values():
    if value > target_to_delete and abs(value - target_to_delete) <= abs(
        closest - target_to_delete
    ):
        closest = value
print(closest)
