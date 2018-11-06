#!/usr/bin/env python
# -*- coding: utf-8 -*-


def counter():
    n = 1
    while True:
        yield n
        n += 1



class test(object):

    """Docstring for test. """

    def __init__(self):
        """TODO: to be defined1. """

    def foo(self):
        print('foo called: {}'.format(next(counter())))
    
    def bar(self):
        self.barcount = iter(counter())
        print('bar called: {}'.format(next(self.barcount)))
        print('bar called: {}'.format(next(self.barcount)))



if __name__ == "__main__":
    test = test()

    test.foo()
    test.foo()

    test.bar()
    test.bar()
