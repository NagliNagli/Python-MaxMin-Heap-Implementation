from math import ceil, log2, floor

def swap(collection, a, b):
    # function which swaps 2 indexes.
    c = collection[a]
    collection[a] = collection[b]
    collection[b] = c


class MaxMinHeap(object):
    # function which initializes the array. the self.__mCount is the length of the heap, and the mList is the array.
    def __init__(self, lst=["x"]):
        self.__mList = lst
        self.__mCount = len(self.__mList) - 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # This function will make the output of the heap to present as Tree structure.
        printMe = "Heap contains: {} nodes\n".format(self.__mCount)
        if self.__mCount == 0:
            print("Heap is empty")
        else:
            height = ceil(log2(self.__mCount))
            i = 1
            max_len = 2 ** height * 2
            for k in range(height + 1):
                for n in range(2 ** k):
                    if i <= self.__mCount:
                        wid = ceil(max_len / (2 ** k))
                        num = "{0:{1}>2d}".format(self.__mList[i], "0")
                        printMe += "{:^{width}}".format(num, width=wid)
                        i += 1
                    else:  # in case where last level has less then 2^current level nodes
                        break
                if k != height:
                    printMe += "\n"

                    for j in range(int(2 ** (height - k - 1))):
                        for h in range(2 ** k):
                            index = int(2 ** (k)) + h
                            left = '/' if 2 * index <= self.__mCount else ' '
                            middle = (j + 1) * 2 * ' '
                            right = '\\' if 2 * index + 1 <= self.__mCount else ' '
                            path = left + middle + right
                            wid = ceil(max_len / (2 ** k))
                            printMe += "{:^{width}}".format(path, width=wid)
                        printMe += '\n'

        return printMe

    def buildHeap(self):
        # This function will build given heap, making each node appear in it's correct spot.
        length_without_leaves = self.getLength() // 2  # In order to build the heap, i wont need to heapify the Leaves.
        for i in range(length_without_leaves, 0, -1):  # Going through the entire heap without the last level.
            self.heapify(i)  # arranging the heap from upside>down, which will make the heap eventually arranged.
        return self

    def heapify(self, i):
        # This function will arrange the heap Upside-down.
        height = floor(log2(i))  # Performing a check if i'm in odd or even level.
        if height % 2 == 1:
            self.minHeapify(i)  # If i'm on odd level, performing min-heapify procedure
        else:
            self.maxHeapify(i)  # If i'm on even level, performing max-heapify procedure

    def maxHeapify(self, i):
        # This function will arrange the heap Upside-down, on max levels.
        if self.hasChildren(i):
            if self.hasGrandChild(i):
                # I need to determine which node has the highest value of my descendants
                m = self.maxChildAndGrandChild(i)
                if self.isGrandChild(i,m): # checking if the descendant with the maximum value is a grandchild of i
                    if self.__mList[m] > self.__mList[i]:
                        swap(self.__mList, m, i)  # swapping if it's value is bigger than it's grand-father.
                        if self.__mList[m] < self.__mList[self.getParent(m)]:
                            # swapping if the grandfather value is lower than it's father.
                            swap(self.__mList, m, self.getParent(m))
                    self.maxHeapify(m)  # re-arranging the heap after the swap has been completed.
                elif self.__mList[m] > self.__mList[i]:
                    swap(self.__mList, m, i)
            # if there are no grandchilds, i will check only with it's child, in order to not exceed the heap length.
            else:
                m = self.maxChild(i)
                if self.__mList[m] > self.__mList[i]:
                    swap(self.__mList, m, i)

    def minHeapify(self, i):
        # This function will arrange the heap Upside-down, on min levels.
        if self.hasChildren(i):
            if self.hasGrandChild(i):
                m = self.minChildAndGrandChild(i)
            else:
                m = self.smallestChild(i)
            if self.isGrandChild(i,m):
                if self.__mList[m] < self.__mList[i]:
                    swap(self.__mList, m, i)
                    if self.__mList[m] > self.__mList[self.getParent(m)]:
                        swap(self.__mList, m, self.getParent(m))
                self.minHeapify(m)
            elif self.__mList[m] < self.__mList[i]:
                swap(self.__mList, i, m)

    def insert(self, key):
        # This function will insert new key to the heap, and arrange it accordingly.
        self.__mList.append(key)  # adding the new value to the last place in the array.
        self.__mCount += 1 # increasing the heap length by 1.
        # sorting the heap from the bottom to the top in order to maintain the heap structure
        self.bubbleUp(self.__mCount)

    def heapsort(self):
        # This function will sort the array, print the sorted output, and rearrange the heap to it's original form.
        sortedarr = [None] * int(self.__mCount)  # creating empty array with the number of nodes.
        for i in range(self.__mCount,0,-1):
            sortedarr[(i - 1)] = (self.__mList[1]) # the last element of my array will be the root (The maximum value)
            if self.__mCount == 3:
                # a check to determine how to decide which value to swap with the root, very identical to finding max.
                maxchildren = self.maxChild(1)
                swap(self.__mList, maxchildren, self.__mCount)
                swap(self.__mList, 1, self.__mCount)
                self.__mCount -= 1
                self.__mList = self.__mList[:-1]
                self.heapify(1)
            elif self.__mCount > 4:
                # a check to determine how to decide which value to swap with the root, very identical to finding max.
                # this occurs when the heap has grandchilds.
                maxgrandchildren = self.maxGrandChildren(1)
                swap(self.__mList, maxgrandchildren, self.__mCount)
                swap(self.__mList, 1, self.__mCount)
                self.__mCount -= 1
                self.__mList = self.__mList[:-1]
                self.heapify(1)

            else:
                # when there is only one child.
                swap(self.__mList, 1, self.__mCount)
                self.__mCount -= 1
                self.__mList = self.__mList[:-1]
                self.heapify(1)
        print("The sorted array is:")
        print(sortedarr)
        print("\nRebuilding your heap\n")
        # rebuilding the heap so the user could continue using operations as he wishes.
        for i in range(len(sortedarr)):
            self.insert(sortedarr[i])


    def bubbleUp(self, i):
        # This function will rearrange the heap after insertion.
        # Performing a check if i'm in odd or even level.
        height = floor(log2(i))
        if height % 2 == 1:
            if self.hasParent(i):
                # if the current value on the Min level is larger than it's parent on the Max level, i will make a swap.
                if self.__mList[i] > self.__mList[self.getParent(i)]:
                    swap(self.__mList, i, self.getParent(i))
                    # Rearranging the heap from the bottom to the top after the swap on max levels.
                    self.maxBubbleUp(self.getParent(i))
                else:
                    # Rearranging the heap from the bottom to the top, on min levels.
                    self.minBubbleUp(i)
        else:
            if self.hasParent(i) and self.__mList[i] < self.__mList[self.getParent(i)]:
                swap(self.__mList, i, self.getParent(i))
                self.minBubbleUp(self.getParent(i))
            else:
                self.maxBubbleUp(i)

    def maxBubbleUp(self, i):
        # Checking if the node has grandparent, on maxlevel which has lower value, then i would make a swap.
        if self.hasGrandParent(i):
            if self.__mList[i] > self.__mList[self.getGrandParent(i)]:
                swap(self.__mList, i, self.getGrandParent(i))
                #  i will make the process until there are no grandparents left.
                self.maxBubbleUp(self.getGrandParent(i))

    def minBubbleUp(self, i):
        # checking if the node has grandparent on minlevel, which has higher value, then i would make a swap.
        if self.hasGrandParent(i):
            if self.__mList[i] < self.__mList[self.getGrandParent(i)]:
                swap(self.__mList, i, self.getGrandParent(i))
                #  i will make the process until there are no grandparents left.
                self.minBubbleUp(self.getGrandParent(i))

    def printHeap(self):
        #  printing the heap as "Tree" structure.
        print(self)

    def extract_max(self):
        # This function will extract the maximum value, and rearrange the heap accordingly.
        if self.__mCount == 0:
            print("Heap is empty, no Key had been extracted!")
        elif self.__mCount == 3:
            # if there are 2 childrens, i need to decide which one of the child's should replace the root.
            maxchildren = self.maxChild(1)
            swap(self.__mList,maxchildren,self.__mCount)
            swap(self.__mList,1,self.__mCount)
            print(self.__mList[self.__mCount])
            self.__mCount -= 1
            self.__mList = self.__mList[:-1]
            self.heapify(1)
        elif self.__mCount > 4:
            # if there are grandchildrens i need to decide which one of the grandchilds should replace the root.
            maxgrandchildren = self.maxGrandChildren(1)
            swap(self.__mList,maxgrandchildren,self.__mCount)
            swap(self.__mList,1,self.__mCount)
            print(self.__mList[self.__mCount])
            self.__mCount -=1
            self.__mList = self.__mList[:-1]
            self.heapify(1)
            # if there is only one child.
        else:
            swap(self.__mList,1,self.__mCount)
            print (self.__mList[self.__mCount])
            self.__mCount -= 1
            self.__mList = self.__mList[:-1]
            self.heapify(1)

    def extract_min(self):
        # This function will extract the minimum value, and rearrange the heap accordingly.
        if self.hasChildren(1):
            # the root wont be the minimum if he has children's, so i determine the min child, swapping him to the last
            # index, extracting the node and heapifying the heap.
            if self.__mCount == 5:
                # if there are 2 grandchildrens i need to decide which one of the childs should replace the smallest.
                minchild = self.smallestChild(self.getLeftChild(1))
                swap(self.__mList,minchild,self.__mCount)
                swap(self.__mList,self.getLeftChild(1),self.__mCount)
                print(self.__mList[self.__mCount])
                self.__mCount -= 1
                self.__mList = self.__mList[:-1]
                self.heapify(self.getLeftChild(1))
            else:
                minvalue = self.smallestChild(1)
                swap(self.__mList,minvalue,self.__mCount)
                print (self.__mList[self.__mCount])
                self.__mCount -= 1
                self.__mList = self.__mList[:-1]
                self.heapify(minvalue)
        elif self.__mCount == 2:
            # if there is only one child, i will return the child value.
            print(self.__mList[self.getLeftChild(1)])
            self.__mCount -= 1
            self.__mList = self.__mList[:-1]
        elif self.__mCount == 1:
            # if only the root remains, i will return the root.
            print (self.__mList[1])
            self.__mCount -= 1
            self.__mList = self.__mList[:-1]
        else:
            print("Heap is empty, no Key had been extracted!")

    def remove(self, i):
        # This function remove the node at index i, and rearrange the heap accordingly.
        if i == 0:
            print("The first index is starting at 1")
        elif i > self.__mCount:
            print("The index you inserted is not in the Heap range.")
        else:
            # swapping the index with the last node.
            swap(self.__mList,i,self.__mCount)
            print("Removing the Key from the index you have inserted : %d, and re-arranging the heap" % self.__mList[self.__mCount])
            self.__mCount -= 1
            self.__mList = self.__mList[:-1]
            self.heapify(i)


    def hasLeftChild(self, i):
        # This function will return if the node at index i has left child
        return (2 * i) <= self.__mCount

    def hasRightChild(self, i):
        # This function will return if the node at index i has right child
        return ((2 * i) + 1) <= self.__mCount

    def getLeftChild(self, i):
        # This function will return the node left child value
        return (2 * i)

    def getRightChild(self, i):
        # This function will return the node right child value
        return (2 * i) + 1

    def hasChildren(self, i):
        # This function will return if the node has one or more children's.
        if (2 * i) < self.__mCount or (2 * i) + 1 < self.__mCount:
            return True
        else:
            return False

    def hasParent(self, i):
        # This function will return if the node has parent.
        if self.getParent(i) != 0:
            return True
        else:
            return False

    def getParent(self, i):
        # This function will return the node parent value
        return i // 2

    def getGrandParent(self, i):
        # This function will return the node grandparent value
        return self.getParent(i // 2)

    def hasGrandParent(self, i):
        # This function will return if the node has grandparent.
        if self.getParent(self.getParent(i)) != 0:
            return True
        else:
            return False

    def maxGrandChildren(self, i):
        # in this function i have to determine who is the max grandchildren, in order to do that and to not get any
        # errors for trying to reach index which doesn't exist, there are many conditions to consider.
        if self.hasChildren(self.getLeftChild(i)) and self.hasChildren(self.getRightChild(i)):
            maxleftgrandchild = self.maxChild(self.getLeftChild(i))
            maxrightgrandchild = self.maxChild(self.getRightChild(i))
            if self.__mList[maxleftgrandchild] >= self.__mList[maxrightgrandchild]:
                # if the left max grandchild is bigger then the right maxgrandchild.
                maxgrandchild = maxleftgrandchild
            else:
                maxgrandchild = maxrightgrandchild
            return maxgrandchild

        elif self.getLeftChild(self.hasRightChild(i)) is False:
            # if there is only one grandchild.
            maxgrandchild = self.getLeftChild(self.getLeftChild(i))
            return maxgrandchild

        elif self.hasRightChild(self.getRightChild(i)) is False:
            # if there are 3 grand childs.
            maxleftgrandchild = self.maxChild(self.getLeftChild(i))
            maxrightgrandchild = self.getRightChild(self.getLeftChild(i))
            if self.__mList[maxleftgrandchild] >= self.__mList[maxrightgrandchild]:
                maxgrandchild = maxleftgrandchild
            else:
                maxgrandchild = maxrightgrandchild
            return maxgrandchild

        elif self.hasChildren(self.getRightChild(i)) is False:
            # if there are 2 grandchilds.
            if self.hasRightChild(self.getLeftChild(i)) is False:
                maxgrandchild = self.getLeftChild(self.getLeftChild(i))
            else:
                maxgrandchild = self.maxChild(self.getLeftChild(i))
            return maxgrandchild

    def minGrandChildren(self, i):
        # in this function i have to determine who is the min grandchildren, in order to do that and to not get any
        # errors for trying to reach index which doesn't exist, there are many conditions to consider.
        if self.hasChildren(self.getLeftChild(i)) and self.hasChildren(self.getRightChild(i)):
            # if there are 4 grandchilds.
            minleftgrandchild = self.smallestChild(self.getLeftChild(i))
            minrightgrandchild = self.smallestChild(self.getRightChild(i))
            if self.__mList[minleftgrandchild] <= self.__mList[minrightgrandchild]:
                mingrandchild = minleftgrandchild
            else:
                mingrandchild = minrightgrandchild
            return mingrandchild

        elif self.getLeftChild(self.hasRightChild(i)) is False:
            # if there is one grandchild.
            mingrandchild = self.getLeftChild(self.getLeftChild(i))
            return mingrandchild

        elif self.hasRightChild(self.getRightChild(i)) is False:
            # if there are three grandchilds.
            minleftgrandchild = self.smallestChild(self.getLeftChild(i))
            minrightgrandchild = self.getRightChild(self.getLeftChild(i))
            if self.__mList[minleftgrandchild] <= self.__mList[minrightgrandchild]:
                mingrandchild = minleftgrandchild
            else:
                mingrandchild = minrightgrandchild
            return mingrandchild

        elif self.hasChildren(self.getRightChild(i)) is False:
            # if there are two grandchilds.
            if self.hasRightChild(self.getLeftChild(i)) is False:
                mingrandchild = self.getLeftChild(self.getLeftChild(i))
            else:
                mingrandchild = self.smallestChild(self.getLeftChild(i))
            return mingrandchild


    def maxChildAndGrandChild(self, i):
        # This function will return the max value between the child's and grandchild's of the node.
        maxchildren = self.maxChild(i)
        maxgrandchild = self.maxGrandChildren(i)
        # Getting the value of the max child and grandchild.
        if self.__mList[maxchildren] >= self.__mList[maxgrandchild]:
            return maxchildren
        else:
            return maxgrandchild

    def minChildAndGrandChild(self, i):
        # This function will return the min value between the child's and grandchild's of the node.
        minChildren = self.smallestChild(i)
        minGrandChild = self.minGrandChildren(i)
        # Getting the value of the max child and grandchild.
        if self.__mList[minChildren] <= self.__mList[minGrandChild]:
            return minChildren
        else:
            return minGrandChild

    def smallestChild(self, i):
        # function which returns the smallest child.
        if self.__mList[self.getLeftChild(i)] < self.__mList[self.getRightChild(i)]:
            minChild = self.getLeftChild(i)
        else:
            minChild = self.getRightChild(i)
        return minChild

    def maxChild(self, i):
        # function which returns the maximum child.
        if self.__mList[self.getLeftChild(i)] > self.__mList[self.getRightChild(i)]:
            maxChild = self.getLeftChild(i)
        else:
            maxChild = self.getRightChild(i)
        return maxChild

    def hasGrandChild(self, i):
        # function which returns if a node at index i has grandchildrens.
        if self.hasChildren(i * 2) or self.hasChildren((i * 2) + 1):
            return True
        else:
            return False

    def isGrandChild(self, i, key):
        # function which returns if a node at index i has grandchild with key value.
        if self.getLeftChild(self.getLeftChild(i)) == key:
            return True
        elif self.getLeftChild(self.getRightChild(i)) == key:
            return True
        elif self.getRightChild(self.getLeftChild(i)) == key:
            return True
        elif self.getRightChild(self.getRightChild(i)) == key:
            return True
        else:
            return False

    def getLength(self):
        # function which returns the length of the heap.
        return self.__mCount

if __name__ == "__main__":
    try:
        # Initializing the heap.
        heap = MaxMinHeap()

        def keyboardBuildHeap(heap):
            # This function will Build the heap based on user keyboard input.
            print("Enter numbers to add to your Heap, Please seperate each number instance by pressing Enter.\notherwise, Error will be presented.\nPress X to Finish")
            num = input()
            while (num != 'X'):
                heap.insert(int(num))
                num = input()

        def fileBuildHeap(heap,filename):
            # This function will Build the heap based on user text file input.
           try:
               with open(filename, "r") as f:
                    for line in f:
                        for num in line.split(" "):
                            heap.insert(int(num))
           except:
                print("\nAn exception occurred - The program couldn't find the inserted file name.")
                print("\nPlease make sure you insert the correct file name and extension.")
                print("\nYou are more than welcome to run the program again.\n")
                exit(1)




        def welcomeMenu():
            # This function represents the welcome menu which is displayed to the user.
            while True:
                print("**" * 50)
                print("Maman13 Assignment\nWelcome My MaxMinHeap Program! Please follow the menu instructions.")
                print("**" * 50)
                print("  ____           _     _   _                   _   _ ")
                print(" / ___|   __ _  | |   | \ | |   __ _    __ _  | | (_)")
                print("| |  _   / _` | | |   |  \| |  / _` |  / _` | | | | |")
                print("| |_| | | (_| | | |   | |\  | | (_| | | (_| | | | | |")
                print(" \____|  \__,_| |_|   |_| \_|  \__,_|  \__, | |_| |_|")
                print("                                       |___/         ")
                print("**" * 50)
                print(
                    "Welcome Menu - after you will build your MaxMin Heap, you will be introduced into the main Heap Menu.")
                print("**" * 50)
                print("Option 1 : Exit the program")
                print("Option 2 : Build MaxMin Heap with Keyboard Input")
                print("Option 3 : Build MaxMin Heap with a text file")

                choice = input("Please Choose One Option: ")

                if choice == "1":
                    print("\nTerminating the program\nSee you next time!\n")
                    exit()
                elif choice == "2":
                    print("\nBuilding the MaxMin Heap\n")
                    keyboardBuildHeap(heap)
                    heap.buildHeap()
                    heapMenu()
                elif choice == "3":
                    print("\nPlease enter the name of the text file you would like to use\n")
                    filename = input()
                    fileBuildHeap(heap,filename)
                    heap.buildHeap()
                    heapMenu()
                else:
                    print("\nYou didn't choose a valid option number.\n")


        def heapMenu():
            # This function represents the heap menu which is displayed to the user after the heap was assembled.
            while True:
                print("**" * 50)
                print("Welcome to the Main Heap Menu, Please follow the menu instructions")
                print("**" * 50)
                print("Option 1 : Exit the program")
                print("Option 2 : Extract the Maximum from the MaxMin Heap")
                print("Option 3 : Extract the Minimum from the MaxMin Heap")
                print("Option 4 : Insert key into the MaxMin Heap")
                print("Option 5 : Delete key from the MaxMin Heap")
                print("Option 6 : Sort the MaxMin Heap")
                print("Option 7 : Print the MaxMin Heap")


                choice = input("Please Choose One Option: ")

                if choice == "1":
                    print("Terminating the program\nSee you next time!\n")
                    exit()
                elif choice == "2":
                    print("\nExtracting the Maximum Key")
                    print("\nThe Maximum key which had been extracted is:")
                    heap.extract_max()
                elif choice == "3":
                    print("\nExtracting the Minimum Key")
                    print("\nThe Minimum key which had been extracted is:")
                    heap.extract_min()
                elif choice == "4":
                    print("\nEnter Key Value to be Inserted\n")
                    heap.insert(int(input()))
                elif choice == "5":
                    print("\nEnter index you wish to be removed from the heap.\n")
                    heap.remove(int(input()))
                elif choice == "6":
                    print("\nSorting the array with maxminheap sort.\nI will rebuild the heap after the procudure.\n")
                    heap.heapsort()
                elif choice == "7":
                    print("\nPrinting the Heap\n")
                    heap.printHeap()
                else:
                    print("\nYou didn't choose a valid option number.\n")


        welcomeMenu()
        heapMenu()

    except KeyboardInterrupt:
        print("\nSad to see you go by KeyBoardInterruption, you should press 1 next time.\nHope to see you back soon.")