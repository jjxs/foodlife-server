import time
import functools


def simple_clock(func):
    print("MethodAnalysis simple_clock: [name: %s],[code: %s], 時間監視中... ..." % (
        func.__name__, func.__code__))

    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%s][実行時間：%0.8fs] %s(%s) -> %r' %
              (func.__code__, elapsed, name, arg_str, result))
        return result
    return clocked


def clock(func):
    print("MethodAnalysis clock: [name: %s],[code: %s], 時間監視中... ..." % (
        func.__name__, func.__code__))

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elspsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))

        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))

        arg_str = ', '.join(arg_lst)
        print('[%s][実行時間：%0.8fs] %s(%s) -> %r' %
              (func.__code__, elspsed, name, arg_str, result))
        return result

    return clocked
