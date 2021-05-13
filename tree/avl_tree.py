import copy


class AVLTreeNode(object):
    def __init__(self, _data):
        self.data = _data
        # height of left child tree minus height of right child tree
        self.height = 1
        self.left = None
        self.right = None


class AVLTree(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def find(self, data):
        return self._find(self.root, data)

    def delete(self, data):
        self.root = self._delete(self.root, data)

    def _insert(self, root, data):
        if root is None:
            return AVLTreeNode(data)

        if root.data < data:
            root.right = self._insert(root.right, data)
        elif root.data > data:
            root.left = self._insert(root.left, data)

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        return self._adjust_balance(root)

    def _find(self, root, data):
        if root is None:
            return None

        if data < root.data:
            return self._find(root.left, data)
        elif data > root.data:
            return self._find(root.right, data)
        else:
            return root

    def _delete(self, root, data):
        if root is None:
            return None

        ret = None
        if data < root.data:
            root.left = self._delete(root.left, data)
            ret = root
        elif data > root.data:
            root.right = self._delete(root.right, data)
            ret = root
        else:
            if root.left is None:
                tmp = root.right
                root.right = None
                ret = tmp
            elif root.right is None:
                tmp = root.left
                root.left = None
                ret = tmp
            else:
                successor = self._find_minimum(root.right)
                successor.right = self._delete(root.right, successor.data)
                successor.left = root.left
                root.left = None
                root.right = None

                ret = successor

        if ret is None:
            return None

        return self._adjust_balance(ret)

    def _is_balanced(self, root):
        if root is None:
            return True
        if abs(self._get_balance_factor(root)) > 1:
            return False
        return self._is_balanced(root.left) and self._is_balanced(root.right)

    def _rotate_right(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        new_root.height = max(self._get_height(new_root.left), self._get_height(new_root.right)) + 1

        return new_root

    def _rotate_left(self, root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        new_root.height = max(self._get_height(new_root.left), self._get_height(new_root.right)) + 1

        return new_root

    def _adjust_balance(self, root):
        root_balance = self._get_balance_factor(root)

        if root_balance > 1 and self._get_balance_factor(root.left) >= 0:
            # inserted node is at the left child of left child of unbalanced node
            # LL
            return self._rotate_right(root)

        if root_balance < -1 and self._get_balance_factor(root.right) <= 0:
            # inserted node is at the right child of right child of unbalanced node
            # RR
            return self._rotate_left(root)

        if root_balance > 1 and self._get_balance_factor(root.left) < 0:
            # LR
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if root_balance < -1 and self._get_balance_factor(root.right) > 0:
            # RL
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    @staticmethod
    def _get_height(root):
        if root is None:
            return 0
        return root.height

    def _get_balance_factor(self, root):
        if root is None:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)

    def _find_minimum(self, root):
        if root.left is None:
            return root
        return self._find_minimum(root.left)

