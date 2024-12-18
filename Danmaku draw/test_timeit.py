import timeit

input = 'input'
result = ['']


def aaa(input):
    result[0] = input
    return input


def bbb():
    result[0] = input
    return input


def printresult(f):
    print(f"Execution time: {f:.4f} seconds")


if __name__ == '__main__':
    inp = 'inp'

    def ccc(inp):
        result[0] = inp
        return inp

    def ddd():
        result[0] = inp
        return inp

    printresult(timeit.timeit(lambda: aaa(input)))
    printresult(timeit.timeit(lambda: bbb()))
    printresult(timeit.timeit('aaa(input)', globals=globals()))
    printresult(timeit.timeit(
        f"aaa('{input}')", setup="from __main__ import aaa"))
    print(50*'-', result)

    result = ['']
    printresult(timeit.timeit(bbb))
    printresult(timeit.timeit('bbb()', globals=globals()))
    printresult(timeit.timeit('bbb()', setup="from __main__ import bbb"))
    print(50*'-', result)

    result = ['']
    printresult(timeit.timeit("bbb", globals=globals()))
    print(50*'-', result)

    result = ['']
    printresult(timeit.timeit(f"aaa('{inp}')",
                              setup="from __main__ import aaa"))
    print(50*'-', result)
