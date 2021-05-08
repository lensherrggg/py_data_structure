class UnionSet(object):
    def __init__(self, _size):
        self._size = _size
        # root node's value is negative of the size of root node's tree
        self._us = [-1 for _ in range(_size)]
        self._priority = [0 for _ in range(_size)]

    @property
    def size(self):
        return self._size

    def find(self, x):
        """Find the root of node x"""
        if self._us[x] < 0:
            return x

        # path compression
        self._us[x] = self.find(self._us[x])
        return self._us[x]

    def union(self, x, y):
        """Connect node x and y"""
        x_root = self.find(x)
        y_root = self.find(y)

        # tree with smaller size joins tree with larger size
        if self._us[y_root] < self._us[x_root]:
            self._us[y_root] += self._us[x_root]
            self._us[x_root] = y_root
        else:
            self._us[x_root] += self._us[y_root]
            self._us[y_root] = x_root

    def is_connected(self, x, y):
        """Check if node x and y is connected"""
        return self.find(x) == self.find(y)
