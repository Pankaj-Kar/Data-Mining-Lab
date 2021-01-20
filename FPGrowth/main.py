import operator
import copy
import time
class FPNode():
    def __init__(self):
        self.item = None
        self.support = 0
        self.parent_node = None
        self.next_link_node = None
        self.children = dict()
        self.path = []


class FPGrowth():
    threshold = 0
    items = list()
    main_database = []
    node_link_table = dict()
    prev_same_item_table = dict()
    root = None

    def minePattern(self, threshold, db):
        self.main_database = db
        self.threshold = threshold*(len(self.main_database))
        print(f'Threshold Support: {self.threshold}')
        L1 = self.generate_f1_itemset()
        sortedL1 = sorted(L1, key=operator.itemgetter(1), reverse=True)
        mp = dict()
        for pair in sortedL1:
            mp[pair[0]] = pair[1]
            self.node_link_table[pair[0]] = None
        
        self.root = FPNode()
        self.root.item = 'R'
        
        for sequence in db:
            tempSeq = []
            for item in mp:
                if item in sequence:
                    #print(item)
                    tempSeq.append([item, mp[item]])
            sortedSeq = sorted(tempSeq, key=operator.itemgetter(1), reverse=True)
            tup = []
            for item in sortedSeq:
                tup.append(item[0])
            #print(tup)
            self.constructFPTree(self.root, tup, 0, 1, [])
        #self.checkFPTree(self.root, [])
        reverse_sorted_L1 = sortedL1[::-1]
        #print(reverse_sorted_L1)
        '''Conditional FP Tree'''
        for i in range(0, len(reverse_sorted_L1)-1):
            item = reverse_sorted_L1[i][0]
            node = self.node_link_table[item]
            #print(item)
            tempCFPMap = dict()
            tempCFPitems = []
            freqCFP = []
            while True:
                #print(item, node.support, node.path, 'A')
                for itm in node.path:
                    if item != itm:
                        if itm not in tempCFPitems:
                            tempCFPMap[itm] = node.support
                            tempCFPitems.append(itm)
                        else:
                            tempCFPMap[itm] += node.support
                #print(tempCFPMap)
                if node.next_link_node == None:
                    break
                node = node.next_link_node
            #print(chr(item), tempCFPMap)
            
            for itm in tempCFPitems:
                if tempCFPMap[itm] >= self.threshold:
                    freqCFP.append(chr(itm))
            print(chr(item), freqCFP, 'fp')
                
            #print(reverse_sorted_L1[i][0])

        

            

        
        #print(L1)
        #print(mp, self.node_link_table)

    def constructFPTree(self, node, transaction, index, support, way):
        #if node.item == 102:
            #print(way, 'way', )
        if index>=len(transaction):
            return
        if transaction[index] not in node.children:
            node.children[transaction[index]] = FPNode()
            node.children[transaction[index]].parent_node = node
            if self.node_link_table[transaction[index]] == None:
                self.node_link_table[transaction[index]] = node.children[transaction[index]]
                self.prev_same_item_table[transaction[index]] = node.children[transaction[index]]
            else:
                self.prev_same_item_table[transaction[index]].next_link_node = node.children[transaction[index]]
                self.prev_same_item_table[transaction[index]] = node.children[transaction[index]]
            
        node.children[transaction[index]].item = transaction[index]       
        node.children[transaction[index]].support += support
        if len(way) != 0:
            node.children[transaction[index]].path = way
            #if node.children[transaction[index]].item == 102:
                #print(node.children[transaction[index]].path,  way, 'here')
        #print(f'Way of {node.children[transaction[index]].item} = {node.children[transaction[index]].path} and {node.children[transaction[index]].support}')
        way.append(node.children[transaction[index]].item)
        #if node.children[transaction[index]].item == 102:
            #print(node.children[transaction[index]].path,  way, 'here')
        self.constructFPTree(node.children[transaction[index]], transaction, index+1, support, copy.deepcopy(way))
        #if node.children[transaction[index]].item == 102:
                #print(node.children[transaction[index]].path)

    def checkFPTree(self, node, branch):
        if node.item is not None:
            branch.append(node.item)
        
        print(node.item, node.path, node.support, 'this')
        for child in node.children:
            self.checkFPTree(node.children[child], copy.deepcopy(branch))
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
    #print(database)
    #start_time = time.time()
    temp_time = time.time()
    FPGrowth().minePattern(minSup, database)
    print(time.time()-temp_time)
    #print(f'Time Taken: {time.time()-start_time} Seconds')