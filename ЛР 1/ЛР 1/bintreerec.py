def gen_bin_rec_tree(root = 0, height = 0):
    """Рекурсивная функция"""

    tree = {}

    if height > 0:
        tree[root] = []
        left_leaf = root ** 2
        right_leaf = root - 2

        tree[root].append(gen_bin_rec_tree(left_leaf, height - 1))
        tree[root].append(gen_bin_rec_tree(right_leaf, height - 1))
    return tree

def main():
    print("Рекурсивное бинарное дерево:")
    print(gen_bin_rec_tree(root=5, height=6))

if __name__ == "__main__":
    main()



