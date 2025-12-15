# COS226Final
<h1>This is the final project for my Data structures and Algorithms class. It uses indexes in B+ trees and A linked list hash table, as well as mergesort to store bulk items.

<h1>How to Run:<br>
-The program must be run from the "dataStorage" file
<br>
-When the program first runs, it prompts the user with the main menu for what function they want the program to carry out:<br>
<br>
<h1>Commands and expected outputs:

1. Indexing: <br>
-When indexing, the initial input shall be a 1 to start indexing.<br>
-Input 0-9 for the property to be indexed. <br>
-The program should respond with a list of the properties again<br>
-The indexed ones now having "-Indexed" next to their property.<br>

2. Exact Value Search: <br>
-The user should initially input 2.<br>
-The program will prompt the user for choice of using the title or a quote.<br>
-The user enters 0 for Title, and 1 for Quote.<br>
-The program confirms their choice, and asks for input of title/quote.<br>
-The user inputs "Bee Movie".<br>
-The program will either deny the item in the database, or return it has found it.<br>
-The program will prompt the user to export it in a csv with 0, or remove it from the database with 1.<br>
-If the user choses 0, the program adds the choice to a .csv.<br>
-If the user choses 1, the program deletes it from the list.<br>
-The program then returns to the main menu.<br>


3. Range Query: <br>
-First, you must Index what you wish to Query.<br>
-Initial input should be 3.<br>
-The program will return a list of indexed properties to choose.<br>
-The user will enter in the corresponding number for their property.<br>
-The program will ask if the user wants to choose less than (0), greater than (1), or in between two values (2)<br>
-The user will input 0-2.<br>
-The program will prompt for the value(s) to search by.<br>
-The user will input the corresponding value(s).<br>
-The program will either deny the items in the database for that range, or return the values in the range.<br>
-The program will prompt the user to export them in a csv with 0, or remove them from the database with 1.<br>
-If the user choses 0, the program adds the values to a .csv.<br>
-If the user choses 1, the program deletes them from the list.<br>
-The program then returns to the main menu.<br>

4. Bye:<br>
-The user inputs 4.<br>
-The program thanks the user and terminates<br>




<br>
<h1>Initialization of the database:
<br>
<br>
-In my database initialization, it takes around 0.92 seconds to load the 15000 dataItems, and due to the use of mergesort and bulkAdding, has around O(N log(N)) efficiency.



<h1>Creation of indexes:
<br>
<br>
-In my indexing, it is very fast, as i take already sorted bulk data from the initialization, and place it into a B plus tree. It uses the same Mergesorted data, and so the time it takes is still O(N log(N)). It indexes all data in 0.00002 seconds.



<h1>Queries:
<br>
-My queries are based off of exact values and indexes. My implementation of exact value uses a hash table with a double hashed linked list. at best it has an efficiency of O(n) and at worst its efficiency is O(1). The B plus tree, which has an efficiency of (O log(N)) is used for indexing.



<h1>Deletions:
<br>
-My deletion first has to delete from all hash tables, and due to my linked list setup, this takes around O(n) time to complete, next it deletes all the indexes and values from the b+ trees, which due to the nature of the B+ tree, this takes (O log(n)) time.

<h1>
<br>

<h1>Hash function design choices:<br>
-I chose to implement the best hash that I hav made within my hashing functions homework. It uses a double hashed linked list. I used this for my database because it had minimal collisions and good time efficiency in my other homework. <br>

<h1>BPlus tree implementation approach:<br>
-In my B plus tree, I took the one I made for homework, and added object oriented implementation for all of the properties in the dataItems.<br>
-I refactored the tree to be bottom up when making the bulk insert for efficiency. that way it does not have to rotate, merge or steal. as well as keeping the buckets only 3/4ths fill, lowers the amount of merges and steals that have to happen.<br>

<h1>Searching Choices: <br>
-I made only the Title and Quotes searchable, because that is what makes sense to me, as although movies that share the same title are more common than ones that contain exactly the same quotes, most people look up what movie they are searching for by the title or phrases in the movie. I did not make the director searchable, because directors make tend to have multiple movies, and not many people look up movies by director. The fields that I did not make searchable are the numeric ones, such as rating, revanue, duration. But also the fields in which multiple movies share, like genre, director, production company, I chose to have those indexable as well.

<h1>Limitations and Issues: <br>
-If indexing a large amount of dataItems, the writing to file feature can handle it no problem, however the deletion can sometimes crash the program. I am not too sure how to fix this, but deleting one or a few at a time works fine.<br>