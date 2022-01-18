class TreeNode:
    def __init__(self, key, val, left = None, right = None, parent = None):
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent
        self.counter = 1

    def has_left_child(self):
        return self.left_child

    def has_right_child(self):
        return self.right_child

    def is_left_child(self):
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        return self.parent and self.parent.right_child == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.right_child or self.left_child)

    def has_any_children(self):
        return self.right_child or self.left_child

    def has_both_children(self):
        return self.right_child and self.left_child

    def replace_node_data(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

    def splice_out(self):
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                    self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                     succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
        return succ

    def find_min(self):
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def print_BST(self):

        result = ''

        def show(result, current_node):
            if current_node:
                if current_node.key:
                    result += ('key: ' + str(current_node.key) + ' value: ' + str(current_node.payload) + ' counter: ' + str(current_node.counter) +'\n')
                    result = show(result, current_node.left_child)
                    result = show(result, current_node.right_child)
                else:
                    pass
            else:
                pass
            return result
        print(show(result, self.root)+'\n')

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()
    
    def put(self, key, val):
        if self.get(key):
            if self._get(key, self.root).payload == val:
                self._get(key, self.root).counter += 1
            else:
                self._get(key, self.root).payload = val
                self._get(key, self.root).counter += 1 
        elif self.root:
            self._put(key, val, self.root) 
            self.size += 1
        else:
            self.root = TreeNode(key, val)
            self.size += 1
    
    def _put(self, key, val, current_node):
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, val,current_node.left_child)
            else:
                current_node.left_child = TreeNode(key, val, parent = current_node)
        else:
            if current_node.has_right_child():
                self._put(key, val,current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, val, parent = current_node)

    def __setitem__(self, k, v): 
        self.put(k, v) 

    def get(self, key):
        if self.root:
            result = self._get(key, self.root)
            if result:
                return result.payload
            else:
                return None
        else:
            return None

    def _get(self, key, current_node):
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left_child)
        else:
            return self._get(key, current_node.right_child)

    def __getitem__(self, key): 
        return self.get(key)        

    def __contains__(self, key):  
        if self._get(key, self.root):
            return True
        else:
            return False
        
    def delete(self, key):        
        node_to_remove = self._get(key, self.root)
        if node_to_remove:
            if node_to_remove.counter == 1:
                if self.size > 1:
                    self.remove(node_to_remove)
                    self.size -= 1
                elif self.size == 1 and self.root.key == key:
                    self.root = None
                    self.size -= 1
                else:
                    raise KeyError('Error, key "' + str(key) + '" not in tree')
            else:
                self._get(key,self.root).counter -= 1
        else:
            raise KeyError('Error, key "' + str(key) + '" not in tree')

    def __delitem__(self, key): 
        self.delete(key)

    def remove(self, current_node):
        if current_node.is_leaf(): 
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children(): 
            succ = current_node.find_successor()
            succ.splice_out()
            current_node.key = succ.key
            current_node.payload = succ.payload
        else: 
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.left_child
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                else:
                    current_node.replace_node_data(current_node.left_child.key,
                                    current_node.left_child.payload,
                                    current_node.left_child.left_child,
                                    current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                elif current_node.is_right_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                else:
                    current_node.replace_node_data(current_node.right_child.key,
                                    current_node.right_child.payload,
                                    current_node.right_child.left_child,
                                    current_node.right_child.right_child)

    def display_tree(self):
        def printTree(current_node, level = 0):
            if current_node != None:
                printTree(current_node.left_child, level + 1)
                print(' ' * 5 * level + '-->', current_node.key)
                printTree(current_node.right_child, level + 1)
            else:
                pass

        return(printTree(self.root))