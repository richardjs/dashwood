from timeit import timeit


def benchmark():
    code = 's.minimax(1)'
    n = 1000
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 's.minimax(2)'
    n = 100
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 's.minimax(3)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.5f} ms')


if __name__ == '__main__':
    benchmark()
