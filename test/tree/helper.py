def is_bst(tree):
    def dfs(tree_root, data_vessel):
        if tree_root is None:
            return
        dfs(tree_root.left, data_vessel)
        data_vessel.append(tree_root.data)
        dfs(tree_root.right, data_vessel)

    root = tree.root
    data_list = []
    dfs(root, data_list)
    for i in range(1, len(data_list)):
        if data_list[i] < data_list[i - 1]:
            return False

    return True


def is_balanced(tree):
    def get_balance_factor(root):
        if root is None:
            return 0
        return get_balance_factor(root.left) - get_balance_factor(root.right)

    def helper(root):
        if root is None:
            return True
        if abs(get_balance_factor(root)) > 1:
            return False

        return helper(root.left) and helper(root.right)

    return helper(tree.root)
