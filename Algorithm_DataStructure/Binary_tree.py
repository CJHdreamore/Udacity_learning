class Node(object):
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree(object):
    def __init__(self,root):
        self.root = Node(root)

    def preorder_search(self,start,find_val):
        if start.value == find_val:
            return True
        elif start.left or start.right:
            return (self.preorder_search(start.left,find_val) or  self.preorder_search(start.right,find_val))
        return False

    def search(self,find_val):
        start = self.root
        return self.preorder_search(start,find_val)


    def preorder_print(self,start,traversal):
        if start:
            traversal.append(start.value)
        if start.left:
            self.preorder_print(start.left,traversal)
        if start.right:
            self.preorder_print(start.right,traversal)
        return traversal


    def print_tree(self):
        '''Print out all tree nodes as they are visited in a
        pre-order traversal'''
        start = self.root
        traversal = []
        self.preorder_print(start,traversal)
        string = ''
        for nodes in traversal:
            string = string + str(nodes) + '-'
        return string[0:-1]







# Set up tree
tree = BinaryTree(1)
tree.root.left = Node(2)
tree.root.right = Node(3)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)

#Test search
#print tree.root
print tree.search(4)
print tree.search(6)

#Test print_tree
#Should be 1-2-4-5-3
print tree.print_tree()




