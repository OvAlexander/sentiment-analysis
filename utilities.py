import hashlib
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


if __name__ == '__main__':
    equals_test = "example"
    assert (string_to_rgb(equals_test) == string_to_rgb(equals_test))
    print(string_to_rgb(equals_test))
