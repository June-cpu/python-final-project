class Node:
    def __init__(self, key, data=None):
        self.key = key  
        self.data = data 
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, current, key, data):
        if current is None:
            return Node(key, data)

        if key < current.key:
            current.left = self._insert_recursive(current.left, key, data)
        elif key > current.key:
            current.right = self._insert_recursive(current.right, key, data)
        else:
            current.data = data

        return current

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current, key):
        if current is None or current.key == key:
            return current

        if key < current.key:
            return self._search_recursive(current.left, key)
        else:
            return self._search_recursive(current.right, key)

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, current, result):
        if current:
            self._inorder_recursive(current.left, result)
            result.append((current.key, current.data))
            self._inorder_recursive(current.right, result)
