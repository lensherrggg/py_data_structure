from tree import AVLTree
import random

from .helper import is_bst, is_balanced


def test_avl_tree():
    tree = AVLTree()

    data_list = [random.randint(0, 10000) for _ in range(1000)]
    for elem in data_list:
        tree.insert(elem)

    assert is_bst(tree)
    assert is_balanced(tree)

    for elem in data_list:
        assert tree.find(elem).data == elem

    for elem in data_list:
        tree.delete(elem)
        assert is_bst(tree)
        assert is_balanced(tree)
        assert tree.find(elem) is None
