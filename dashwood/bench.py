from timeit import timeit

from dashwood import state


def benchmark():
    code = 'list(state.children(s))'
    n = 1000
    t = timeit(code, '''\
from dashwood import state
s = state.initial()
    ''', number=n)
    print(f'{code}\t{t*1000*1000/n:.5f} µs')

    code = 'state.is_win(s)'
    n = 1000000
    t = timeit(code, '''\
from dashwood import state
s = state.initial()
    ''', number=1000)
    print(f'{code}\t\t{t*1000*1000/n:.5f} µs')

    code = 'search.minimax(s, 2)'
    n = 3
    t = timeit(code, '''\
from dashwood import state
from dashwood import search
s = state.initial()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.2f} ms')

    code = 'search.montecarlo(s, 1)'
    n = 5
    t = timeit(code, '''\
from dashwood import state
from dashwood import search
s = state.initial()
    ''', number=n)
    print(f'{code}\t{t*1000/n:.2f} ms')


if __name__ == '__main__':
    benchmark()
