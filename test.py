import time
from functools import cache


@cache
def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return (recur_fibo(n - 1) + recur_fibo(n - 2))


def main():
    file = open("filename.txt", 'r')

    for i in file:
        yield i


if __name__ == '__main__':
    a = main()

    next(a)
