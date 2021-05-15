import random

from tree import RBTree
from .helper import is_bst_for_rbtree


def test_rb_tree():
    tree = RBTree()
    data_list = [random.randint(0, 10000) for _ in range(10)]
    for elem in data_list:
        tree.insert(elem)
        assert is_bst_for_rbtree(tree)

    for elem in data_list:
        tree.delete(elem)
        assert is_bst_for_rbtree(tree)
        assert tree.find(elem) is None
