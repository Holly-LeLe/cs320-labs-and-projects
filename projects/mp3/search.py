class Node:
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        # TODO: implement recursive size calculation
        pass

    def lookup(self, key):
        # TODO: implement recursive search
        pass


class BST:
    def __init__(self):
        self.root = None

    def add(self, key, val):
        # TODO: implement iterative insert
        pass

    def __dump(self, node):
        # TODO: add recursive traversal
        pass

    def dump(self):
        # TODO: call __dump on the root
        pass

    def __getitem__(self, key):
        # TODO: return values for key
        pass
