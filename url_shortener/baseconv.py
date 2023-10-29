from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class BaseConverter:
    """
    Convert integer to any base

    >>> import string
    >>> BaseConverter(string.printable[:36]).encode(0xDEADBEEF)
    '1ps9wxb'
    """

    alphabet: str

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
