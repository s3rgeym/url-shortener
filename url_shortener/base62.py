import string
import uuid

# Возможно, стоило бы использовать base66 (можно дополнительно использовать: "~", "-", "_", ".")
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE62_LEN = len(BASE62)
assert BASE62_LEN == 62


def encode(x: str | uuid.UUID) -> str:
    n = int(str(x).replace("-", ""), 16)
    rv = ""
    while n > 0:
        rv += BASE62[n % BASE62_LEN]
        n //= BASE62_LEN
    return rv[::-1]


# https://stackoverflow.com/a/27101414/2240578
def decode(short_code: str) -> str:
    sc_len = len(short_code)
    rv = 0
    for i, c in enumerate(short_code, 1):
        rv += BASE62.find(c) * BASE62_LEN ** (sc_len - i)
    return str(uuid.UUID(int=rv))
