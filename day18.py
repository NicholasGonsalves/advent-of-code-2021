"""Day 18."""
import ast
from typing import Optional
from collections import namedtuple
from itertools import combinations
from copy import deepcopy


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
        return str(self.number)

    def __add__(self, other):
        self.number = [self.number, other.number]
        self.load_tree()
        while self.explode() or self.split():
            self.update_number_from_tree()
            continue
        return self

    def __radd__(self, other):  # required so sum() works with this class
        return self + other

    def load_tree(self) -> None:
        """Load tree from list representation, including parent node pointers."""
        self.root = self.load_node(self.root, self.number)
        self.parent_fix(self.root)

    def load_node(self, root, leaf):
        """Assign specific nodes a place in the tree recursively."""
        if root is None:
            root = Node()

        if isinstance(leaf, int):
            return Node(value=leaf)

        left, right = leaf
        root.l = self.load_node(Node(), left)
        root.r = self.load_node(Node(), right)
        return root

    def parent_fix(self, node):
        """Fix parent pointers in tree, as initial tree construction does not handle them correctly."""
        while node.l is not None and node.l.p is None:
            node.l.p = node
            self.parent_fix(node.l)
        while node.r is not None and node.r.p is None:
            node.r.p = node
            self.parent_fix(node.r)

    def find_exploder(self, root, depth=0):
        """Find first (left-most using dfs) node that meets criteria for exploding (is nested >4 deep)."""
        if root:
            exploder = self.find_exploder(root.l, depth + 1)
            if exploder: return exploder
            if depth == 4:
                if root.l is not None and root.r is not None:
                    return root
            exploder = self.find_exploder(root.r, depth + 1)
            if exploder: return exploder

        return None

    def get_left_number(self, node):
        """Get first node with a non-None value to the 'left' of the passed node."""
        if node.p is None: return None
        if node == node.p.l:
            return self.get_left_number(node.p)
        n = node.p.l
        if n is None: return n
        while n.r is not None:
            n = n.r
        return n

    def get_right_number(self, node):
        """Get first node with a non-None value to the 'right' of the passed node."""
        if node.p is None: return None
        if node == node.p.r:
            return self.get_right_number(node.p)
        n = node.p.r
        if n is None: return n
        while n.l is not None:
            n = n.l
        return n

    def explode(self):
        """Apply explosion to found exploder node."""
        # get node to 'explode'
        exploder = self.find_exploder(self.root)
        if exploder is None: return False

        # add left val of exploding node to first left val node
        next_l = self.get_left_number(exploder.l)
        if next_l is not None:
            next_l.v += exploder.l.v

        # add right val of exploding node to first right val node
        next_r = self.get_right_number(exploder.r)
        if next_r is not None:
            next_r.v += exploder.r.v

        # exploding node val set to 0, and is now leaf
        exploder.l = None
        exploder.r = None
        exploder.v = 0

        return True

    def update_number_from_tree(self):
        """Condense tree (root) into list representation of number and assign to self."""
        self.number = ast.literal_eval(self.get_number_string_from_tree(self.root))

    def get_number_string_from_tree(self, node):
        """Get string representation of the passed tree/node recursively."""
        if node.v is not None:
            return str(node.v)
        return '[' + self.get_number_string_from_tree(node.l) + ',' + self.get_number_string_from_tree(node.r) + ']'

    def find_to_split(self, root):
        """Find first node with a value greater than or equal to 10. DFS."""
        if root:
            split = self.find_to_split(root.l)
            if split: return split
            if (root.v is not None) and (root.v >= 10):
                return root
            split = self.find_to_split(root.r)
            if split: return split
        return None

    def split(self):
        """Split value according to the rules, and assigned respective nodes."""
        to_split = self.find_to_split(self.root)
        if to_split is None: return False

        if to_split.v % 2 == 0:
            l_val = r_val = to_split.v//2
        else:
            l_val = to_split.v // 2
            r_val = to_split.v // 2 + 1

        to_split.l = Node(value=l_val, parent=to_split)
        to_split.r = Node(value=r_val, parent=to_split)
        to_split.v = None

        return True

    def get_magnitude(self):
        """Get magnitude of current self."""
        return self.magnitude(self.root)

    def magnitude(self, root):
        """Get magnitude of passed tree/node representation of the number."""
        if root.v is not None:
            return root.v
        return 3 * self.magnitude(root.l) + 2 * self.magnitude(root.r)


def part_one(homework):
    # Sum all Numbers in homework and return magnitude of result.
    numbers = [Number(number) for number in homework]
    answer = sum(numbers[1:], start=numbers[0])
    magnitude = answer.get_magnitude()
    return magnitude


def update_max_magnitude_with_pair(a, b, max_magnitude):
    """Update and return max_magnitude for the passed pair of numbers (helper for part 2)."""
    answer = a + b
    magnitude = answer.get_magnitude()
    if magnitude > max_magnitude:
        max_magnitude = magnitude
    return max_magnitude


def part_two(homework):
    # Return max magnitude of the sum of any pair of values in the homework
    max_magnitude = 0
    numbers = [Number(number) for number in homework]
    pairs = combinations(numbers, 2)
    for a, b in pairs:
        max_magnitude = update_max_magnitude_with_pair(deepcopy(a), deepcopy(b), max_magnitude)
        max_magnitude = update_max_magnitude_with_pair(deepcopy(b), deepcopy(a), max_magnitude)
    return max_magnitude


if __name__ == "__main__":
    data = read_file("day18.txt")

    print(part_one(data))
    print(part_two(data))
