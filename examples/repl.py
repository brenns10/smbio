"""Example for the repl."""

from smbio.util.repl import repl


def main():
    a = 1
    b = 2
    stuff = list(range(10))

    # "stuff" is modifiable (but not reassignable), since it's an object.  "a"
    # and "b" can't be modified, but can be accessed still
    repl()

    print(a)
    print(b)
    print(stuff)


if __name__ == '__main__':
    main()
