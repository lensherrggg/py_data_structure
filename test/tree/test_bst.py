from tree import BinarySearchTree
import random

from .helper import is_bst


def test_bst():
    tree = BinarySearchTree()
    data_list = [random.randint(0, 10000) for _ in range(1000)]
    for elem in data_list:
        tree.insert(elem)

    for elem in data_list:
        assert tree.find(elem).data == elem

    assert is_bst(tree)
    for elem in data_list:
        tree.delete(elem)
        assert is_bst(tree)
