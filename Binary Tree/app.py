from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# Define other routes for the binary tree API here

if __name__ == "__main__":
    app.run(debug=True)

# Node definition for the binary tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Binary Tree class
class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self.insert(root.left, key)
            else:
                root.right = self.insert(root.right, key)
        return root

    def search(self, root, key):
        if root is None or root.val == key:
            return root is not None
        if key < root.val:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def delete_node(self, root, key):
        if root is None:
            return root
        if key < root.val:
            root.left = self.delete_node(root.left, key)
        elif key > root.val:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            min_val = self.find_min(root.right)
            root.val = min_val
            root.right = self.delete_node(root.right, min_val)
        return root

    def find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.val

# Create a binary tree instance
tree = BinaryTree()
tree.root = tree.insert(tree.root, 50)
tree.root = tree.insert(tree.root, 30)
tree.root = tree.insert(tree.root, 70)
tree.root = tree.insert(tree.root, 20)
tree.root = tree.insert(tree.root, 40)
tree.root = tree.insert(tree.root, 60)
tree.root = tree.insert(tree.root, 80)

@app.route('/search', methods=['GET'])
def search():
    key = int(request.args.get('key'))
    found = tree.search(tree.root, key)
    return jsonify({"key": key, "found": found})

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    key = data.get('key')
    tree.root = tree.delete_node(tree.root, key)
    return jsonify({"message": f"Node with key {key} deleted, if it existed."})

if __name__ == "__main__":
    app.run(debug=True)
