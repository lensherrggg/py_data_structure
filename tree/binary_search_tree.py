class TreeNode(object):
    def __init__(self, _key):
        self._key = _key
        self.left = None
        self.right = None
        self._childCount = 0

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, _key):
        self._key = _key

    @property
    def size(self):
        return self._childCount + 1

    def update_child_count(self):
        if self.left is None and self.right is None:
            self._childCount = 0
        elif self.left is None:
            self._childCount = self.right.size
        elif self.right is None:
            self._childCount = self.left.size
        else:
            self._childCount = self.left.size + self.right.size

    def __repr__(self):
        return repr(self._key)


# BST search
class BinarySearchTree(object):
    def __init__(self):
        self.root = None
        self._iterator = None

    def __iter__(self):
        self._iterator = BSTIterator(self)
        return self._iterator

    def __next__(self):
        return self._iterator.__next__()

    @property
    def size(self):
        if self.root is None:
            return 0
        return self.root.size

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def find(self, key):
        return self._find(self.root, key)

    def find_min(self):
        return self._find_min(self.root)

    def find_max(self):
        return self._find_max(self.root)

    def range(self, lower_bound=None, upper_bound=None, lower_included=True, upper_included=True):
        if lower_bound is None and upper_bound is None:
            yield from self._traverse()
        elif lower_bound is None:
            yield from self._less_than(upper_bound, included=upper_included)
        elif upper_bound is None:
            yield from self._greater_than(lower_bound, included=lower_included)
        else:
            for node in self:
                if lower_included and upper_included:
                    if lower_bound <= node.key <= upper_bound:
                        yield node.key
                elif lower_included:
                    if lower_bound <= node.key < upper_bound:
                        yield node.key
                elif upper_included:
                    if lower_bound < node.key <= upper_bound:
                        yield node.key
                else:
                    if lower_bound < node.key < upper_bound:
                        yield node.key

                if upper_included:
                    if node.key > upper_bound:
                        break
                else:
                    if node.key >= upper_bound:
                        break

    def _insert(self, root, key):
        if root is None:
            root = TreeNode(key)
        elif key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)

        root.update_child_count()
        return root

    def _find(self, root, key):
        if root is None:
            return None

        if root.key == key:
            return root
        elif key < root.key:
            return self._find(root.left, key)
        else:
            return self._find(root.right, key)

    def _find_min(self, root):
        if root.left is not None:
            return self._find_min(root.left)
        return root

    def _find_max(self, root):
        if root.right is not None:
            return self._find_max(root.right)
        return root

    def _delete(self, root, key):
        if root is None:
            return None
        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if root.left is not None and root.right is not None:
                temp = self._find_min(root.right)
                root.key = temp.key
                root.right = self._delete(root.right, temp.key)
            elif root.right is None and root.left is None:
                root = None
            elif root.right is None:
                root = root.left
            else:
                root = root.right

        if root is not None:
            root.update_child_count()
        return root

    def _less_than(self, key, included=True):
        for node in self:
            if included:
                if node.key > key:
                    break
            else:
                if node.key >= key:
                    break
            yield node.key

    def _greater_than(self, key, included=True):
        for node in self:
            if included:
                if node.key < key:
                    continue
            else:
                if node.key <= key:
                    continue
            yield node.key

    def _traverse(self):
        for node in self:
            yield node.key


class BSTIterator(object):
    def __init__(self, _bst):
        self._curr = _bst.root
        self._stk = []

    def __next__(self):
        while self._curr is not None:
            self._stk.append(self._curr)
            self._curr = self._curr.left

        if len(self._stk) == 0:
            raise StopIteration

        ret = self._stk.pop()
        self._curr = ret.right
        return ret
