# https://blog.csdn.net/z649431508/article/details/78034751
RED = 0
BLACK = 1


class RBNode(object):
    def __init__(self, _data, _color=RED):
        self.data = _data
        self.color = _color
        self.left = None
        self.right = None
        self.parent = None

    def is_black(self):
        return self.color == BLACK

    def set_black(self):
        self.color = BLACK

    def set_red(self):
        self.color = RED

    def __eq__(self, other):
        if isinstance(other, RBNode):
            return self.data == other.data
        return False


class RBTree(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        z = RBNode(data)
        self._insert(z)

    def find(self, data):
        curr = self.root
        while curr is not None:
            if data < curr.data:
                curr = curr.left
            elif data > curr.data:
                curr = curr.right
            else:
                return curr

        return None

    def delete(self, data):
        z = self.find(data)
        if z is None:
            return

    def _insert(self, z):
        x = self.root
        y = None
        while x is not None:
            y = x
            if z.data < x.data:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y is None:
            self.root = z
            self.root.set_black()
            return self.root
        elif z.data < y.data:
            y.left = z
        else:
            y.right = z

        self._insert_fixup(z)
        return z

    def _delete(self, z):
        y = z
        y_origin_color = y.color
        if z.left is None:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._find_minimum(z.right)
            y_origin_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_origin_color == BLACK:
            self._delete_fixup(x)

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._rotate_left(z.parent.parent)

        self.root.set_black()

    def _delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.left
                if w.color == RED:
                    w.set_black()
                    x.parent.set_red()
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.set_red()
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.set_black()
                        w.set_red()
                        self._rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.set_black()
                    w.right.set_black()
                    self._rotate_left(x.parent)
                    x = self.root

            else:
                w = x.parent.left
                if w.color == RED:
                    w.set_black()
                    x.parent.set_red()
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.set_red()
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.set_black()
                        w.set_red()
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.set_black()
                    w.left.set_black()
                    self._rotate_right(x.parent)
                    x = self.root
        x.set_black()

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    @staticmethod
    def _find_minimum(root):
        curr = root
        while curr.left is not None:
            curr = curr.left

        return curr

    def _rotate_left(self, root):
        parent = root.parent
        right = root.right

        root.right = right.left
        if root.right:
            root.right.parent = root

        right.left = root
        root.parent = right

        right.parent = parent
        if parent is None:
            self.root = root
            return

        if parent.left == root:
            parent.left = right
        else:
            parent.right = right

    def _rotate_right(self, root):
        parent = root.parent
        left = root.left

        root.left = left.left
        if root.left:
            root.left.parent = root

        left.left = root
        root.parent = left

        left.parent = parent
        if parent is None:
            self.root = root
            return

        if parent.left == root:
            parent.left = left
        else:
            parent.right = left
