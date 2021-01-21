import copy
import time
import itertools
class TrieNode():
    def __init__(self):
        self.item = None
        self.support = 0
        self.children = dict()
        self.visited = False
        self.depth = None
        self.next_same_node = None
        self.path = []


class AprioriAlgorithm():
    items = list()
    main_database = []
    temp_pattern = []
    threshold = 0.0
    total_number_of_frequent_patterns = 0
    total_number_of_candidates = 0
    candidates = []
    link_hash = dict()
    prev_same_item_table = dict()
    level = 0
    prev_sets = []
    number_of_patterns = 0
    candidate_count = 0
    joining_count = 0
    temp_count = 0
    candidate_ns = []
    frequent_ns = []
    isL2 = False
    
    def mine_patterns(self, threshold, db):
        self.main_database = db
        self.threshold = threshold*len(self.main_database)
        
        #self.threshold = 2.0
        print(f'Threshold Support: {self.threshold}')
        L1 = self.generate_f1_itemset()
        #print(L1)
        self.total_number_of_frequent_patterns+=len(L1)
        C2 = self.generate_c2_itemset(L1)
        #print(C2)
        print(f'Frequent Pattern After L1 = {self.total_number_of_frequent_patterns}')
        #self.total_number_of_candidates = self.total_number_of_candidates + len(L1) + len(C2)
        #self.candidates = C2
        #L2 = self.generate_f2_itemset(C2)
        self.level = 2
        self.root = TrieNode()
        f1 = []
        L2 = []
        for item in L1:
            self.link_hash[item[0]] = None
            f1.append(item[0])
        #print(f1)
        for sequence in db:
            tup = []
            for item in f1:
                if item in sequence:
                    tup.append(item)
            self.constructTrie(self.root, tup, 0, 1, [], 0)
        #self.checkTrie(self.root, [])

        for item in C2:
            back_check = item[1]
            self.checkF2Frequent(self.link_hash[back_check], item[0], 0)
            #print(self.isL2, 'helre')
            if self.isL2:
                L2.append(item)
                #print(item, self.temp_count)
            self.temp_count = 0
            self.isL2 = False 
        #print(L2)
        self.total_number_of_frequent_patterns+=len(L2)
        self.prev_sets = L2
        print(f'Frequent Pattern After L2 = {self.total_number_of_frequent_patterns}')
        #print(self.prev_same_item_table)
        ns = 3
        while True:
            for i in range(0, len(self.prev_sets)):
                for j in range(i+1, len(self.prev_sets)):
                    if self.prev_sets[i][:-1] == self.prev_sets[j][:-1]:
                        temp = self.prev_sets[i] + [self.prev_sets[j][-1]]
                        isNotPruned = self.inGenerationPrune(temp)
                        if isNotPruned:
                            self.candidate_ns.append(temp)
            #print(self.candidate_ns)

            for candidate in self.candidate_ns:
                #print(candidate[-1])
                self.checkFrequency(self.link_hash[candidate[-1]], candidate)
                self.joining_count = 0
            #print(self.frequent_ns)
            
            self.total_number_of_frequent_patterns+=len(self.frequent_ns)
            self.prev_sets = self.frequent_ns
            print(f'Frequent Pattern After L{ns} = {self.total_number_of_frequent_patterns}')
            if len(self.frequent_ns) == 0 or len(self.frequent_ns) == 1:
                break
            
            self.frequent_ns = []
            self.candidate_ns = []
            
            ns+=1
            

    def checkFrequency(self, node, can):
        #print(can, node.path, node.item, node.next_same_node, node.support)
        if len(can) <= len(node.path):
            #print('hello')
            l1 = set(can)
            l2 = set(node.path)
            if l1.issubset(l2):
                self.joining_count += node.support
        #print(self.joining_count)
        if node.next_same_node == None:
            #print('here', self.joining_count, self.threshold)
            if self.joining_count >= self.threshold:
                #print('hiii')
                self.frequent_ns.append(can)
                return
            else:
                return
        self.checkFrequency(node.next_same_node, can)
                
    def inGenerationPrune(self, itemset):
        subsets = self.findsubsets(set(itemset), len(itemset)-1)
        for tup in subsets:
            #print(sorted(list(tup)), self.prev_sets)
            if sorted(list(tup)) not in self.prev_sets:
                return False
        return True

    
    def findsubsets(self, s, n): 
        return list(itertools.combinations(s, n)) 
        #print('1')


    def checkF2Frequent(self, node, prev_item, count):
        if prev_item in node.path:
            self.temp_count += node.support
        #print(node.next_same_node)
        if node.next_same_node == None:
            #print('here', node.item, self.temp_count, self.threshold)
            if self.temp_count >= self.threshold:
                #print('hiii')
                self.isL2 = True
                return
            else:
                self.isL2 = False
                return
        self.checkF2Frequent(node.next_same_node, prev_item, count)





    def constructTrie(self, node, transaction, index, support, way, depth):
        if index>=len(transaction):
            return
        if transaction[index] not in node.children:
            node.children[transaction[index]] = TrieNode()
            node.children[transaction[index]].parent_node = node
            node.children[transaction[index]].depth = depth
            if self.link_hash[transaction[index]] == None:
                self.link_hash[transaction[index]] = node.children[transaction[index]]
                self.prev_same_item_table[transaction[index]] = node.children[transaction[index]]
                #print(self.prev_same_item_table[transaction[index]], transaction[index])
            else:

                self.prev_same_item_table[transaction[index]].next_same_node = node.children[transaction[index]]
                #print(self.prev_same_item_table[transaction[index]].next_same_node)
                self.prev_same_item_table[transaction[index]] = node.children[transaction[index]]
                #print(self.prev_same_item_table[transaction[index]])
                #print(self.prev_same_item_table[transaction[index]].next_same_node, node.children[transaction[index]])
        
        node.children[transaction[index]].item = transaction[index]       
        node.children[transaction[index]].support += support
        
        if len(way) != 0:
            node.children[transaction[index]].path = way
        way.append(node.children[transaction[index]].item)
        self.constructTrie(node.children[transaction[index]], transaction, index+1, support, copy.deepcopy(way), depth+1)

    def checkTrie(self, node, branch):
        if node.item is not None:
            branch.append(node.item)
        
        print(node.item, node.path, node.support, 'this')
        for child in node.children:
            self.checkTrie(node.children[child], copy.deepcopy(branch))
        return

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


if __name__=="__main__":
    inputDB = open('tempdb.txt', 'r')
    database = []
    minSup = 0.2
    for line in inputDB:
        tempdb = []
        line = line.replace('\n', "")
        for item in line.split(" "):
            #item = item.replace(',', "")
            if len(item)!=0:
                #tempdb.append(int(item))
                tempdb.append(ord(item))
        database.append(tempdb)
    #print(database)
    start_time = time.time()
    AprioriAlgorithm().mine_patterns(minSup, database)
    print(f'Time Taken: {time.time()-start_time} Seconds')