import numpy as np
from time import time
import random
from node import node

class puzzle:
    def __init__(self, initializedRootNode = None):
        self.__rootNode = initializedRootNode
        self.__nodeSolution = None
        self.__priorityQueueOfNode = []
        self.__kurangValues = {}
        self.__kurangTotalPlusX = 0
        self.__totalNodes = 1
        self.__executionTime = None

    @classmethod
    def initializePuzzle(cls, pathFile = None):
        matrix = np.array([ [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None]])

        if (not pathFile):
            elmtList = random.sample(range(1, 17), 16)
            for row in range(node.TotalRow):
                for col in range(node.TotalCol):
                    matrix[row][col] = elmtList.pop(0)
            
        else:
            file = open(pathFile, 'r')
            row = 0
            for rowElmts in file:
                matrix[row] = [int(elmt) for elmt in rowElmts.split()]
                row += 1

        rootNode = node.create(matrix)
        return cls(rootNode)

    def solve(self):
        startTime = time()
        
        self.__calculateKurangValues()
        if (self.__kurangTotalPlusX % 2 == 0):
            self.__enqueueNode(self.__rootNode)

            isPuzzleSolved = False         
            while (not isPuzzleSolved):
                processedNode = self.__dequeueNode()
                if (processedNode.isGoal()):
                    isPuzzleSolved = True
                    self.__nodeSolution = processedNode

                else:
                    self.__generateChildNodes(processedNode)
        
        self.__executionTime = time() - startTime

    def __calculateKurangValues(self):
        # For each cell in matrix of rootNode, calculate how many cells which are lesser in value but greater in position 
        # than cell being processed 

        # If a processed cell is at 0 <= row <= 1, substracts the cell's value with total of cells 
        # which the value and the position is lesser than the cell being processed

        # else if the cell is at 2 <= row <= 3, count the total cells 
        # which the value is lesser but the position is greater than cell being processed

        # sum of kurang function and value of X will be calculated as well
        for row in range(node.TotalRow):
            for col in range(node.TotalCol):
                val = self.__rootNode.at(row, col)
                if (row <= 1):
                    kurangCounter = self.__rootNode.at(row, col) - 1

                    for rowToCheck in range (row + 1):
                        lastCol = col*(1-row+rowToCheck) + 4*(row-rowToCheck)
                        for colToCheck in range (lastCol):
                            valToCheck = self.__rootNode.at(rowToCheck, colToCheck)
                            if (valToCheck < val):
                                kurangCounter -= 1
                                
                    self.__kurangValues[val] = kurangCounter
                    self.__kurangTotalPlusX += kurangCounter

                elif (row > 1):
                    kurangCounter = 0

                    startRow = row + (int)(col/3)
                    startCol = (col + 1) % 4
                    rowIterateCounter = 0
                    for rowToCheck in range (startRow, node.TotalRow):
                        startCol *= (1 - rowIterateCounter)  
                        for colToCheck in range (startCol, node.TotalCol):
                            valToCheck = self.__rootNode.at(rowToCheck, colToCheck)
                            if (valToCheck < val):
                                kurangCounter += 1
                        rowIterateCounter += 1

                    self.__kurangValues[val] = kurangCounter
                    self.__kurangTotalPlusX += kurangCounter
            
        if (self.__rootNode.getBlank("row") % 2 == 0 and 
            self.__rootNode.getBlank("col") % 2 == 1
            or
            self.__rootNode.getBlank("row") % 2 == 1 and 
            self.__rootNode.getBlank("col") % 2 == 0):
            
            self.__kurangTotalPlusX += 1

    def __generateChildNodes(self, parentNode):
        moveDirection = ["RIGHT", "DOWN", "LEFT", "UP"]
        for direction in moveDirection:
            childNode = node.move(parentNode, direction)
            if (childNode.isValid()):
                self.__enqueueNode(childNode)
                self.__totalNodes += 1

    def __enqueueNode(self, node):
        idx = 0
        isNodeCostLesser = False
        for queuedNode in self.__priorityQueueOfNode:
            if (node.getCost() < queuedNode.getCost()):
                isNodeCostLesser = True
                break
            idx += 1

        if (isNodeCostLesser):
            self.__priorityQueueOfNode.insert(idx, node)
        else:
            self.__priorityQueueOfNode.append(node)

    def __dequeueNode(self):
        if (self.__priorityQueueOfNode):
            return self.__priorityQueueOfNode.pop(0)


    # Below are getter methods used by main

    def isSolved(self):
        return self.__nodeSolution != None

    def getTotalGeneratedNodes(self):
        return self.__totalNodes

    def getTotalOfKurangPlusX(self):
        return self.__kurangTotalPlusX
        
    def getTimeTaken(self):
        return self.__executionTime

    def printPuzzle(self):
        self.__rootNode.printNode()
        print()

    def printSolution(self):
        solutionBranches = []
        solution = self.__nodeSolution
        while (solution):
            solutionBranches.insert(0, solution)
            solution = solution.getParentNode()
        
        for node in solutionBranches:
            node.printNode(); print()

    def printKurangValues(self):
        for i in range (1, 17):
            if (i < 16):
                print("Kurang{:4} = {}".format('(' + str(i) + ')', self.__kurangValues[i]))
            else:
                print("Kurang{:4} = {} -> Optional (as blank value)".format('(' + str(i) + ')', self.__kurangValues[i]))
        print()


