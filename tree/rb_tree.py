# https://blog.csdn.net/z649431508/article/details/78034751
# https://www.cnblogs.com/skywang12345/p/3245399.html
# https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/
RED = 0
BLACK = 1


class RBNode(object):
    def __init__(self, data, color=RED):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def is_black(self):
        return self.color == BLACK

    def set_black(self):
        self.color = BLACK

    def set_red(self):
        self.color = RED


class RBTree(object):
    def __init__(self):
        self.NIL = RBNode(None, color=BLACK)
        self.root = self.NIL

    def insert(self, data):
        z = RBNode(data)
        z.left = self.NIL
        z.right = self.NIL
        self._insert(z)

    def find(self, data):
        curr = self.root
        while curr != self.NIL:
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
        self._delete(z)

    def _insert(self, z):
        x = self.root
        y = None
        while x != self.NIL:
            y = x
            if z.data < x.data:
                x = x.left
            elif z.data > x.data:
                x = x.right
            else:
                return

        z.parent = y

        if y is None:
            self.root = z
            self.root.set_black()
        elif z.data < y.data:
            y.left = z
        else:
            y.right = z

        if z.parent is None:
            z.set_black()
            return

        if z.parent.parent is None:
            return

        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while self._is_red(z.parent):
            if z.parent == z.parent.parent.left:
                # case 1: z's parent is z's grand parent's left child
                # z's uncle node
                y = z.parent.parent.right
                if self._is_red(y):
                    # case 1-1: uncle node is red
                    z.parent.set_black()
                    y.set_black()
                    # set grand parent to red
                    z.parent.parent.set_red()
                    # make grand parent the current node
                    z = z.parent.parent
                else:
                    # case 1-2: uncle node is black
                    if z == z.parent.right:
                        # case 1-2: current node is its parent's right child
                        # make parent the current node
                        z = z.parent
                        self._rotate_left(z)
                    # case 1-3: uncle node is black and current node is left child
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._rotate_right(z.parent.parent)
            else:
                # case 2: z's parent is z's grand parent's right child
                # same as above, exchange right and left
                y = z.parent.parent.left
                if self._is_red(y):
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

    def _delete(self, z):
        y = z
        y_origin_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
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

    def _delete_fixup(self, x):
        while x != self.root and self._is_black(x):
            if x == x.parent.left:
                w = x.parent.right
                if self._is_red(w):
                    # case 1: x is black + black node, x's brother is red
                    w.set_black()
                    x.parent.set_red()
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if self._is_black(w.left) and self._is_black(w.right):
                    # case 2: x is black + black node, x's brother is black
                    # both of x's brother's children are black
                    w.set_red()
                    x = x.parent
                else:
                    if self._is_black(w.right):
                        # case 3: x is black + black node, x's brother is black
                        # x's brother's left child is red and right child is black
                        w.left.set_black()
                        w.set_red()
                        self._rotate_right(w)
                        w = x.parent.right
                    # case 4: x is black + black node, x's brother is black
                    # x's brother's right child is red
                    w.color = x.parent.color
                    x.parent.set_black()
                    w.right.set_black()
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if self._is_red(w):
                    w.set_black()
                    x.parent.set_red()
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if self._is_black(w.left) and self._is_black(w.right):
                    w.set_red()
                    x = x.parent
                else:
                    if self._is_black(w.left):
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

    def _find_minimum(self, root):
        curr = root
        while curr.left != self.NIL:
            curr = curr.left

        return curr

    def _successor(self, x):
        # if right subtree is not None
        # successor is the leftmost node in right subtree
        if x.right != self.NIL:
            return self._find_minimum(x.right)

        # else it is the lowest ancestor of x whose left child
        # is also an ancestor of x
        y = x.parent
        while y != self.NIL and x == y.right:
            x = y
            y = y.parent
        return y

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    @staticmethod
    def _is_black(node):
        if node is None:
            return True
        return node.color == BLACK

    @staticmethod
    def _is_red(node):
        if node is None:
            return False
        return node.color == RED

    @staticmethod
    def is_nil(node):
        return node.left is None and node.right is None
