#Nathan Wheeler
#Professor Schotter
#COS-226
#12/4/25

#this program uses 3 different programs from my class to make a database system.
# it uses a slightly modified version of my B+ tree
# as well as my hashtable which I will set to the most efficient of the types it contains
# it also uses the mergesort that we built in class, but modified to sort alphabetically

import csv
import time

#Make the DataItems
class DataItem:

    def __init__(self, id, movieName, genre, releaseDate, director, revenue, rating, minDuration, productionCompany, quote):
        self.id = id
        self.movieName = movieName
        self.genre = genre
        self.releaseDate = releaseDate 
        self.director = director
        self.revenue = revenue
        self.rating = rating
        self.minDuration = minDuration
        self.productionCompany = productionCompany
        self.quote = quote

def main():
    import Database
    #first load the data
    file = "MOCK_DATA.csv"
    dataItems = []
    database = Database.Database()
    index = 0
    with open(file, 'r', newline= '', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            if (len(row) >= 9):
                items = DataItem(
                    id = index,
                    movieName = row[0],
                    genre = row[1],
                    releaseDate = row[2],
                    director = row[3],
                    revenue = row[4],
                    rating = row[5],
                    minDuration = row[6],
                    productionCompany = row[7],
                    quote = row[8]
                )

                index += 1
                dataItems.append(items)

    database.bulkAdd(dataItems)

    shouldExit = False
    print("Welcome to super mega databse engine 2.0!")


        #prompts the user for input of their intention
    while (not shouldExit):
        print("Please Input what you want to do!")
        print("1: Create Index")
        print("2: Exact value search")
        print("3: Range Query")
        print("4: Bye")
        choice = input("Enter your choice: ")

        print("\n")
        if choice == "1":
            HandleIndexCreation(database)

        elif choice == "2":
            HandleValueSearch(database)
            
        elif choice == "3":
            HandleRangeQuery()
            pass
        elif choice == "4":
            print("The super mega databse engine 2.0 is shutting down")
            time.sleep(3)
            print("... bye")
            shouldExit = True
        else:
            time.sleep(3)
            print("Loaser")
            time.sleep(1)

#handles the index user choice case
def HandleIndexCreation(database):
    hasChosen = False
    chosenProperty = None
    propertiesIsIndexed = database.getAllProperties()
    if all(value.isIndex == True for _, value in propertiesIsIndexed.items()):
        print("All properties are indexed!")
        return
    
    while(not hasChosen):
        print("Here's all the property inside the database:")
        propertyList = []
        index = 0
        for key, value in propertiesIsIndexed.items():
            propertyList.append(key)
            propertyName = key
            if value.isIndex == True:
                propertyName = propertyName + " - Indexed"
            print(str(index) + ": " + propertyName)
            index = index + 1
        choice = input("Please Select property to index: ")
        #handles the property choices
        #checks for the input to be digit
        if choice.isdigit():
            chosenIndex = int(choice)
            if (chosenIndex >= 0 and chosenIndex < len(propertyList)):
                chosenProperty = propertyList[chosenIndex]

                if propertiesIsIndexed.get(chosenProperty).isIndex == True:
                    print("This property is already indexed!")
                else:
                    hasChosen = True
            else:
                print("That number is not a correct one!")
        else:
            print("That's not a number!")
        
        print("\n")

    print("You have chosen this property: " + chosenProperty)
    database.createIndex(chosenProperty)

def HandleValueSearch(database):
    hasChosen = False
    chosenProperty = None
    propertiesIsIndexed = database.getAllProperties()
    
    while(not hasChosen):
        print("Here's all the searchable property inside the database:")
        propertyList = []
        index = 0
        for key, value in propertiesIsIndexed.items():
            if value.isSearchable == True:
                propertyList.append(key)
                print(str(index) + ": " + key)
                index = index + 1

        choice = input("Please Select property to search: ")

        #handles the property choices
        #checks for the input to be digit
        if choice.isdigit():
            chosenIndex = int(choice)
            if (chosenIndex >= 0 and chosenIndex < len(propertyList)):
                chosenProperty = propertyList[chosenIndex]
                hasChosen = True      
            else:
                print("That number is not a correct one!")
        else:
            print("That's not a number!")
        
        print("\n")

    print("You have chosen this property: " + chosenProperty)

    searchWords = input("Please input what you want to search: ")

    print("Now searching this: " + searchWords)
    
    result = database.exactSearch(chosenProperty, searchWords)

    if (result == None):
        print("We couldn't find any dataitem like this")
    else:
        HandleResult(database, [result])

def HandleRangeQuery():
    pass


def HandleResult(database, results):
    print("We found one, boss")
    print("Watcha wanna do with this one, boss?")
    
    while True:
        print("\n")
        print("0: Export him out in an excel")
        print("1: Whack him out of za database")

        answer = input("It's your call, boss: ")

        if (answer == "0"):
            print("Right boss, let's show this fool his way out into an excel")
            exportToExcel(database, results)
            return
        
        if (answer == "1"):
            print("Let's take him out, boys")
            return
        
        print("Boss, that ain't a good choice, lemme ask again")


def exportToExcel(database, results):
    allProperties = database.getAllProperties()

    line = []

    for key, _ in allProperties.items():
        line.append(key)

    with open("result.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(line)

        for result in results:
            line = []
            for key, _ in allProperties.items():
                line.append(getattr(result, key))
            writer.writerow(line)

    print("The result has been exported!")

if __name__ == "__main__":
    main()