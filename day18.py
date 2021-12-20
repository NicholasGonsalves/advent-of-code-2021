"""Day 18."""
import ast
from typing import Optional
from collections import namedtuple


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.readlines()
    inputs = [i.strip("\n") for i in inputs]
    return inputs


class Node:
    def __init__(self, value=None, parent=None):
        self.p = parent
        self.l = None
        self.r = None
        self.v = value


Step = namedtuple("Step", "depth value")


class Number:
    def __init__(self, number):
        self.number = ast.literal_eval(number)
        self.root: Optional[Node] = None
        self.load_tree()

    def __str__(self):
        self.print_tree(self.root)
        return str(self.number)

    def __add__(self, other):
        self.number = [self.number, other]
        self.load_tree()
        self.find_exploder()
        # explode, reduce, etc, etc
        ...

    def print_tree(self, node, level=0):
        if node is not None:
            self.print_tree(node.l, level + 1)
            if node.v is not None:
                print(' ' * 2 * level + '->', node.v)
            else:
                print(' ' * 2 * level + '->')
            self.print_tree(node.r, level + 1)

    def load_tree(self) -> None:
        self.root = self.load_node(self.root, self.number)
        self.parent_fix(self.root)

    def load_node(self, root, leaf):
        if root is None:
            root = Node()

        if isinstance(leaf, int):
            return Node(value=leaf)

        # if isinstance(leaf, list):
        left, right = leaf
        root.l = self.load_node(Node(), left)
        root.r = self.load_node(Node(), right)
        return root

    # Fixes parent pointers for already defined tree
    def parent_fix(self, node):
        while node.l is not None and node.l.p is None:
            node.l.p = node
            self.parent_fix(node.l)
        while node.r is not None and node.r.p is None:
            node.r.p = node
            self.parent_fix(node.r)

    def find_exploder(self, root, depth=0):
        # find leftmost pair nested 4 deep
        if root:
            # First recur on left child
            exploder = self.find_exploder(root.l, depth + 1)
            if exploder: return exploder
            if depth == 4:
                if root.l is not None and root.r is not None:
                    return root
            exploder = self.find_exploder(root.r, depth + 1)
            if exploder: return exploder

        return None

    def get_left_number(self, node):
        if node.p is None: return None
        if node == node.p.l:
            return self.get_left_number(node.p)
        n = node.p.l
        if n is None: return n
        while n.r is not None:
            n = n.r
        return n

    def get_right_number(self, node):
        if node.p is None: return None
        if node == node.p.r:
            return self.get_right_number(node.p)
        n = node.p.r
        if n is None: return n
        while n.l is not None:
            n = n.l
        return n

    def explode(self):
        exploder = self.find_exploder(self.root)
        if exploder is None: return False

        next_l = self.get_left_number(exploder.l)
        if next_l is not None:
            next_l.v += exploder.l.v

        next_r = self.get_right_number(exploder.r)
        if next_r is not None:
            next_r.v += exploder.r.v

        exploder.l = None
        exploder.r = None
        exploder.v = 0

        return True

    def update_number_from_tree(self):
        self.number = ast.literal_eval(self.get_number_string_from_tree(self.root))

    def get_number_string_from_tree(self, node):
        if node.v is not None:
            return str(node.v)
        return '[' + self.get_number_string_from_tree(node.l) + ',' + self.get_number_string_from_tree(node.r) + ']'


def part_one(homework):
    number = Number(homework[0])
    number.explode()
    number.update_number_from_tree()
    print(number)


def part_two(homework):
    ...


if __name__ == "__main__":
    data = read_file("day18.txt")

    print(part_one(data))
    print(part_two(data))
