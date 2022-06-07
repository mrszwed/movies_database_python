from math import ceil

import numpy as np


class BatchGenerator():
    def __init__(self, ids, batch_size=100, start_from=0):
        self.ids = ids
        self.batch_size = batch_size
        self.start_from = start_from
        self.cursor = start_from

    def __iter__(self):
        start = self.cursor
        # for i in range(len(self.ids)//self.batch_size+1):
        for i in range(ceil((len(self.ids) - self.cursor) / self.batch_size)):
            end = self.cursor + self.batch_size
            if end >= len(self.ids):
                end = len(self.ids)
            yield self.ids[self.cursor:end]
            self.cursor += self.batch_size

    def get_cursor(self):
        return self.cursor

    def ids_size(self):
        return len(self.ids)

    def get_batch_number(self):
        return self.cursor // self.batch_size

    def get_number_of_batches(self):
        return ceil(len(self.ids) / self.batch_size)


def batch_generator_test():
    tab = np.arange(1000)
    bg = BatchGenerator(tab, 17)
    for t in bg:
        print(t)


if __name__ == "__main__":
    batch_generator_test()
