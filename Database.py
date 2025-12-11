#Nathan Wheeler
#Professor Schotter
#COS-226
#12/4/25
from typing import List
from BPlusTree import bTree
from HashTable import HashTables
from dataStorage import DataItem
from sorter import mergeSORT, indexKey

class Database:

    def __init__(self):
        self.maxDegree = 100
        self.dictPropertyIsIndex = dict()
        self.btreeIndexes = dict()
        self.searchableProperties = dict()
        self.primaryStorage = None

    #adds the bulk information for the DataItems
    def bulkAdd(self, items: list[DataItem]):
        self.primaryStorage = items

        if len(items) == 0:
            return

        singleItem = items[0]
        Properties = dir(singleItem)

        for property in Properties:
            if property.startswith("__"):
                continue
            
            isIndex = False
            isSearchable = False

            if property == "id":
                isIndex = True
            
            if property == "movieName" or property == "quote":
                isSearchable = True

            propertiesToInsert =  []
            self.dictPropertyIsIndex[property] = PropertyMetaData(isIndex, isSearchable)

            for item in items:
                propertiesToInsert.append(getattr(item, property))

            if isSearchable:
                self.searchableProperties[property] = HashTables(len(items))
                self.searchableProperties.get(property).bulkInsert(propertiesToInsert)

            if isIndex:
                self.createIndex(property)


    #gets the properties in the dataItem
    def getAllProperties(self):
        return self.dictPropertyIsIndex
    
    #creates an index for the Items
    def createIndex(self, property):
        self.dictPropertyIsIndex[property].isIndex = True
        self.btreeIndexes[property] = bTree(100)

        propertiesToIndex = []
        index = 0

        for item in self.primaryStorage:
            propertiesToIndex.append((getattr(item, property), index))
            index += 1
            
        mergeSORT(propertiesToIndex, key=indexKey)
        self.btreeIndexes.get(property).bulkInsert(propertiesToIndex)

    def exactSearch(self, property: str, stringToSearch: str):
        result = self.searchableProperties[property].searhByKey(stringToSearch)

        if (result == -1):
            return None
        else:
            return self.primaryStorage[result]

class PropertyMetaData:
    
    def __init__(self, isIndex, isSearchable):
        self.isIndex = isIndex
        self.isSearchable = isSearchable