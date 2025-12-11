#Nathan Wheeler
#Professor Schotter
#COS-226
#12/4/25
#DataItem for B+ tree includes self, key, value

#make the max degree that works with my tree
from sympy import Tuple
from dataStorage import DataItem

class Tree:
    def __init__(self, maxdegree):
        self.root = None # reference to the root node
        self.maxdegree = maxdegree # the number of keys that will cause a split
class Bucket:

    def __init__(self, maxdegree):
        self.keys = [] # A list of Keys that are used to organize the data
        self.links = [] # A list of links potential child nodes
        self.parent = None # A link to the parent node
        self.is_leaf = True # A boolean indicating if the node is a leaf node (and thus holds the data in the keys)
        self.next = None # A link to the next leaf node in the chain
        self.prev = None
        self.maxdegree = maxdegree

class bBucket(Bucket):
    
    def getKeyAtIndex(self, index):
        if self.is_leaf:
            return self.keys[index].key
        else:
            return self.keys[index]

    def getSize(self):
        return len(self.keys)

    def bucketRemove(self, key):
        #bucket remove
        #use the target loop again
        target = 0
        while target < len(self.keys):
            dataItem = self.keys[target]
           
            if (dataItem.key == key):
                removedItem = self.keys.pop(target)
                return removedItem
            
            elif dataItem.key > key:
                break
                
            target += 1
        return -1

    def addNodeToInternalBucket(self, key, node):
        targetIndex = len(self.keys)
        #look through the bucket
        for bucketKey in self.keys:
            if key <= bucketKey:
                #find where we will insert
                targetIndex = self.keys.index(bucketKey)
                break
        
        nodeKeyToInsert = targetIndex
        nodeKey = node.keys[0]
        if hasattr(node.keys[0], 'key'): #I don't remeber what this does!!!
            nodeKey = node.keys[0].key

        if (nodeKey >= key):
            nodeKeyToInsert += 1

        self.keys.insert(targetIndex, key)
        self.links.insert(nodeKeyToInsert, node)
        return

    def addValueToLeafBucket(self, key, data):
        targetIndex = len(self.keys)
        #look through the bucket
        for dataItem in self.keys:
            if key < dataItem.key:
                #find where we will insert
                targetIndex = self.keys.index(dataItem)
                break
        self.keys.insert(targetIndex, DataItem(key, data))
        return
    #now that we can add buckets, it is time to find the leaf to add them to
    #whenever adding, we are always adding to a leaf
    
class bTree(Tree):

    def getMinimumAmountOfKeys(self):
        minimumKey = (self.maxdegree - 1) // 2
        return minimumKey

    def remove(self, key): #keep an eye on the parents

        curBucket = self.root
        memory = None #bucket where we find the key early
        memoryIndex = 0 #Which index is in the memory bucket

        if curBucket == None:
            return -1

        if curBucket.is_leaf:
            curBucket.bucketRemove(key)
            return
        
        #find the correct bucket based on the key
            #difference compaired to the add
            #if you find the key early, store the curBucket in memory, and target in memoryIndex
            #if we reach the leafNode and it is still none, dont worry about it

        while (curBucket != None):
            if curBucket.is_leaf:
                break
            else:
                bucketIndex = 0
                for bucketKey in curBucket.keys:
                    if key < bucketKey:
                        break
                    elif key == bucketKey:
                        memoryIndex = bucketIndex
                        bucketIndex += 1
                        memory =  curBucket
                        break
                    bucketIndex += 1

                curBucket = curBucket.links[bucketIndex]

        #if we are close to the bottom, it doesnt matter
        #if memory == curBucket.parent:
         #   memory = None SOLVING IN DIFFERENT PLACE

        if memory != None:
            #fix the memory node
            nextKey = self.findNextKey(curBucket)
            if nextKey != None:
                memory.keys[memoryIndex] = nextKey


        #curBucket is the correct leaf where "key" *might* exist
        remove = curBucket.bucketRemove(key)

        #remove will either have -1 or entire DataItem
        #check
        if remove != -1:
            #found something
            #check to see if we need to fix the leafbucket


            #check if the bucket is smol
            if (len(curBucket.keys) < (self.maxdegree - 1) //2):
                #too small, need to fix
                self.fixLeafBucket(curBucket) #fix the leaf bucket
                
            return f"Found {key} and removed {remove.value}"

        else:
            #didn't find it, let the children know we have no food
            return f"Did not find {key}"


    def fixLeafBucket(self, bbucket):
        leftBucket, rightBucket, linkIndex = self.getSiblings(bbucket)

        #steal left
        if leftBucket != None and self.validSteal(leftBucket) == True:
            self.steal(bbucket, leftBucket, "left", linkIndex)
            return

        #steal right
        elif rightBucket != None and self.validSteal(rightBucket) == True:
               self.steal(bbucket, rightBucket, "right", linkIndex)
               return

        if leftBucket != None:
        #merge left
            self.mergeLeaf(leftBucket, bbucket )
        else:
        #merge right
            self.mergeLeaf(bbucket, rightBucket)


    def getSiblings(self, bbucket):
        #when we fetch siblings we might as well get the left and right sibling and 
        #find where bbucket is in parent.links 
        leftBucket = None
        rightBucket = None

        #find out hwere we are

        target = 0 
        for i in bbucket.parent.links:
            if i == bbucket:
                break
            target += 1

        if target > 0:
            leftBucket = bbucket.parent.links[target - 1]
        if target < len(bbucket.parent.links) -1:
            #if it is possible to have a right sibling
            rightBucket = bbucket.parent.links[target + 1]

        #return all pieces of information
        return leftBucket, rightBucket, target

    def fixKeys(self, bbucket): #will only run on internal buckets
        for linkIndex in range(1, len(bbucket.links)): #we're working with numbers
            #start at 1 continue to end of list
            bbucket.keys[linkIndex -1] = bbucket.links[linkIndex].keys[0].key
        

    def findNextKey(self, bbucket: bBucket):  #only rins on leaf buckets
        #find the next key after key

        #How can we know if there is no next key?
        #key is currently node.keys[0].key
        #how can we see if there is no next key


        if bbucket.getSize() > 1: #bucket is large enough, the next key is here
            return bbucket.keys[1].key
        elif bbucket.next != None: #check if there is  bucket to the right
            return bbucket.next.keys[0].key
        else: 
            return None
        



    def steal(self, bbucket, siblingBbucket, direction, linkIndex):
        #check direction
        keyIndex = linkIndex
        if direction == "left":
            siblingKey = siblingBbucket.getKeyAtIndex(siblingBbucket.getSize() - 1)
            newParentKey = siblingKey
            keyIndex = linkIndex - 1
            parentKey = bbucket.parent.keys[linkIndex]
            if parentKey == siblingKey:
                newParentKey = siblingBbucket.getKeyAtIndex(siblingBbucket.getSize() - 2)

        else: #its right
            siblingKey = siblingBbucket.getKeyAtIndex(0)
            newParentKey = siblingKey
            keyIndex = linkIndex
            parentKey = bbucket.parent.keys[linkIndex]
            if parentKey == siblingKey:
                newParentKey = siblingBbucket.getKeyAtIndex(1)

        siblingValue = siblingBbucket.bucketRemove(siblingKey)
        bbucket.addValueToLeafBucket(siblingValue.key, siblingValue.value)
        bbucket.parent.keys[keyIndex] = newParentKey


    def mergeLeaf(self, leftBucket, rightBucket):
        #take everything in the rightBucket, and stuff it into the left
        leftBucket.keys.extend(rightBucket.keys)
        target = 0
        for link in leftBucket.parent.links:
            if link == leftBucket:
                break
            target += 1
        #now target is the index where leftBucket is
        leftBucket.parent.keys.pop(target)
        leftBucket.parent.links.pop(target + 1)
        leftBucket.next = rightBucket.next #Fixes the next/previous connections.
        if leftBucket.next:
            leftBucket.next.previous = leftBucket
        #now we have to check if the parent is too smol
        if leftBucket.parent.getSize() < self.getMinimumAmountOfKeys():
            self.fixInternalBucket(leftBucket.parent)


    def fixInternalBucket(self, bbucket):
        #if you reach here, the bucket is internal
        #and it is too small

        if bbucket == self.root: # root cqannot be too small, add to fixLeaf
            return
        
        leftSibling, rightSibling, linkIndex = self.getSiblings(bbucket)

        #check if you can steal left
        if self.validSteal(leftSibling):
            self.stealInternal(bbucket, leftSibling, linkIndex, "left")
            return
        #check if you can steal right
        elif self.validSteal(rightSibling):
            self.stealInternal(bbucket, rightSibling, linkIndex, "right")
            return

        if leftSibling != None:
        #merge left
            self.internalMerge(leftSibling, bbucket, linkIndex - 1)
        else:
        #merge right
            self.internalMerge(bbucket, rightSibling, linkIndex)

    def stealInternal(self, bbucket, siblingBucket, linkIndex, direction):
        if direction == "left":
            #the parent.key @ target -1 insert to start of keys in bucket
            keySeparator = bbucket.parent.keys.pop(linkIndex - 1)
            bbucket.keys.insert(0, keySeparator)
            #the last link in leftBucket, pop it and insert it at the start of links in bucket
            steal = siblingBucket.links.pop()
            bbucket.links.insert(0, steal)
            #the left bucket last key, pop it, place it in the parent key, target -1
            lastKey = siblingBucket.keys.pop()
            bbucket.parent.keys.insert(linkIndex -1, lastKey)




        else:
            #same as above, EXCEPT:
            #youre pullling form the start of the right bucket
            #and adding to the END of BUCKET

            #the parent.key @ target +1 insert to end of keys in bucket
            keySeparator = bbucket.parent.keys.pop(linkIndex)
            bbucket.keys.insert(bbucket.getSize(), keySeparator)
            #the last link in leftBucket, pop it and insert it at the start of links in bucket
            steal = siblingBucket.links.pop(0)
            bbucket.links.insert(bbucket.getSize(), steal)
            #the right bucket last key, pop it, place it in the parent key, target +1
            lastKey = siblingBucket.keys.pop(0)
            bbucket.parent.keys.insert(linkIndex +1, lastKey)
            

    def internalMerge(self, leftBucket: bBucket, rightBucket: bBucket, parentKeyIndex):
        #take the parent key between left and right, pop it
        leftBucket.next = rightBucket.next
        parentKey = leftBucket.parent.keys.pop(parentKeyIndex)
        leftBucket.keys.append(parentKey)
        leftBucket.keys.extend(rightBucket.keys)

        for link in rightBucket.links:
            link.parent = leftBucket
            leftBucket.links.append(link)

        #append it to leftBucket.keys
        rightBucket.parent.links.pop(parentKeyIndex + 1)
        #pop the *link* in the parent.links thats pointing to rightBucket
        #DO     NOT     FORGET   THE     PARENTS

        #cycle through all links in rightBucket and set their links to leftBucket
        #stuff all the keys in rightBucket into leftBucket
        #stuff all links from rightBucket into leftBucket

        #if parent.keys length is now 0 and it is the root, set the root to the leftBucket
        if leftBucket.parent.getSize() == 0:
            self.root = leftBucket
        
        #check if parent is too small, (BUT NOT 0) 
        # if so, another internalFix
        elif leftBucket.parent.getSize() < self.getMinimumAmountOfKeys():
            self.fixInternalBucket(leftBucket.parent)

    def validSteal(self, bbucket: bBucket):
        if bbucket == None:
            return False
        return bbucket.getSize() > self.getMinimumAmountOfKeys()

    #this makes the tree
    def add(self, key, value):
        #is the tree empty?
        if self.root == None:
            self.root = bBucket(self.maxdegree)
            self.root.addValueToLeafBucket(key, value)
            return
        else:
            bucket = self.addRecursive(self.root, value, key)

            if (len(bucket.keys) >= bucket.maxdegree):
                self.splitLeaf(bucket)
            #CHECK FOR LEAF OR INTERNAL

    def addRecursive(self, bbucket: bBucket, value, key):
        if(bbucket.is_leaf):
            #by now we are a leaf bucket
            bbucket.addValueToLeafBucket(key, value)
            return bbucket
        else:
            #if we get to here we are an internal bucket
            #we only have keys and not data
            target = 0
            for internalKey in bbucket.keys:
                #by the end of the loop we will arrive at the target to insert into
                if key < internalKey:
                    break
                target += 1
            bbucket = bbucket.links[target]
            return self.addRecursive(bbucket, value, key)

    def splitLeaf(self, bbucket: bBucket):
        newLeaf = bBucket(self.maxdegree)
        middleIndex = self.maxdegree // 2
        newLeaf.keys = bbucket.keys[middleIndex:]
        bbucket.keys = bbucket.keys[:middleIndex]
        newLeaf.prev = bbucket
        newLeaf.next = bbucket.next
        bbucket.next = newLeaf
        
        #if the leaf node is the root
        #this if statement os the very first key
        if(bbucket.parent == None):
            #create a root bucket as internal
            self.root = bBucket(self.maxdegree)
            self.root.is_leaf = False
            #the bucket is empty
            bbucket.parent = self.root #do same for left
            newLeaf.parent = self.root
            self.root.keys = [newLeaf.keys[0].key]
            self.root.links = [bbucket, newLeaf]
            return
        else:
            newLeaf.parent = bbucket.parent
        bbucket.parent.addNodeToInternalBucket(newLeaf.keys[0].key, newLeaf)
        parentNewSize = len(bbucket.parent.keys)
        #if the parent is over the degree, split it
        if (parentNewSize >= self.maxdegree):
            self.splitInternal(bbucket.parent)

    def splitInternal(self, bbucket: bBucket):
        leftNode = bBucket(self.maxdegree)
        leftNode.is_leaf = False
        #we just created the left bucket, but this split does so evenly and with a parent
        middle = self.maxdegree //2
        leftNode.keys = bbucket.keys[:middle]
        #the original bNode.keys is a slice of itself
        #we cannot use the leaf node code because we lose the middle
        stored = bbucket.keys[middle]
        bbucket.keys = bbucket.keys[middle + 1:]
        #we have to get the links copied, we do so by slicing
        #this gets us 1, 2, 3
        leftNode.links = bbucket.links[: middle +1]
        #now get 3, 4, 5
        bbucket.links = bbucket.links[middle + 1:]
        #now loop through all the links and point them back up to their parents
        #LOOP TAKE THE WHEEL, FIX PARENT
        #i is buckets
        for i in leftNode.links:
            i.parent = leftNode

        #check if parent is none
        if (bbucket.parent == None):
            self.root = bBucket(self.maxdegree)  #set to internal, is leaf set to false
            self.root.is_leaf = False
            self.root.keys = [stored]
            self.root.links = [leftNode, bbucket]
            leftNode.parent = self.root
            bbucket.parent = self.root
            return
        
        #if this is not the case
        leftNode.parent = bbucket.parent
        bbucket.parent.addNodeToInternalBucket(stored, leftNode)
        split = len(bbucket.parent.links)
        if(split >= self.maxdegree):
            self.splitInternal(bbucket.parent)

    def bulkInsert(self, keysWithValues: list[any]):
        currentLeafBucket = bBucket(self.maxdegree)
        leafBuckets = [currentLeafBucket]

        for keyWithValue in keysWithValues:
            if currentLeafBucket.getSize() >= int(self.maxdegree / 4 * 3):
                newLeafBucket = bBucket(self.maxdegree)
                newLeafBucket.prev = currentLeafBucket
                currentLeafBucket.next = newLeafBucket
                currentLeafBucket = newLeafBucket
                leafBuckets.append(currentLeafBucket)
            currentLeafBucket.keys.append(keyWithValue[0])
            currentLeafBucket.links.append(keyWithValue[1])

        self.BulkInsertFix(leafBuckets)

    def BulkInsertFix(self, buckets: list[bBucket]):
        if len(buckets) == 1:
            self.root = buckets[0]
            return

        shouldTakeKey = False
        bucketToAdd = bBucket(self.maxdegree)
        bucketToAdd.is_leaf = False
        internalBuckets = []
        for bucket in buckets:
            bucket.parent = bucketToAdd
            bucketToAdd.links.append(bucket)

            if shouldTakeKey:
                bucketToAdd.keys.append(bucket.keys[0])
            else:
                internalBuckets.append(bucketToAdd)
                shouldTakeKey = True
        
            if (len(bucketToAdd.keys) >= self.maxdegree):
                bucketToAdd = bBucket(self.maxdegree)
                bucketToAdd.is_leaf = False
                shouldTakeKey = False
            
        
        self.BulkInsertFix(internalBuckets)
        

        
