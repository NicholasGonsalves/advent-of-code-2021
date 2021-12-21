"""Day 12."""
from typing import Dict, Set


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    return [i.split('-') for i in inputs]


class Graph:
    def __init__(self, connections):
        self._graph: Dict[str, Set] = {}
        self.add_connections(connections)

    def __str__(self):
        return f"{self.__class__.__name__}({dict(self._graph)})"

    def add_connections(self, connections):
        """Add connections to graph"""
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """Add connection between node1 and node2"""
        if node1 not in self._graph:
            self._graph[node1] = set()
        if node2 not in self._graph:
            self._graph[node2] = set()
        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    def find_all_paths_small_caves_only_once(self, start='start', end='end', path=None):
        # modified semi-dijkstra
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self._graph:
            return []
        paths = []
        for node in self._graph[start]:
            if (node not in path) or (node.isupper()):
                new_paths = self.find_all_paths_small_caves_only_once(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def get_small_caves(self):
        return [node for node in self._graph.keys() if (node.islower() and (node not in {'start', 'end'}))]

    def find_paths_for_small_caves(self):
        all_paths = []
        for small_cave in self.get_small_caves():
            all_paths += self.find_all_paths_one_small_cave_twice(small_cave=small_cave)
        unique_paths = set()
        for p in all_paths:
            path = tuple(p)
            if path not in unique_paths:
                unique_paths.add(path)
        return unique_paths

    def find_all_paths_one_small_cave_twice(self, start='start', end='end', path=None, small_cave=None):
        # let each small_cave have a turn at allowing two visits
        # modified semi-dijkstra
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self._graph:
            return []
        paths = []
        for node in self._graph[start]:
            if (node not in path) or (node.isupper()) or ((node == small_cave) and (path.count(small_cave) < 2)):
                new_paths = self.find_all_paths_one_small_cave_twice(node, end, path, small_cave)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths


def part_one(paths):
    graph = Graph(paths)
    print(graph)
    return len(graph.find_all_paths_small_caves_only_once())


def part_two(paths):
    graph = Graph(paths)
    return len(graph.find_paths_for_small_caves())


if __name__ == "__main__":
    data = read_file("day12.txt")

    print(part_one(data))
    print(part_two(data))
