from timeit import timeit


def benchmark():
    code = 's.minimax(1, concurrent=False)'
    n = 100
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')


    code = 's.minimax(1)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 's.minimax(2, concurrent=False)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 's.minimax(2)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 's.minimax(3, concurrent=False)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.5f} ms')

    code = 's.minimax(3)'
    n = 10
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.5f} ms')

    code = 's.minimax(4, concurrent=False)'
    n = 2
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.5f} ms')

    code = 's.minimax(4)'
    n = 2
    t = timeit(code, '''\
from dashwood.state import State
s = State()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.5f} ms')

if __name__ == '__main__':
    benchmark()
