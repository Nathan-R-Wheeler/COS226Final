# COS226Final
<h2>This is the final project for my Data structures and Algorithms class. It uses B+ trees and A hash table, as well as mergesort to store bulk items.

<h2>How to Run:<br>
The program must be run from the "dataStorage" file
<br>
-When the program first runs, it prompts the user for what function they want the program to carry out:<br>
<br>
1: Create Index<br>
2: Exact value search<br>
3: Range Query<br>
4: Bye<br>
<br>

<h2>If the user selects 1: Create Index:<br>
<br>
-The program will prompt the user to select from a list of properties inside the database:
<br>
0: director<br>
1: genre<br>
2: id - Indexed<br>
3: minDuration<br>
4: movieName<br>
5: productionCompany<br>
6: quote<br>
7: rating<br>
8: releaseDate<br>
<br>
Upon selection the task will be carried out. <br>
<br>
Afterwards, user is returned to the properties menu.<br>
<br>
Upon another selection of property, the program will again 
prompt the user for the function to carry out upon the property.<br>
<br>


<h2>If the user selects 2: Exact Value Search:<br>
<br>
-The program will prompt the user with categories of searchable properties<br>
<br>
-After selecting which category to search, the program prompts the user what to search for<br>
<br>
-After sucessfully returning the searched item the program will prompt the user for what to do with the value.<br>
<br>
-The user can choose to either export it to a csv, or to delete it out of the database.
<br>

<h2>If the user selects 3: Range Query:<br>
<br>

<h2>If the user selects 4: Quit:<br>
<br>
-The program will close

<br>
<br>
<h1>Commands and expected outputs

1. Indexing<br>
-When indexing, the initial input shall be a 1 to start indexing.<br>
-Input 0-9 for the property to be indexed. <br>
-The program should respond with a list of the properties again<br>
-The indexed ones now having "-Indexed" next to their property.<br>

2. Exact Value Search<br>
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


3. Range Query <br>
-Initial input should be 3.<br>




<br>
<h1>Initialization of the database:
<br>
<br>
-In my database initialization, it takes around 0.92 seconds to load the 15000 dataItems, and due to the use of mergesort and bulkAdding, has around O(N Log(N)) efficiency.



<h1>Creation of indexes
<br>
<br>
-In my indexing, it is very fast, as i take already sorted bulk data from the initialization, and place it into a B plus tree. It uses the same Mergesorted data, and so the time it takes is still O(N log(N)). It indexes all data in 0.00002 seconds.



<h1>Queries
<br>



<h1>Deletions
<br>

<h1>
<br>