#Nathan Wheeler
#Professor Schotter
#COS-226
#12/4/25


from typing import List
from BPlusTree import bTree
from HashTable import HashTables
from dataStorage import DataItem
from sorter import mergeSORT, indexKey
import time


#Database stores the dataItems
#manages indexes and structures to help with fast lookup
class Database:

    def __init__(self):
        #set the maxdegree for the B+ tree
        self.maxDegree = 100
        #store data about properties
        self.dictPropertyMetaData = dict()
        #store indexes for b plus trees
        self.btreeIndexes = dict()
        #stores hash tables for searchable properties
        self.searchableProperties = dict()
        #make a main storage for dataItems
        self.primaryStorage = None

    #adds the bulk information for the DataItems
    def bulkAdd(self, items: list[DataItem]):
        #store the list of dataItems
        self.primaryStorage = items

        #if there is nothing to do
        if len(items) == 0:
            return
        #use first item to inspect properties
        singleItem = items[0]
        Properties = dir(singleItem)

        #loop through properties
        for property in Properties:
            if property.startswith("__"):
                continue
            
            isIndex = False
            isSearchable = False
            #the id is always indexed
            if property == "id":
                isIndex = True
            
            #moviename and quote will be searchable
            if property == "movieName" or property == "quote":
                isSearchable = True

            propertiesToInsert =  []
            #check if property has numeric values
            isNumber = isinstance(getattr(singleItem, property), int) or isinstance(getattr(singleItem, property), float)
            #store data for the property
            self.dictPropertyMetaData[property] = PropertyMetaData(isIndex, isSearchable, isNumber)

            #get all values for this from every dataItem
            for item in items:
                propertiesToInsert.append(getattr(item, property))

            #if its searchable, we make a hash table and put imn the values
            if isSearchable:
                self.searchableProperties[property] = HashTables(len(items))
                self.searchableProperties.get(property).bulkInsert(propertiesToInsert)
         
            #if it is indexed we make a B+ tree index
            if isIndex:
                self.createIndex(property)

        
    #gets the properties in the dataItem
    def getAllProperties(self):
        return self.dictPropertyMetaData
    
    #creates a b+ index for the Items
    def createIndex(self, property):
        #mark as indexed
        self.dictPropertyMetaData[property].isIndex = True
        #make new tree
        self.btreeIndexes[property] = bTree(100)

        propertiesToIndex = []
        index = 0

        #collect the value and key pairs
        for item in self.primaryStorage:
            propertiesToIndex.append((getattr(item, property), index))
            index += 1

        #sort before entering   
        mergeSORT(propertiesToIndex, key=indexKey)
        #bulk insert the data
        self.btreeIndexes.get(property).bulkInsert(propertiesToIndex)

    #preforms the exact search by hash table
    def exactSearch(self, property: str, stringToSearch: str):
        result = self.searchableProperties[property].searhByKey(stringToSearch)

        #if it was not found
        if (result == -1):
            return None
        else:
            #return the item
            return self.primaryStorage[result]

    #finds the items between two values
    def BetweenValuesRangeIndexSearch(self, property, lowerValue, higherValue):
        propertyMetaData = self.dictPropertyMetaData[property]

        #if it is numeric, make int
        if (propertyMetaData.isNumber):
            if lowerValue.isdigit():
                lowerValue = int(lowerValue)
            else:
                return []
            if higherValue.isdigit():
                higherValue = int(higherValue)
            else:
                return []

        #preform range search of tree
        tree = self.btreeIndexes.get(property)
        indexResults = tree.FindDataItemsBetweenValues(lowerValue, higherValue)
        #retrieve the dataItems using the indexes
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result
    
    #finds what data is below value
    def BelowValueRangeIndexSearch(self, property, value):
        propertyMetaData = self.dictPropertyMetaData[property]

        if (propertyMetaData.isNumber):
            if value.isdigit():
                value = int(value)
            else:
                return []
        #does the search
        tree = self.btreeIndexes.get(property)
        indexResults = tree.FindDataItemsBelowValue(value)
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result
    #finds the data above a value
    def AboveValueRangeIndexSearch(self, property, value):
        propertyMetaData = self.dictPropertyMetaData[property]

        if (propertyMetaData.isNumber):
            if value.isdigit():
                value = int(value)
            else:
                return []
        #does the search    
        tree = self.btreeIndexes.get(property)
        indexResults = tree.findDataItemsAboveValue(value)
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result

    #deletes from all databases and indexes
    def deleteFromDatabase(self, dataItems):
        for dataItem in dataItems:
            #remove from B+ trees indexes
            for property, tree in self.btreeIndexes.items():
                key = getattr(dataItem, property)
                tree.remove(key)

            #remove from all hash tables
            for property, table in self.searchableProperties.items():
                key = getattr(dataItem, property)
                table.deleteByKey(key)
            #mark item as deleted in storage
            self.primaryStorage[dataItem.id] = None

#stores data about dataITems
class PropertyMetaData:
    
    def __init__(self, isIndex, isSearchable, isNumber):
        #tells if this has an index
        self.isIndex = isIndex
        #teoos if it can be searched in a hash table
        self.isSearchable = isSearchable
        #tells if it is a number
        self.isNumber = isNumber