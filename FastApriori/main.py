class TrieNode():
    def __init__(self):
        self.children = dict()
        self.terminate = False
        self.support = 0
        self.depth = None
        self.label = None

class ConstructTrie():
    def __init__(self):
        self.root = self.get_node()
    
    def get_node(self):
        return TrieNode()
    

    def insert(self, parent_node, transaction, index):
        print(parent_node.label, index)
        if index >= len(transaction):
            return
        #print(transaction[index], parent_node.children)
        if transaction[index] in parent_node.children:
            child_node = parent_node.children[transaction[index]]
            #print(child_node)
            child_node.support += 1
            child_node.terminate = False
            self.insert(child_node, transaction, index + 1)
        else:
            new_node = TrieNode()
            parent_node.children[transaction[index]] = new_node
            new_node.label = transaction[index]
            new_node.support = 1
            new_node.terminate = False
            self.insert(new_node, transaction, index+1)
    
    def print_trie(self):
        for items in self.root.children:
            print(items)
            
        
            

if __name__=="__main__":
    t = ConstructTrie()
    node = TrieNode()
    t.insert(node, "hello", 0)
    t.insert(node, "bello", 0)
    
    print(node.children['h'])