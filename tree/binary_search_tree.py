class TreeNode(object):
    def __init__(self, _data):
        self.data = _data
        self.left = None
        self.right = None
        self._childCount = 0

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
        return repr(self.data)


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

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def delete(self, data):
        self.root = self._delete(self.root, data)

    def find(self, data):
        return self._find(self.root, data)

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
                    if lower_bound <= node.data <= upper_bound:
                        yield node.data
                elif lower_included:
                    if lower_bound <= node.data < upper_bound:
                        yield node.data
                elif upper_included:
                    if lower_bound < node.data <= upper_bound:
                        yield node.data
                else:
                    if lower_bound < node.data < upper_bound:
                        yield node.data

                if upper_included:
                    if node.data > upper_bound:
                        break
                else:
                    if node.data >= upper_bound:
                        break

    def _insert(self, root, data):
        if root is None:
            root = TreeNode(data)
        elif data < root.data:
            root.left = self._insert(root.left, data)
        elif data > root.data:
            root.right = self._insert(root.right, data)

        root.update_child_count()
        return root

    def _find(self, root, data):
        if root is None:
            return None

        if root.data == data:
            return root
        elif data < root.data:
            return self._find(root.left, data)
        else:
            return self._find(root.right, data)

    def _find_min(self, root):
        if root.left is not None:
            return self._find_min(root.left)
        return root

    def _find_max(self, root):
        if root.right is not None:
            return self._find_max(root.right)
        return root

    def _delete(self, root, data):
        if root is None:
            return None
        if data < root.data:
            root.left = self._delete(root.left, data)
        elif data > root.data:
            root.right = self._delete(root.right, data)
        else:
            if root.left is not None and root.right is not None:
                temp = self._find_min(root.right)
                root.data = temp.data
                root.right = self._delete(root.right, temp.data)
            elif root.right is None and root.left is None:
                root = None
            elif root.right is None:
                root = root.left
            else:
                root = root.right

        if root is not None:
            root.update_child_count()
        return root

    def _less_than(self, data, included=True):
        for node in self:
            if included:
                if node.data > data:
                    break
            else:
                if node.data >= data:
                    break
            yield node.data

    def _greater_than(self, data, included=True):
        for node in self:
            if included:
                if node.data < data:
                    continue
            else:
                if node.data <= data:
                    continue
            yield node.data

    def _traverse(self):
        for node in self:
            yield node.data


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
