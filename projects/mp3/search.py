class Node:
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        # TODO: implement recursive size calculation
    
        size = len(self.values)
        if self.left != None:
            size += len(self.left)
        if self.right != None:
            size += len(self.right)
        return size

    def lookup(self, key):
        # TODO: implement recursive search
        if key == self.key:
            return self.values
        elif key < self.key:
            if self.left is None:
                return []
            return self.left.lookup(key)
        else:
            if self.right is None:
                return []
            return self.right.lookup(key)


class BST:
    def __init__(self):
        self.root = None

    def add(self, key, val):
        # TODO: implement iterative insert
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                if curr.right is None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                break

        curr.values.append(val)

    def __dump(self, node):
        # TODO: add recursive traversal
        if node == None:
            return
        self.__dump(node.right)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.left)             # 3


    def dump(self):
        # TODO: call __dump on the root
        self.__dump(self.root)

    def __getitem__(self, key):
        # TODO: return values for key
        if self.root is None:
            return []
        return self.root.lookup(key)