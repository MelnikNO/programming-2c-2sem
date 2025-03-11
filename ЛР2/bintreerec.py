def gen_bin_rec_tree(root = 0, height = 0):
    """Рекурсивная функция"""
    tree = {}

    def bin_tree(r, h):
        if h > 0:
            tree[r] = []
            left_leaf = r ** 2
            right_leaf = r - 2

            tree[r].append(bin_tree(left_leaf, h - 1))
            tree[r].append(bin_tree(right_leaf, h - 1))

        return r

    if height == 0:
        return {root: []}
    bin_tree(root, height)
    return tree

def main():
    print("Рекурсивное бинарное дерево:")
    print(gen_bin_rec_tree(root=5, height=6))

if __name__ == "__main__":
    main()



