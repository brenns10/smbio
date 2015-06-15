"""Demo for smbio.util.progress stuff."""

from smbio.util.progress import progress, pzip, progress_bar
import time


# Index tells it which index positional argument contains the number of
# iterations.
@progress_bar(index=0)
def fib(n):
    prev = 0
    curr = 1
    for _ in range(n):
        yield curr
        new = prev + curr
        prev = curr
        curr = new


def main():
    for n in fib(20):
        print(n)
        time.sleep(0.05)

    for x in progress(range(10)):
        time.sleep(0.1)

    for x in pzip(range(10), range(20)):
        time.sleep(0.1)


if __name__ == '__main__':
    main()
