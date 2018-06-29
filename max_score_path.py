#!/usr/bin/python

import random
from collections import deque

N, M = 3, 4

class Tile:
    def __init__(self):
        self.value = random.randrange(1, 100)
        self.acc_value = 0
        self.previous_tile = (-1, -1)
        self.is_visited = False
        self.final_value = self.value

    def compare_and_update_acc_value(self, acc_value, previous_tile):
        if self.acc_value < acc_value:
            self.acc_value = acc_value
            self.previous_tile = previous_tile
            self.final_value = self.acc_value + self.value

class Board:
    def __init__(self, row, col):
        self.tiles = []
        self.row = row
        self.col = col

        for i in range(0, row):
            self.tiles.append([])
            for j in range(0, col):
                self.tiles[i].append(Tile())

    def show(self):
        for row in self.tiles[::-1]:
            print "\t".join([str(a.value) for a in row])

    def update_tile(self, acc_value, target_tile, previous_tile):
        (r, c) = target_tile
        self.tiles[r][c].compare_and_update_acc_value(acc_value, previous_tile)

    def walk(self):
        bfs_queue = deque([(0, 0)])

        while len(bfs_queue) > 0:
            tile_pos = bfs_queue.popleft()
            (r, c) = tile_pos

            if self.tiles[r][c].is_visited:
                continue

            self.tiles[r][c].is_visited = True

            if r < self.row - 1:
                next_pos = (r+1, c)
                bfs_queue.append(next_pos)
                self.update_tile(self.tiles[r][c].final_value, next_pos, tile_pos)

            if c < self.col - 1:
                next_pos = (r, c+1)
                bfs_queue.append(next_pos)
                self.update_tile(self.tiles[r][c].final_value, next_pos, tile_pos)

    def max_path_value(self):
        return self.tiles[self.row-1][self.col-1].final_value

    def max_path(self):
        tile_pos = (self.row-1, self.col-1)
        trace = []

        for i in range(0, self.row + self.col -1):
            (r, c) = tile_pos
            if r >= 0 and c >= 0:
                trace.append(tile_pos)
                tile_pos = self.tiles[r][c].previous_tile
            else:
                break

        trace.reverse()
        return " -> ".join(["(%d, %d) / %d" % (c, r, self.tiles[r][c].value) for (r, c) in trace])

board = Board(N, M)
board.show()
board.walk()
print "max path value:", board.max_path_value()
print "max path:", board.max_path()

