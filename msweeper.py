#!/usr/bin/env python

from __future__ import print_function
import random
import sys

class Cell:
    def __init__(self):
        self._flagged = False
        self._bomb = False
        self._visited = False
        self._fatal = False # only true if this is a bomb we landed on
        self._count = 0 # never exceeds 8

    def __str__(self):
        if not self._visited:
            if self._flagged:
                return '@'
            return '.'

        if self._fatal:
            return 'X'

        if self._bomb:
            return '*'

        if self._count > 0:
            return str(self._count)

        return ' '

class Board:
    def __init__(self, rows, columns, bombs):
        self.rows = rows
        self.columns = columns
        self.grid = [[Cell() for _ in xrange(columns)] for _ in xrange(rows)]

        ints = [x for x in xrange(rows * columns)]
        random.shuffle(ints)
        for i in xrange(bombs):
            self.grid[ints[i] // columns][ints[i] % columns]._bomb = True

    def printgrid(self):
        print("     ", end="")
        for c in xrange(self.columns):
            print("{0:4d}".format(c), end="")
        print()
        for r in xrange(self.rows):
            print("     ", end="")
            for c in xrange(self.columns):
                print('+---', end='')
            print('+')
            print("{0:4d} ".format(r), end="")
            for c in xrange(self.columns):
                print("| ", self.grid[r][c], " ", end="", sep="")
            print('|', end="")
            print("{0:4d} ".format(r), end="")
            print()
        print("     ", end="")
        for c in xrange(self.columns):
            print('+---', end='')
        print('+')
        print("     ", end="")
        for c in xrange(self.columns):
            print("{0:4d}".format(c), end="")
        print()

    def _neighbors(self, r, c):
        """
        generate all neighbors
        """

        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                if i == 0 and j == 0:
                    continue

                rr = r + i
                cc = c + j
                
                if 0 <= rr < self.rows and 0 <= cc < self.columns:
                    yield [rr, cc]

    def _adjacent_bombs(self, r, c):
        count = 0
        for n in self._neighbors(r, c):
            if self.grid[n[0]][n[1]]._bomb:
                count += 1

        return count

    def _visit(self, r, c):
        if self.grid[r][c]._visited == True:
            return

        self.grid[r][c]._visited = True

        self.grid[r][c]._count = self._adjacent_bombs(r, c)
        if self.grid[r][c]._count > 0:
            return

        for n in self._neighbors(r, c):
            self._visit(n[0], n[1])

    def visit(self, r, c):
        # cell is either a bomb, adjacent to a bomb, or vacant.
        # if we are adjacent, do not visit neighbors.

        if self.grid[r][c]._bomb == True:
            self.grid[r][c]._fatal = True

            # visit all nodes, print grid
            for i in xrange(self.rows):
                for j in xrange(self.columns):
                    self.grid[i][j]._visited = True

            print("KABOOM")
            self.printgrid()
            sys.exit(0)

        self._visit(r, c)

b = Board(20, 20, 30)
b.printgrid()

while True:
    setflag = False
    x = raw_input("[f] r c, q ==> ")
    a = x.split()
    if len(a) < 1:
        continue

    if a[0] == 'q':
        print('done')
        sys.exit(0)

    if a[0] == 'f':
        setflag = True
        r = int(a[1])
        c = int(a[2])
    else:
        # assume r and c
        r = int(a[0])
        c = int(a[1])

    if not (0 <= r < b.rows) or not (0 <= c < b.columns):
        print("out of range")
        continue

    if setflag:
        b.grid[r][c]._flagged = True
    else:
        b.visit(r, c)

    b.printgrid()
