#Nathan Wheeler
#Professor Schotter
#COS-226
#12/15/25

#Merge
              #O(Nlog(N))

#this piece implements a sorter for the bulk loading of dataItems
#added key for functionality

def mergeSORT(x, key = None):
    if key is None:
        def key(v):
            return v
        
    mergeSPLIT(x, 0, len(x)-1, key )

def indexKey(pair):
    return pair[0]

def mergeSPLIT(x,leftBound, rightBound, key):
    if (rightBound - leftBound)== 0: #array is size 1
        return
    # left half of our array section 
    # start is leftbound
    # right is (rightBound + leftbound) //2

    #right half of array section
    #start is leftEnd + 1
    #end is rightBound

    leftEnd = (rightBound + leftBound) //2
    rightStart = leftEnd +1

    mergeSPLIT(x, leftBound, leftEnd, key)
    mergeSPLIT(x, rightStart, rightBound, key)
    
    #check to see if we are already sorted
    if key(x[leftEnd]) <= key(x[rightStart]):
        return
    
    tempSpace = x[leftBound:rightStart]
    #we're gonna put a pointer at the start of our sublists
   
    

    #compaire the size of the 2
    #while i or j still has space to run

    #copy left subarray into temp space
    tempSpace = x[leftBound: rightStart] #slicing in inclusive on the right exclusive on the left



    i = 0
    j = rightStart
    k = leftBound # location where we plop the sorted number

    while(i < len(tempSpace)  or j <= rightBound): #by the end of the while we need our 
        # subarrays into a sorted array
        leftDone = (i >= len(tempSpace))
        rightDone = (j > rightBound)
        
        if not leftDone and (rightDone or key(tempSpace[i])< key(x[j])):

            x[k] = tempSpace[i]
            i += 1
        else:
            x[k] = x[j]
            j += 1
        k += 1 #set k to be the next spot for next sorted number