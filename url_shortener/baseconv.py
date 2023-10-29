import string
from dataclasses import dataclass
from functools import cached_property

__all__: tuple[str, ...] = ("BaseConverter", "base36", "base58", "base62")


@dataclass
class BaseConverter:
    """
    Convert integer to any base

    >>> import string
    >>> BaseConverter(string.hexdigits[:16]).encode(0xDEADBEEF)
    'deadbeef'
    >>> base36.encode(0xDEADBEEF)
    '1ps9wxb'
    """

    alphabet: str

    # Если alphabet изменится, то alhabet_len тоже поменяется
    @cached_property
    def alphabet_len(self) -> int:
        return len(self.alphabet)

    def encode(self, n: int) -> str:
        rv = ""
        while n > 0:
            rv += self.alphabet[n % self.alphabet_len]
            n //= self.alphabet_len
        return rv[::-1]

    # https://stackoverflow.com/a/27101414/2240578
    def decode(self, s: str) -> int:
        rv = 0
        sl = len(s)
        for i, c in enumerate(s, 1):
            rv += self.alphabet.find(c) * self.alphabet_len ** (sl - i)
        return rv


# for i in (36, 58, 62):
#     globals()[f"base{i}"] = BaseConverter(string.printable[:i])

# Лучше явно указать, тк иначе IDE не видит
base36 = BaseConverter(string.printable[:36])
base58 = BaseConverter(string.printable[:58])
base62 = BaseConverter(string.printable[:62])

if __name__ == "__main__":
    import doctest

    doctest.testmod()
