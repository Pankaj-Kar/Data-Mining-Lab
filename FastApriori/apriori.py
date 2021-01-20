import copy
import time
class TrieNode():
    def __init__(self):
        self.item = None
        self.support = 0
        self.children = dict()
        self.visited = False
        self.depth = None


class AprioriAlgorithm():
    items = list()
    main_database = []
    temp_pattern = []
    threshold = 0.0
    total_number_of_frequent_patterns = 0
    total_number_of_candidates = 0
    candidates = []
    level = 0
    number_of_patterns = 0
    candidate_count = 0
    joining_count = 0
    
    def mine_patterns(self, threshold, db):
        self.main_database = db
        self.threshold = threshold*len(self.main_database)
        #self.threshold = 20.0
        print(f'Threshold Support: {self.threshold}')
        L1 = self.generate_f1_itemset()
        #print(L1)
        C2 = self.generate_c2_itemset(L1)
        #print(C2)
        self.total_number_of_frequent_patterns+=len(L1)
        print(f'Frequent Pattern After L1 = {self.total_number_of_frequent_patterns}')
        self.total_number_of_candidates = self.total_number_of_candidates + len(L1) + len(C2)
        self.candidates = C2
        self.level = 2
        self.root = TrieNode()
        #print('1')
        for itemsets in self.candidates:
            self.generate_trie(self.root, itemsets, 0)
        #print('2')
        while True:
            for sequence in self.main_database:
                self.support_counter(self.root, sequence)
            self.number_of_patterns = 0
            #print('before')
            #self.check_trie(self.root, [])
            self.generate_frequent_itemsets(self.root, 0)
            #print('after')
            
            
            total_patterns = self.number_of_patterns
            #print(total_patterns, self.level)
            self.total_number_of_frequent_patterns += total_patterns
            print(f'Frequent Pattern After L{self.level} = {self.total_number_of_frequent_patterns}')
            if self.number_of_patterns < self.level:
                break
            #print(self.root.children)
            self.candidate_count = 0
            self.joining_count = 0
            self.join_items(self.root, [], 0)
            #self.check_trie(self.root, [])
            #self.after_join_deletion(self.root, 0)
            #print('after join')
            #self.check_trie(self.root, [])
            #print(self.candidate_count, 'cs')
            self.level+=1
            self.total_number_of_candidates+=self.candidate_count
            #print(self.total_number_of_candidates, 'cd')
        #self.check_trie(self.root, [])
        return

    def check_trie(self, node, items):
        if node.item is not None:
            items.append(node.item)
        print(items)
        for child in node.children:
            self.check_trie(node.children[child], copy.deepcopy(items))

    def join_items(self, node, arr, depth):
        #print(node.children)
        node.visited = False
        if node.item is not None:
            arr.append(node.item)
            #print(arr, 'arr')
        #print(depth, self.level, node.children)
        if depth == self.level-1:
            #print(node.children)
            itemset = list(node.children.keys())
            itemset.sort()
            #print(itemset)
            for i in range(0, len(itemset)):
                for j in range(i+1, len(itemset)):
                    self.joining_count += 1
                    self.temp_pattern = arr + [itemset[i] , itemset[j]]
                    #print(self.temp_pattern)
                    frequent = self.in_generation_prune()
                    #print(frequent)
                    if frequent:
                        #print('Result: ',  self.temp_pattern)
                        self.candidate_count+=1
                        self.add_child(node.children[itemset[i]], itemset[j])
            
            return
        for child in node.children:
            temp_arr = copy.deepcopy(arr)
            #print(temp_arr)
            self.join_items(node.children[child], temp_arr, depth+1)
    
    def after_join_deletion(self, node, level):
        #print(node.visited)
        if node.visited == True:
            print(node.item, node.visited)
        temp_children = copy.deepcopy(node.children)
        #print(temp_children)
        node.children = dict()
        if (node.item is not None) and (level == self.level+1):
            self.number_of_patterns += 1
            node.visited == True
        child_no = 0
        node.support = 0
        for child in temp_children:
            val = self.after_join_deletion(temp_children[child], level+1)
            #print(val)
            if val > 0 :
                child_no += val
                node.children[child] = temp_children[child]
        return child_no + node.visited
        

    def add_child(self, node, item):
        node.visited = False
        new_child = TrieNode()
        new_child.item = item
        node.children[item] = new_child
        #print(node.item, node.children[item].item)
        return

    def in_generation_prune(self):
        #print('hello')
        for i in range(0, len(self.temp_pattern)):
            temp_current_pattern = copy.deepcopy(self.temp_pattern)
            del temp_current_pattern[i]
            val = self.check_subsets(self.root, temp_current_pattern, 0)
            if val is False:
                return False
        return True
    
    def check_subsets(self, node, temp_pattern, index):
        for i in range(index, len(temp_pattern)):
            if temp_pattern[i] not in node.children:
                return False
            node = node.children[temp_pattern[i]]
        return True
        



    def generate_frequent_itemsets(self, node, level):
        children = copy.deepcopy(node.children)
        node.children = dict()
        if(node.item is not None) and (node.support >= self.threshold) and (level == self.level):
            self.number_of_patterns += 1
            node.visited =True
        child_no = 0
        node.support = 0
        for child in children:
            val = self.generate_frequent_itemsets(children[child], level+1)
            #print(val, 'v')
            if val > 0 :
                child_no += val
                node.children[child] = children[child]
                node.children[child].visited = False
        #print(child_no, node.visited)
        return child_no + node.visited

    def generate_f1_itemset(self):
        #print(self.threshold)
        items_collection = dict()
        for sequence in self.main_database:
            for item in sequence:
                if item not in items_collection:
                    items_collection[item] = 1
                else:
                    items_collection[item] += 1
        temp_L1 = list()
        for item in items_collection:
            if items_collection[item] >= self.threshold:
                temp_L1.append([int(item), items_collection[item]])
        temp_L1.sort()
        return temp_L1
    
    def generate_c2_itemset(self, L1):
        temp_C2 = list()
        length = len(L1)
        for i in range(0, length):
            for j in range(i+1, length):
                temp_C2.append([L1[i][0], L1[j][0]])
        return temp_C2

    def generate_trie(self, node, transaction, index):
        if index>=len(transaction):
            return
        if transaction[index] in node.children:
            child = node.children[transaction[index]]
            child.support = 0
            child.visited = False
            self.generate_trie(child, transaction, index+1)
        else:
            temp_node = TrieNode()
            node.children[transaction[index]] = temp_node
            temp_node.item = transaction[index]
            temp_node.support = 0
            temp_node.visited = False
            self.generate_trie(temp_node, transaction, index+1)

    def support_counter(self, node, transaction):
        node.visited = False
        for child in node.children:
            temp_node = node.children[child]
            if temp_node.item in transaction:
                temp_node.support +=1
                self.support_counter(temp_node, transaction)

if __name__=="__main__":
    inputDB = open('tempdb.txt', 'r')
    database = []
    minSup = 0.6
    for line in inputDB:
        tempdb = []
        line = line.replace('\n', "")
        for item in line.split(" "):
            #item = item.replace(',', "")
            if len(item)!=0:
                tempdb.append(int(item))
                #tempdb.append(ord(item))
        database.append(tempdb)
    print(database)
    start_time = time.time()
    AprioriAlgorithm().mine_patterns(minSup, database)
    print(f'Time Taken: {time.time()-start_time} Seconds')
    




