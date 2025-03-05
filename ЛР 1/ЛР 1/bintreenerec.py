def gen_bin_nec_tree(height: int, root: int, left_leaf = lambda x: x ** 2, right_leaf = lambda x: x - 2) -> dict:
    """Нерекурсивная функция"""

    if height <= 0:
        return {}

    tree = {str(root): []}
    stack = [(root, height)]

    while stack:
        current_root, current_height = stack.pop()

        if current_height > 1:
            left_value = left_leaf(current_root)
            right_value = right_leaf(current_root)

            if str(left_value) not in tree:
                tree[str(left_value)] = []
            if str(right_value) not in tree:
                tree[str(right_value)] = []

            tree[str(current_root)].append({str(left_value): []})
            tree[str(current_root)].append({str(right_value): []})

            stack.append((left_value, current_height - 1))
            stack.append((right_value, current_height - 1))

    return tree

def main():
    print("Нерекурсивное бинарное дерево:")
    print(gen_bin_nec_tree(root=5, height=6))

if __name__ == "__main__":
    main()
