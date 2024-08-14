import sys
import argparse
import random
import hashlib
import csv
from calc import scale
# Generates random color based on string


def string_to_rgb(s):
    # Create a hash of the string
    hash_object = hashlib.md5(s.encode())
    hex_dig = hash_object.hexdigest()

    # Convert the first 6 characters of the hash to an RGB value
    r = int(hex_dig[0:2], 16)
    g = int(hex_dig[2:4], 16)
    b = int(hex_dig[4:6], 16)

    # Scale rgb values to match matplotlib color settings
    r = scale(r, 0, 255, 0, 1)
    g = scale(g, 0, 255, 0, 1)
    b = scale(b, 0, 255, 0, 1)

    return (r, g, b)


def get_names(file: str):
    names = []
    with open(file, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in rows:
            last_name = row[0][1:len(row[0])]
            first_name = (row[1][1:-1])
            names.append((first_name, last_name))
        names.pop(0)
        names.pop(0)
    return names


def makeGroup(lines, group_size, group_num):
    leftovers = len(lines) % group_size

    group = random.sample(lines, group_size)
    for x in group:
        lines.remove(x)
    print("Group ", group_num, ": ", group)
    return lines, group_size, group_num


if __name__ == '__main__':
    equals_test = "example"
    assert (string_to_rgb(equals_test) == string_to_rgb(equals_test))
    print(string_to_rgb(equals_test))

    names = get_names(
        "_BWSI 2024 UAS-SAR (Synthetic Aperture Radar) Attendance - Sheet1.csv")
    print(names)
