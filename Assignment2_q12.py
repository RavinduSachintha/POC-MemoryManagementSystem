# Python version 3.5

import sys

# Memory Block class defining
class MemBlock:
    def __init__(self):
        self.stAddress = None
        self.enAddress = None
        self.proID = None
        self.hole = True
        self.next = None

    def viewBlock(self):
        ID = self.proID
        if self.hole:
            free = "Free"
        else:
            free = "Used"
        size = self.enAddress-self.stAddress+1
        print(ID," ",free," ",size,"k")

# Linked List class defining
class LinkedList:
    
    def __init__(self):
        os_memory = 400
        user_proccess = 2560

        sysBlock = MemBlock()
        sysBlock.stAddress = 1
        sysBlock.enAddress = os_memory
        sysBlock.proID = "OS"
        sysBlock.hole = False

        freeBlock = MemBlock()
        freeBlock.stAddress = os_memory + 1
        freeBlock.enAddress = user_proccess
        freeBlock.proID = "FR"
        freeBlock.hole = True

        self.head = sysBlock
        sysBlock.next = freeBlock
        self.blockCount = 2

    # return a free block
    def checkSpace(self,size):
        sblock = self.head
        while sblock != None:
            if sblock.hole:
                curSize = sblock.enAddress - sblock.stAddress + 1
                if curSize >= size:
                    return sblock
                    break
            sblock = sblock.next

    # return before proccess to the checked proccess
    def checkProccess(self,proID):
        sblock = self.head
        while sblock.next != None:
            if sblock.next.proID==proID:
                return sblock
                break
            sblock = sblock.next

    # print all data in memory
    def snapshot(self):
        sblock = self.head
        print("----------------------------")
        while sblock != None:
            sblock.viewBlock()
            sblock = sblock.next
        print("----------------------------")

# main program
memory = LinkedList()

def allocate(proID,size):
    if not memory.checkSpace(size)==None:
        sblock = memory.checkSpace(size)
        curSize = sblock.enAddress - sblock.stAddress + 1

        # free block size equal to new proccess size
        if curSize == size:
            sblock.proID = proID
            sblock.hole = False

        # free block size bigger than to new proccess size
        else:
            nba = sblock.enAddress # for new block enAddress

            sblock.enAddress = sblock.stAddress + size - 1
            sblock.proID = proID
            sblock.hole = False
            
            newBlock = MemBlock()
            newBlock.stAddress = sblock.enAddress + 1
            newBlock.enAddress  = nba
            newBlock.proID = "FR"
            newBlock.hole = True

            newBlock.next = sblock.next
            sblock.next = newBlock
    else:
        print("There is no free space for this proccess.")

def terminate(proID):
    if not memory.checkProccess(proID)==None:
        sblock = memory.checkProccess(proID) #sblock.next is the checked proccess

        # when both side not free    
        if not (sblock.hole or sblock.next.next.hole):
            sblock.next.proID = "FR"
            sblock.next.hole = True

        # when back free and front not free 
        elif (sblock.hole and not sblock.next.next.hole):
            sblock.enAddress = sblock.next.enAddress
            sblock.next = sblock.next.next

        # when back not free and front free    
        elif (not sblock.hole and sblock.next.next.hole):
            sblock.next.next.stAddress = sblock.next.stAddress
            sblock.next = sblock.next.next

        # when both side free
        elif (sblock.hole and sblock.next.next.hole):
            sblock.enAddress = sblock.next.next.enAddress
            sblock.next = sblock.next.next.next
            
    else:
        print("The proccess you entered is not in the memory.")

def inputData():
    action = input("\nEnter your option : ")
    if action == 'a':
        proID = input("Enter the Proccess ID : ")
        size = int(input("Enter the Size of the Proccess : "))
        allocate(proID,size)
        memory.snapshot()
        inputData()
    
    elif action == 't':
        proID = input("Enter the Proccess ID : ")
        terminate(proID)
        memory.snapshot()
        inputData()

    elif action == ':q':
        print("Thank You.")
        sys.exit(0)
        
    else:
        print("Your input not identified.")
        inputData()
        
# interface

print("\n########################################################################")
print("########      Memory Management System in Computer Memory      #########")
print("########################################################################\n")


print("Type 'a' for allocating a proccess to the memory.")
print("Type 't' for terminating a proccess from the memory.")
print("Type ':q' for quiting from the system.")

inputData()





