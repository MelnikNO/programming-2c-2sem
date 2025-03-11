def gen_bin_nec_tree(height: int = 0, root: int = 0, left_leaf = lambda x: x ** 2, right_leaf = lambda x: x - 2) -> dict:
    """Нерекурсивная функция"""

    if height <= 0:
        return {}

    tree = {root: []}
    stack = [(root, height)]

    while stack:
        current_root, current_height = stack.pop()

        if current_height > 1:
            left_value = left_leaf(current_root)
            right_value = right_leaf(current_root)

            if left_value not in tree:
                tree[left_value] = []
            if right_value not in tree:
                tree[right_value] = []

            tree[current_root].append({left_value: []})
            tree[current_root].append({right_value: []})

            stack.append((left_value, current_height - 1))
            stack.append((right_value, current_height - 1))

    return tree

def main():
    print("Нерекурсивное бинарное дерево:")
    print(gen_bin_nec_tree(root=5, height=6))

if __name__ == "__main__":
    main()
