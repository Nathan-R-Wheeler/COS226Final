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

class Database:

    def __init__(self):
        self.maxDegree = 100
        self.dictPropertyMetaData = dict()
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
            isNumber = isinstance(getattr(singleItem, property), int) or isinstance(getattr(singleItem, property), float)
            self.dictPropertyMetaData[property] = PropertyMetaData(isIndex, isSearchable, isNumber)

            for item in items:
                propertiesToInsert.append(getattr(item, property))

            if isSearchable:
                self.searchableProperties[property] = HashTables(len(items))
                self.searchableProperties.get(property).bulkInsert(propertiesToInsert)

            if isIndex:
                self.createIndex(property)

        
    #gets the properties in the dataItem
    def getAllProperties(self):
        return self.dictPropertyMetaData
    
    #creates an index for the Items
    def createIndex(self, property):
        self.dictPropertyMetaData[property].isIndex = True
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

    def BetweenValuesRangeIndexSearch(self, property, lowerValue, higherValue):
        propertyMetaData = self.dictPropertyMetaData[property]

        if (propertyMetaData.isNumber):
            if lowerValue.isdigit():
                lowerValue = int(lowerValue)
            else:
                return []
            if higherValue.isdigit():
                higherValue = int(higherValue)
            else:
                return []

        tree = self.btreeIndexes.get(property)
        indexResults = tree.FindDataItemsBetweenValues(lowerValue, higherValue)
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result
    
    def BelowValueRangeIndexSearch(self, property, value):
        propertyMetaData = self.dictPropertyMetaData[property]

        if (propertyMetaData.isNumber):
            if value.isdigit():
                value = int(value)
            else:
                return []
 
        tree = self.btreeIndexes.get(property)
        indexResults = tree.FindDataItemsBelowValue(value)
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result
    
    def AboveValueRangeIndexSearch(self, property, value):
        propertyMetaData = self.dictPropertyMetaData[property]

        if (propertyMetaData.isNumber):
            if value.isdigit():
                value = int(value)
            else:
                return []
            
        tree = self.btreeIndexes.get(property)
        indexResults = tree.findDataItemsAboveValue(value)
        result = []
        for index in indexResults:
            result.append(self.primaryStorage[index])
        return result

    def deleteFromDatabase(self, dataItems):
        for dataItem in dataItems:
            for property, tree in self.btreeIndexes.items():
                key = getattr(dataItem, property)
                tree.remove(key)

            for property, table in self.searchableProperties.items():
                key = getattr(dataItem, property)
                table.deleteByKey(key)

            self.primaryStorage[dataItem.id] = None


class PropertyMetaData:
    
    def __init__(self, isIndex, isSearchable, isNumber):
        self.isIndex = isIndex
        self.isSearchable = isSearchable
        self.isNumber = isNumber