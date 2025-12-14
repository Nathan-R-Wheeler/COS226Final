#Nathan Wheeler
#Professor Schotter
#COS-226
#12/4/25
from typing import List
import dataStorage
from sympy import isprime


class node:
    def __init__(self, key, value, nextNode = None):
        self.key = key
        self.value = value
        self.next = nextNode

class linkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        #watch for collisions, initiate a counter
        collisions = 0
        #check to see if there is key & value
        if not key  or not value:
            print("Key or Value was none")
            return collisions
        
        newNode = node(key, value)

        if self.head is None:
            self.head = newNode
        
            return collisions
        
        currentNode = self.head
        parentNode = None

        while (currentNode is not None):
            if currentNode.key == key:
                #then the key exists
                return collisions
            else:
                parentNode = currentNode
                currentNode = currentNode.next
            collisions += 1
        parentNode.next = newNode
        return collisions
        
class HashTables():
    #make the empty hash table
    def __init__(self, size):
        self.size = size
        self.collisions = 0

        #for linked list
        self.linkedList = [linkedList() for i in range(size)]


        #for linear probing
        self.linearTable = [None] * size

        #for quadratic probing
        self.quadraticTable = [None] * size

        #to fix collisions and time for implementation #4
        self.prime = self.nextPrime(129)

    def nextPrime(self, num):
        while True:
            if isprime(num):
                return num
            num += 1

     #inserts into the hash function
    # def insert(self, key, value):
    #     hashedKeys = self.hashKey(key)
    #     index = hashedKeys % self.size
    #     linkedList = self.linkedList[index]
    #     self.collisions += linkedList.insert(hashedKeys, value)

    def linearInsert(self, key, value):
        hashed = self.doubleHash(key)
        index = hashed % self.size
        collisions = 0
        while True:
            insertionSlot = self.linearTable[index]

            #check if empty
            if insertionSlot is None:
                self.linearTable[index] = (key, value)
                self.collisions += collisions
                return
            
            #if the key is the same, update it
            if insertionSlot[0] == key:
                return
            
            #if there is a collision, check the next slot
            collisions += 1
            index = (index + 1) % self.size

            #in case the table gets full
            if collisions >= self.size:
                print("The table got full")


    def bulkInsert(self, dataItems):
        for index, dataItems in enumerate(dataItems):
            self.linearInsert(dataItems, index)

    def searhByKey(self, key):
        hashed = self.doubleHash(key)
        index = hashed % self.size
        count = 0
        
        while count < self.size:
            insertionSlot = self.linearTable[index]

            #check if empty
            if insertionSlot is not None and insertionSlot[0] == key:
                return insertionSlot[1]
            
            count += 1
            index = (index + 1) % self.size
        
        return -1

    def deleteByKey(self, key):
        hashed = self.doubleHash(key)
        index = hashed % self.size
        count = 0
        
        while count < self.size:
            insertionSlot = self.linearTable[index]

            #check if empty
            if insertionSlot is not None and insertionSlot[0] == key:
                self.linearTable[index] = None
                return
            
            count += 1
            index = (index + 1) % self.size
        
        return -1

    def hashKey(self, key):
        #do things to stringData, turn it into an int
        #initialize a hashed number
        hashNum = 0
        for ch in key:
            hashNum = (hashNum * self.prime + ord(ch))
        return hashNum
    
    #rehashes the hashkey
    def doubleHash(self, key):
        onceHashed = self.hashKey(key)
        twiceHashed = (onceHashed * self.nextPrime(122))
        return twiceHashed
    
def main():
    counter = 0
    hashTable = HashTables(0)
    tableSize = hashTable.nextPrime(counter * 2)
    hashTable = HashTables(tableSize)
    for theItems in dataStorage.dataItems:
        key = theItems
        hashTable.linearInsert(key, theItems)

if __name__=="__main__":
    main()
