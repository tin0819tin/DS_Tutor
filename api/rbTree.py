from flask import Flask, jsonify, session, Blueprint
from flask_cors import CORS
from datetime import timedelta
import os, json
import math
import random


# -----------------------------------------------------------
# Define some static variables
# -----------------------------------------------------------
FIRST_PRINT_POS_X = 50
PRINT_VERTICAL_GAP = 20
PRINT_HORIZONTAL_GAP = 50


FOREGROUND_RED = "#AA0000"
BACKGROUND_RED = "#FFAAAA"

FOREGROUND_BLACK =  "#000000"
BACKGROUND_BLACK = "#AAAAAA"
BACKGROUND_DOUBLE_BLACK = "#777777"

HIGHLIGHT_LABEL_COLOR = "#FF0000"
HIGHLIGHT_LINK_COLOR = "#FF0000"

BLUE = "#0000FF"

LINK_COLOR = "#000000"
BACKGROUND_COLOR = BACKGROUND_BLACK
HIGHLIGHT_COLOR = "#007700"
FOREGROUND_COLOR = FOREGROUND_BLACK
PRINT_COLOR = FOREGROUND_COLOR

widthDelta  = 50
heightDelta = 50
startingY = 50


FIRST_PRINT_POS_X  = 40
PRINT_VERTICAL_GAP  = 20
PRINT_HORIZONTAL_GAP = 50
EXPLANITORY_TEXT_X = 10
EXPLANITORY_TEXT_Y = 10

# -----------------------------------------------------------
# Define utility function
# -----------------------------------------------------------
AnimationCommands = []

def addCmd(command, *args, sep='<;>'):
    AnimationCommands.append(command + sep + sep.join(map(str, args))) 

def clearCmd():
    AnimationCommands.clear()

def normalizeInput(value):
    pass

# -----------------------------------------------------------
# RBTree node
# -----------------------------------------------------------
class RBNode():

    def __init__(self, key, id, initialX, initialY):
        self.value = key
        self.graphicID = id
        self.x = initialX
        self.y = initialY
        self.blackLevel = 0
        self.phantomLeaf = False
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

        # For tree root in resize tree
        self.leftWidth = widthDelta//2
        self.rightWidth = widthDelta//2

    def isLeftChild(self):
        if self.parent == None:
            return False
        return self.parent.left == self

# -----------------------------------------------------------
# Define RBTree class
# -----------------------------------------------------------
class RBTree():
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.treeRoot = None
        self.nextIndex = 1
        self.startingX = w / 2
        self.print_max  = w - PRINT_HORIZONTAL_GAP
        self.first_print_pos_y  = h - 2 * PRINT_VERTICAL_GAP
        addCmd("CreateLabel", 0, "", EXPLANITORY_TEXT_X, EXPLANITORY_TEXT_Y, 0)
        self.first = True
        self.oper_list = []
        self.build_list = []
    
    def reset(self):
        clearCmd()
        self.treeRoot = None
        self.nextIndex = 1
        self.startingX = self.w / 2
        self.print_max  = self.w - PRINT_HORIZONTAL_GAP
        self.first_print_pos_y  = self.h - 2 * PRINT_VERTICAL_GAP
        addCmd("CreateLabel", 0, "", EXPLANITORY_TEXT_X, EXPLANITORY_TEXT_Y, 0)
        self.first = True
        self.oper_list = []
        self.build_list = []

    # Add any utility function if needed e.g. FindUncle, FindBlackLevel, SingleRotation etc.
    def insert(self, value, build=False):
        if value == "":
            return
        if not (self.first or build):
            clearCmd()
        self.first = False
        addCmd("SetText", 0, " Inserting "+value)
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        if self.treeRoot == None:
            treeNodeID = self.nextIndex
            self.nextIndex += 1
            addCmd("CreateCircle", treeNodeID, value,  self.startingX, startingY)
            addCmd("SetForegroundColor", treeNodeID, FOREGROUND_BLACK)
            addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_BLACK)
            self.treeRoot = RBNode(value, treeNodeID, self.startingX, startingY)
            self.treeRoot.blackLevel = 1
            
            self.attachNullLeaves(self.treeRoot)
            self.resizeTree()
        else:
            treeNodeID = self.nextIndex
            self.nextIndex += 1
            
            addCmd("CreateCircle", treeNodeID, value, 30, startingY)
            addCmd("SetForegroundColor", treeNodeID, FOREGROUND_RED)
            addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_RED)
            addCmd("Step")
            insertElem = RBNode(value, treeNodeID, 100, 100)
            
            addCmd("SetHighlight", insertElem.graphicID, 1)
            insertElem.height = 1
            self.insert_recursive(insertElem, self.treeRoot)
            # resizeTree();				
        
        addCmd("SetText", 0, " ");

        ##for debug##
        # if not build:
        #     print("insert:")
        #     for x in AnimationCommands:
        #         print(x)	
        #####################################		
        return
        
    def find(self, value):
        clearCmd()
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        self.findRecursive(self.treeRoot, value)
        return

    def delete(self, value, build=False):
        if value == "":
            return
        if not (self.first or build):
            clearCmd()
        self.first = False
        addCmd("SetText", 0, "Deleting "+value)
        addCmd("Step")
        addCmd("SetText", 0, " ")
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        self.treeDelete(self.treeRoot, value)
        addCmd("SetText", 0, " ");	
        return 

    def print(self):
        self.build(steps=10, Random=True)
        # clearCmd()
        # if self.treeRoot != None:
        #     self.highlightID = self.nextIndex
        #     self.nextIndex += 1
        #     firstLabel = self.nextIndex
        #     addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, self.treeRoot.x, self.treeRoot.y)
        #     self.xPosOfNextLabel = FIRST_PRINT_POS_X
        #     self.yPosOfNextLabel = self.first_print_pos_y
        #     self.printTreeRecursive(self.treeRoot)
        #     addCmd("Delete",self.highlightID)
        #     addCmd("Step")
        #     for i in range(firstLabel, self.nextIndex):
        #         addCmd("Delete", i)
        #     self.nextIndex = self.highlightID  # Reuse objects.  Not necessary.
        return
    
    def build(self, steps, Random):
        self.reset()
        operation = ['insert', 'delete']
        self.oper_list = ['insert'] * 3
        if Random:
            self.build_list = []
            self.oper_list += random.choices(operation, weights = [4, 1], k = 40)
        current_stpes = 0
        for oper in self.oper_list:
            if oper == 'insert':
                insert_value = str(random.randrange(999))
                self.build_list.append(insert_value)
                self.insert(insert_value, build=True)
                current_stpes += 1

            elif oper == 'delete' and self.treeRoot != None:
                delete_value = random.choice(self.build_list)
                self.build_list.remove(delete_value)
                self.delete(delete_value, build=True)
                current_stpes += 1

            if current_stpes >= steps:
                break
        pass
    # utility functions

    def printTreeRecursive(self, tree):
        addCmd("Step")
        if tree.left != None and not tree.left.phantomLeaf:
            addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
            self.printTreeRecursive(tree.left)
            addCmd("Move", self.highlightID, tree.x, tree.y)
            addCmd("Step")
        
        nextLabelID = self.nextIndex
        self.nextIndex += 1
        addCmd("CreateLabel", nextLabelID, tree.value, tree.x, tree.y)
        addCmd("SetForegroundColor", nextLabelID, PRINT_COLOR)
        addCmd("Move", nextLabelID, self.xPosOfNextLabel, self.yPosOfNextLabel)
        addCmd("Step")
        
        self.xPosOfNextLabel +=  PRINT_HORIZONTAL_GAP
        if self.xPosOfNextLabel > self.print_max:
            self.xPosOfNextLabel = FIRST_PRINT_POS_X
            self.yPosOfNextLabel += PRINT_VERTICAL_GAP
            
        if tree.right != None and not tree.right.phantomLeaf:
            addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
            self.printTreeRecursive(tree.right)
            addCmd("Move", self.highlightID, tree.x, tree.y);
            addCmd("Step")

        return

    def findRecursive(self, tree, value):
        addCmd("SetText", 0, "Searchiing for "+value)
        if tree != None and not tree.phantomLeaf:
            addCmd("SetHighlight", tree.graphicID, 1)
            if (tree.value == value):
                addCmd("SetText", 0, "Searching for "+value+" : " + value + " = " + value + " (Element found!)")
                addCmd("Step")
                addCmd("SetText", 0, "Found:"+value)
                addCmd("SetHighlight", tree.graphicID, 0)
            else:
                if float(tree.value) > float(value):
                    addCmd("SetText", 0, "Searching for "+value+" : " + value + " < " + tree.value + " (look to left subtree)")
                    addCmd("Step")
                    addCmd("SetHighlight", tree.graphicID, 0)
                    if tree.left != None:
                        addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                        addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                        addCmd("Step")
                        addCmd("Delete", self.highlightID)
                    self.findRecursive(tree.left, value)
                else:
                    addCmd("SetText", 0, " Searching for "+value+" : " + value + " > " + tree.value + " (look to right subtree)")			
                    addCmd("Step")
                    addCmd("SetHighlight", tree.graphicID, 0)
                    if tree.right != None:
                        addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                        addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                        addCmd("Step")
                        addCmd("Delete", self.highlightID)
                    self.findRecursive(tree.right, value)
        else:
            addCmd("SetText", 0, " Searching for "+value+" : " + "< Empty Tree > (Element not found)")
            addCmd("Step")
            addCmd("SetText", 0, " Searching for "+value+" : " + " (Element not found)")

    def attachNullLeaves(self, node):
        self.attachLeftNullLeaf(node);
        self.attachRightNullLeaf(node);
    
    def attachLeftNullLeaf(self, node):     # Add phantom left leaf
        treeNodeID = self.nextIndex
        self.nextIndex += 1
        addCmd("CreateCircle", treeNodeID, "NULL\nLEAF",  node.x, node.y)
        addCmd("SetForegroundColor", treeNodeID, FOREGROUND_BLACK)
        addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_BLACK)
        node.left = RBNode("", treeNodeID, self.startingX, startingY)
        node.left.phantomLeaf = True
        addCmd("SetLayer", treeNodeID, 1)
        node.left.blackLevel = 1
        addCmd("Connect",node.graphicID, treeNodeID, LINK_COLOR)

    def attachRightNullLeaf(self, node):    # Add phantom right leaf
        treeNodeID = self.nextIndex
        self.nextIndex += 1
        addCmd("CreateCircle", treeNodeID, "NULL\nLEAF",  node.x, node.y)
        addCmd("SetForegroundColor", treeNodeID, FOREGROUND_BLACK)
        addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_BLACK)
        node.right = RBNode("", treeNodeID, self.startingX, startingY)
        addCmd("SetLayer", treeNodeID, 1)
        node.right.phantomLeaf = True
        node.right.blackLevel = 1
        addCmd("Connect", node.graphicID, treeNodeID, LINK_COLOR)
        
    def resizeTree(self):
        startingPoint  = self.startingX
        self.resizeWidths(self.treeRoot)
        if self.treeRoot != None:
            if self.treeRoot.leftWidth > startingPoint:
                startingPoint = self.treeRoot.leftWidth
            elif self.treeRoot.rightWidth > startingPoint:
                startingPoint = max(self.treeRoot.leftWidth, 2 * startingPoint - self.treeRoot.rightWidth)
            self.setNewPositions(self.treeRoot, startingPoint, startingY, 0);
            self.animateNewPositions(self.treeRoot)
            addCmd("Step")

    def resizeWidths(self, tree):
        if tree == None:
            return 0
        tree.leftWidth = max(self.resizeWidths(tree.left), widthDelta / 2)
        tree.rightWidth = max(self.resizeWidths(tree.right), widthDelta / 2)
        return tree.leftWidth + tree.rightWidth

    def setNewPositions(self, tree, xPosition, yPosition, side):
        if tree != None:
            tree.y = yPosition
            if side == -1:
                xPosition = xPosition - tree.rightWidth
                tree.heightLabelX = xPosition - 20
            elif side == 1:
                xPosition = xPosition + tree.leftWidth
                tree.heightLabelX = xPosition + 20
            else:
                tree.heightLabelX = xPosition - 20
            tree.x = xPosition;
            tree.heightLabelY = tree.y - 20
            self.setNewPositions(tree.left, xPosition, yPosition + heightDelta, -1)
            self.setNewPositions(tree.right, xPosition, yPosition + heightDelta, 1)

    def animateNewPositions(self, tree):
        if tree != None:
            addCmd("Move", tree.graphicID, tree.x, tree.y)
            self.animateNewPositions(tree.left)
            self.animateNewPositions(tree.right)

    def insert_recursive(self, elem, tree):
        addCmd("SetHighlight", tree.graphicID, 1)
        addCmd("SetHighlight", elem.graphicID, 1)

        if (float(elem.value) < float(tree.value)):
            addCmd("SetText", 0, elem.value + " < " + tree.value + ".  Looking at left subtree")
        else:
            addCmd("SetText",  0, elem.value + " >= " + tree.value + ".  Looking at right subtree")		

        addCmd("Step")
        addCmd("SetHighlight", tree.graphicID , 0)
        addCmd("SetHighlight", elem.graphicID, 0)

        if float(elem.value) < float(tree.value):
            if tree.left == None or tree.left.phantomLeaf:
                addCmd("SetText", 0, "Found null tree (or phantom leaf), inserting element")

                if tree.left != None:
                    addCmd("Delete", tree.left.graphicID)

                addCmd("SetHighlight", elem.graphicID, 0)
                tree.left=elem
                elem.parent = tree
                addCmd("Connect", tree.graphicID, elem.graphicID, LINK_COLOR)
                self.attachNullLeaves(elem)
                self.resizeTree()   # resize twice in RedBlack.js
                self.fixDoubleRed(elem)
            else:
                addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                addCmd("Step")
                addCmd("Delete", self.highlightID)
                self.insert_recursive(elem, tree.left)
        else:
            if tree.right == None  or tree.right.phantomLeaf:
                addCmd("SetText",  0, "Found null tree (or phantom leaf), inserting element")
                if tree.right != None:
                    addCmd("Delete", tree.right.graphicID)
                
                addCmd("SetHighlight", elem.graphicID, 0)
                tree.right=elem
                elem.parent = tree
                addCmd("Connect", tree.graphicID, elem.graphicID, LINK_COLOR)
                elem.x = tree.x + widthDelta/2
                elem.y = tree.y + heightDelta
                addCmd("Move", elem.graphicID, elem.x, elem.y)
                
                self.attachNullLeaves(elem)
                self.resizeTree()
            
                self.resizeTree()
                self.fixDoubleRed(elem)
            else:
                addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                addCmd("Step")
                addCmd("Delete", self.highlightID)
                self.insert_recursive(elem, tree.right)

    def fixDoubleRed(self, tree):
        if tree.parent != None:

            if tree.parent.blackLevel > 0:
                return

            if tree.parent.parent == None:
                addCmd("SetText", 0, "Tree root is red, color it black.")
                addCmd("Step")
                tree.parent.blackLevel = 1
                addCmd("SetForegroundColor", tree.parent.graphicID, FOREGROUND_BLACK)
                addCmd("SetBackgroundColor", tree.parent.graphicID, BACKGROUND_BLACK)
                return

            uncle = self.findUncle(tree);
            # print(uncle)
            if self.blackLevel(uncle) == 0:
                addCmd("SetText", 0, "Node and parent are both red.  Uncle of node is red -- push blackness down from grandparent")
                addCmd("Step")
                
                addCmd("SetForegroundColor", uncle.graphicID, FOREGROUND_BLACK)
                addCmd("SetBackgroundColor",uncle.graphicID, BACKGROUND_BLACK)
                uncle.blackLevel = 1
                
                tree.parent.blackLevel = 1
                addCmd("SetForegroundColor", tree.parent.graphicID, FOREGROUND_BLACK)
                addCmd("SetBackgroundColor",tree.parent.graphicID, BACKGROUND_BLACK)
                
                tree.parent.parent.blackLevel = 0
                addCmd("SetForegroundColor", tree.parent.parent.graphicID, FOREGROUND_RED)
                addCmd("SetBackgroundColor",tree.parent.parent.graphicID, BACKGROUND_RED)
                addCmd("Step")
                self.fixDoubleRed(tree.parent.parent)
            else:
                if tree.isLeftChild() and  not tree.parent.isLeftChild():
                    addCmd("SetText", 0, "Node and parent are both red.  Node is left child, parent is right child -- rotate")
                    addCmd("Step")
                    
                    self.singleRotateRight(tree.parent)
                    tree=tree.right
                elif not tree.isLeftChild() and tree.parent.isLeftChild():
                    addCmd("SetText", 0, "Node and parent are both red.  Node is right child, parent is left child -- rotate")
                    addCmd("Step")
                    
                    self.singleRotateLeft(tree.parent)
                    tree = tree.left
                
                if tree.isLeftChild():
                    addCmd("SetText", 0, "Node and parent are both red.  Node is left child, parent is left child\nCan fix extra redness with a single rotation")
                    addCmd("Step")
                    
                    self.singleRotateRight(tree.parent.parent)
                    tree.parent.blackLevel = 1
                    addCmd("SetForegroundColor", tree.parent.graphicID, FOREGROUND_BLACK)
                    addCmd("SetBackgroundColor",tree.parent.graphicID, BACKGROUND_BLACK)

                    tree.parent.right.blackLevel = 0
                    addCmd("SetForegroundColor", tree.parent.right.graphicID, FOREGROUND_RED)
                    addCmd("SetBackgroundColor",tree.parent.right.graphicID, BACKGROUND_RED)
                else:
                    addCmd("SetText", 0, "Node and parent are both red.  Node is right child, parent is right child\nCan fix extra redness with a single rotation")
                    addCmd("Step")
                    
                    self.singleRotateLeft(tree.parent.parent)
                    tree.parent.blackLevel = 1
                    addCmd("SetForegroundColor", tree.parent.graphicID, FOREGROUND_BLACK)
                    addCmd("SetBackgroundColor",tree.parent.graphicID, BACKGROUND_BLACK)
                    
                    tree.parent.left.blackLevel = 0
                    addCmd("SetForegroundColor", tree.parent.left.graphicID, FOREGROUND_RED)
                    addCmd("SetBackgroundColor",tree.parent.left.graphicID, BACKGROUND_RED)
        else:
            if tree.blackLevel == 0:
                addCmd("SetText", 0, "Root of the tree is red.  Color it black")
                addCmd("Step")

                tree.blackLevel = 1
                addCmd("SetForegroundColor", tree.graphicID, FOREGROUND_BLACK)
                addCmd("SetBackgroundColor", tree.graphicID, BACKGROUND_BLACK)

    def treeDelete(self, tree, valueToDelete):
        leftchild = False
        if tree != None and not tree.phantomLeaf:
            if tree.parent != None:
                leftchild = tree.parent.left == tree
            
            addCmd("SetHighlight", tree.graphicID, 1)
            if float(valueToDelete) < float(tree.value):
                addCmd("SetText", 0, valueToDelete + " < " + tree.value + ".  Looking at left subtree")
            elif float(valueToDelete) > float(tree.value):
                addCmd("SetText", 0, valueToDelete + " > " + tree.value + ".  Looking at right subtree")
            else:
                addCmd("SetText", 0, valueToDelete + " == " + tree.value + ".  Found node to delete")
            addCmd("Step")
            addCmd("SetHighlight", tree.graphicID, 0)
            
            if valueToDelete == tree.value:
                needFix = tree.blackLevel > 0
                if ((tree.left == None) or tree.left.phantomLeaf)  and ((tree.right == None) or tree.right.phantomLeaf):
                    addCmd("SetText",  0, "Node to delete is a leaf.  Delete it.")
                    addCmd("Delete", tree.graphicID)
                    
                    if tree.left != None:
                        addCmd("Delete", tree.left.graphicID)
                    if tree.right != None:
                        addCmd("Delete", tree.right.graphicID)
                    
                    if leftchild and tree.parent != None:
                        tree.parent.left = None
                        self.resizeTree()				
                        
                        if needFix:
                            self.fixLeftNull(tree.parent)
                        else:
                            self.attachLeftNullLeaf(tree.parent)
                            self.resizeTree()
                    
                    elif tree.parent != None:
                        tree.parent.right = None
                        self.resizeTree()		
                        if needFix:
                            self.fixRightNull(tree.parent)
                        else:
                            self.attachRightNullLeaf(tree.parent)
                            self.resizeTree()
                    else:
                        self.treeRoot = None
                    
                
                elif tree.left == None or tree.left.phantomLeaf:
                    addCmd("SetText", 0, "Node to delete has no left child.  \nSet parent of deleted node to right child of deleted node.")
                    if tree.left != None:
                        addCmd("Delete", tree.left.graphicID)
                        tree.left = None
                    
                    if tree.parent != None:
                        addCmd("Disconnect", tree.parent.graphicID, tree.graphicID)
                        addCmd("Connect", tree.parent.graphicID, tree.right.graphicID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tree.graphicID)
                        if leftchild:
                            tree.parent.left = tree.right
                            if needFix:
                                addCmd("SetText", 0, "Back node removed.  Increasing child's blackness level")
                                tree.parent.left.blackLevel += 1
                                self.fixNodeColor(tree.parent.left)
                                self.fixExtraBlack(tree.parent.left)
                        else:
                            tree.parent.right = tree.right
                            if needFix:
                                tree.parent.right.blackLevel += 1
                                addCmd("SetText", 0, "Back node removed.  Increasing child's blackness level")
                                self.fixNodeColor(tree.parent.right)
                                self.fixExtraBlack(tree.parent.right)
                        tree.right.parent = tree.parent
                    else:
                        addCmd("Delete", tree.graphicID)
                        self.treeRoot = tree.right
                        self.treeRoot.parent = None
                        if self.treeRoot.blackLevel == 0:
                            self.treeRoot.blackLevel = 1
                            addCmd("SetForegroundColor", self.treeRoot.graphicID, FOREGROUND_BLACK)
                            addCmd("SetBackgroundColor", self.treeRoot.graphicID, BACKGROUND_BLACK)
                    
                    self.resizeTree()
                elif tree.right == None or tree.right.phantomLeaf:
                    addCmd("SetText",  0,"Node to delete has no right child.  \nSet parent of deleted node to left child of deleted node.")
                    if tree.right != None:
                        addCmd("Delete", tree.right.graphicID)
                        tree.right = None
                    if tree.parent != None:
                        addCmd("Disconnect", tree.parent.graphicID, tree.graphicID)
                        addCmd("Connect", tree.parent.graphicID, tree.left.graphicID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tree.graphicID)
                        if leftchild:
                            tree.parent.left = tree.left
                            if needFix:
                                tree.parent.left.blackLevel += 1
                                self.fixNodeColor(tree.parent.left)
                                self.fixExtraBlack(tree.parent.left)
                                self.resizeTree();
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.")							
                                self.resizeTree()
                        else:
                            tree.parent.right = tree.left
                            if needFix:
                                tree.parent.right.blackLevel += 1
                                self.fixNodeColor(tree.parent.right)
                                self.fixExtraBlack(tree.parent.left)
                                self.resizeTree()
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.");								
                                self.resizeTree()
                        tree.left.parent = tree.parent
                    else:
                        addCmd("Delete" , tree.graphicID)
                        self.treeRoot = tree.left
                        self.treeRoot.parent = None
                        if self.treeRoot.blackLevel == 0:
                            self.treeRoot.blackLevel = 1
                            self.fixNodeColor(self.treeRoot)
                else: # tree.left != None && tree.right != None\
                    addCmd("SetText", 0, "Node to delete has two childern.  \nFind largest node in left subtree.")								
                    
                    self.highlightID = self.nextIndex
                    self.nextIndex += 1
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                    tmp = tree
                    tmp = tree.left
                    addCmd("Move", self.highlightID, tmp.x, tmp.y)
                    addCmd("Step")

                    while tmp.right != None and not tmp.right.phantomLeaf:
                        tmp = tmp.right
                        addCmd("Move", self.highlightID, tmp.x, tmp.y)
                        addCmd("Step")

                    if tmp.right != None:
                        addCmd("Delete", tmp.right.graphicID)
                        tmp.right = None

                    addCmd("SetText", tree.graphicID, " ")
                    labelID = self.nextIndex
                    self.nextIndex += 1
                    addCmd("CreateLabel", labelID, tmp.value, tmp.x, tmp.y)
                    addCmd("SetForegroundColor", labelID, BLUE)
                    tree.value = tmp.value
                    addCmd("Move", labelID, tree.x, tree.y)
                    addCmd("SetText", 0, "Copy largest value of left subtree into node to delete.")								
                    
                    addCmd("Step")
                    addCmd("SetHighlight", tree.graphicID, 0)
                    addCmd("Delete", labelID)
                    addCmd("SetText", tree.graphicID, tree.value)
                    addCmd("Delete", self.highlightID)				
                    addCmd("SetText", 0, "Remove node whose value we copied.")									
                    
                    needFix = tmp.blackLevel > 0;
                    
                    if tmp.left == None:
                        addCmd("Delete", tmp.graphicID)
                        if tmp.parent != tree:
                            tmp.parent.right = None
                            self.resizeTree()
                            if needFix:
                                self.fixRightNull(tmp.parent)
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.")						
                                addCmd("Step")
                        else:
                            tree.left = None
                            self.resizeTree()
                            if needFix:
                                self.fixLeftNull(tmp.parent)
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.")							
                                addCmd("Step")
                    else:
                        addCmd("Disconnect", tmp.parent.graphicID, tmp.graphicID)
                        addCmd("Connect", tmp.parent.graphicID, tmp.left.graphicID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tmp.graphicID)
                        
                        if tmp.parent != tree:
                            tmp.parent.right = tmp.left
                            tmp.left.parent = tmp.parent
                            self.resizeTree()
                            
                            if needFix:
                                addCmd("SetText", 0, "Coloring child of deleted node black")
                                addCmd("Step")
                                tmp.left.blackLevel += 1

                                if tmp.left.phantomLeaf:
                                    addCmd("SetLayer", tmp.left.graphicID, 0)

                                self.fixNodeColor(tmp.left)
                                self.fixExtraBlack(tmp.left)

                                if tmp.left.phantomLeaf:
                                    addCmd("SetLayer", tmp.left.graphicID, 1)
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.")							
                                addCmd("Step")
                        else:
                            tree.left = tmp.left
                            tmp.left.parent = tree
                            self.resizeTree()
                            if needFix:
                                addCmd("SetText", 0, "Coloring child of deleted node black")
                                addCmd("Step")
                                tmp.left.blackLevel += 1
                                if tmp.left.phantomLeaf:
                                    addCmd("SetLayer", tmp.left.graphicID, 0)
                                
                                self.fixNodeColor(tmp.left)
                                self.fixExtraBlack(tmp.left)
                                if tmp.left.phantomLeaf:
                                    addCmd("SetLayer", tmp.left.graphicID, 1)
                            else:
                                addCmd("SetText", 0, "Deleted node was red.  No tree rotations required.")								
                                addCmd("Step")

                    tmp = tmp.parent;
                    
            elif float(valueToDelete) < float(tree.value):
                if tree.left != None:
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                    addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                    addCmd("Step")
                    addCmd("Delete", self.highlightID)
                self.treeDelete(tree.left, valueToDelete)
            else:
                if tree.right != None:
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_COLOR, tree.x, tree.y)
                    addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                    addCmd("Step")
                    addCmd("Delete", self.highlightID)
                self.treeDelete(tree.right, valueToDelete)
        else:
            addCmd("SetText", 0, "Elemet "+valueToDelete+" not found, could not delete");

    def fixNodeColor(self, tree):
        if tree.blackLevel == 0:
            addCmd("SetForegroundColor", tree.graphicID, FOREGROUND_RED)
            addCmd("SetBackgroundColor", tree.graphicID, BACKGROUND_RED)
        else:
            addCmd("SetForegroundColor", tree.graphicID, FOREGROUND_BLACK)
            if tree.blackLevel > 1:
                addCmd("SetBackgroundColor",tree.graphicID, BACKGROUND_DOUBLE_BLACK)
            else:
                addCmd("SetBackgroundColor",tree.graphicID, BACKGROUND_BLACK)
        return
    
    def fixExtraBlack(self, tree):
        if tree.blackLevel > 1:
            if tree.parent == None:
                addCmd("SetText", 0, "Double black node is root.  Make it single black.")
                addCmd("Step")
                
                tree.blackLevel = 1
                addCmd("SetBackgroundColor", tree.graphicID, BACKGROUND_BLACK)
            elif tree.parent.left == tree:
                self.fixExtraBlackChild(tree.parent, True)
            else:
                self.fixExtraBlackChild(tree.parent, False)
        return

    def fixExtraBlackChild(self, parNode, isLeftChild):
        if isLeftChild:
            sibling = parNode.right
            doubleBlackNode = parNode.left
        else:
            sibling = parNode.left		
            doubleBlackNode = parNode.right

        if self.blackLevel(sibling) > 0 and self.blackLevel(sibling.left) > 0 and self.blackLevel(sibling.right) > 0:
            addCmd("SetText", 0, "Double black node has black sibling and 2 black nephews.  Push up black level")
            addCmd("Step")
            sibling.blackLevel = 0
            self.fixNodeColor(sibling)
            if doubleBlackNode != None:
                doubleBlackNode.blackLevel = 1
                self.fixNodeColor(doubleBlackNode)
                
            if parNode.blackLevel == 0:
                parNode.blackLevel = 1
                self.fixNodeColor(parNode)
            else:
                parNode.blackLevel = 2
                self.fixNodeColor(parNode)
                addCmd("SetText", 0, "Pushing up black level created another double black node.  Repeating ...")
                addCmd("Step")
                self.fixExtraBlack(parNode)	
        elif self.blackLevel(sibling) == 0:
            addCmd("SetText", 0, "Double black node has red sibling.  Rotate tree to make sibling black ...")
            addCmd("Step")
            if isLeftChild:
                newPar = self.singleRotateLeft(parNode)
                newPar.blackLevel = 1
                self.fixNodeColor(newPar)
                newPar.left.blackLevel = 0
                self.fixNodeColor(newPar.left)
                addCmd("Step")
                self.fixExtraBlack(newPar.left.left)
            else:
                newPar = self.singleRotateRight(parNode)
                newPar.blackLevel = 1
                self.fixNodeColor(newPar)
                newPar.right.blackLevel = 0
                self.fixNodeColor(newPar.right)
                addCmd("Step")
                self.fixExtraBlack(newPar.right.right)
        elif isLeftChild and self.blackLevel(sibling.right) > 0:
            addCmd("SetText", 0, "Double black node has black sibling, but double black node is a left child, \nand the right nephew is black.  Rotate tree to make opposite nephew red ...")
            addCmd("Step")
            
            newSib = self.singleRotateRight(sibling)
            newSib.blackLevel = 1
            self.fixNodeColor(newSib)
            newSib.right.blackLevel = 0
            self.fixNodeColor(newSib.right)
            addCmd("Step")
            self.fixExtraBlackChild(parNode, isLeftChild)
        elif not isLeftChild and self.blackLevel(sibling.left) > 0:
            addCmd("SetText", 0, "Double black node has black sibling, but double black node is a right child, \nand the left nephew is black.  Rotate tree to make opposite nephew red ...")
            addCmd("Step")
            newSib = self.singleRotateLeft(sibling)
            newSib.blackLevel = 1
            self.fixNodeColor(newSib)
            newSib.left.blackLevel = 0
            self.fixNodeColor(newSib.left)
            addCmd("Step")
            self.fixExtraBlackChild(parNode, isLeftChild)
        elif isLeftChild:
            addCmd("SetText", 0, "Double black node has black sibling, is a left child, and its right nephew is red.\nOne rotation can fix double-blackness.")
            addCmd("Step")
            
            oldParBlackLevel  = parNode.blackLevel
            newPar = self.singleRotateLeft(parNode)
            if oldParBlackLevel == 0:
                newPar.blackLevel = 0
                self.fixNodeColor(newPar)
                newPar.left.blackLevel = 1
                self.fixNodeColor(newPar.left)
            newPar.right.blackLevel = 1
            self.fixNodeColor(newPar.right)
            if newPar.left.left != None:
                newPar.left.left.blackLevel = 1
                self.fixNodeColor(newPar.left.left)
        else:
            addCmd("SetText", 0, "Double black node has black sibling, is a right child, and its left nephew is red.\nOne rotation can fix double-blackness.")
            addCmd("Step")
            
            oldParBlackLevel  = parNode.blackLevel
            newPar = self.singleRotateRight(parNode)
            if oldParBlackLevel == 0:
                newPar.blackLevel = 0
                self.fixNodeColor(newPar)
                newPar.right.blackLevel = 1
                self.fixNodeColor(newPar.right)
            newPar.left.blackLevel = 1
            self.fixNodeColor(newPar.left)
            if newPar.right.right != None:
                newPar.right.right.blackLevel = 1
                self.fixNodeColor(newPar.right.right)
        return

    def singleRotateLeft(self, tree):
        A = tree
        B = tree.right
        t2 = B.left
        
        addCmd("SetText", 0, "Single Rotate Left")
        addCmd("SetEdgeHighlight", A.graphicID, B.graphicID, 1)
        addCmd("Step")
        
        if t2 != None:
            addCmd("Disconnect", B.graphicID, t2.graphicID)																	  
            addCmd("Connect", A.graphicID, t2.graphicID, LINK_COLOR)
            t2.parent = A
        addCmd("Disconnect", A.graphicID, B.graphicID)
        addCmd("Connect", B.graphicID, A.graphicID, LINK_COLOR)
        B.parent = A.parent
        if self.treeRoot == A:
            self.treeRoot = B
        else:
            addCmd("Disconnect", A.parent.graphicID, A.graphicID, LINK_COLOR)
            addCmd("Connect", A.parent.graphicID, B.graphicID, LINK_COLOR)
            
            if A.isLeftChild():
                A.parent.left = B
            else:
                A.parent.right = B
        B.left = A
        A.parent = B
        A.right = t2
        self.resetHeight(A)
        self.resetHeight(B)
        
        self.resizeTree()
        return B

    def singleRotateRight(self, tree):
        B = tree
        A = tree.left
        t2 = A.right
        
        addCmd("SetText", 0, "Single Rotate Right")
        addCmd("SetEdgeHighlight", B.graphicID, A.graphicID, 1)
        addCmd("Step")
        
        if t2 != None:
            addCmd("Disconnect", A.graphicID, t2.graphicID)
            addCmd("Connect", B.graphicID, t2.graphicID, LINK_COLOR)
            t2.parent = B
        addCmd("Disconnect", B.graphicID, A.graphicID)
        addCmd("Connect", A.graphicID, B.graphicID, LINK_COLOR)
        
        A.parent = B.parent
        if self.treeRoot == B:
            self.treeRoot = A
        else:
            addCmd("Disconnect", B.parent.graphicID, B.graphicID, LINK_COLOR);
            addCmd("Connect", B.parent.graphicID, A.graphicID, LINK_COLOR)
            if B.isLeftChild():
                B.parent.left = A
            else:
                B.parent.right = A
        A.right = B
        B.parent = A
        B.left = t2
        self.resetHeight(B)
        self.resetHeight(A)
        self.resizeTree()	
        return A
        
    def resetHeight(self, tree):
        if tree != None:
            newHeight = max(self.getHeight(tree.left), self.getHeight(tree.right)) + 1
            if tree.height != newHeight:
                tree.height = max(self.getHeight(tree.left), self.getHeight(tree.right)) + 1

    def getHeight(self, tree):
        if tree == None:
            return 0
        return tree.height
        
    def fixLeftNull(self, tree):
        treeNodeID = self.nextIndex
        self.nextIndex += 1
        addCmd("SetText", 0, "Coloring 'Null Leaf' double black")
        
        addCmd("CreateCircle", treeNodeID, "NULL\nLEAF",  tree.x, tree.y)
        addCmd("SetForegroundColor", treeNodeID, FOREGROUND_BLACK)
        addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_DOUBLE_BLACK)
        nullLeaf = RBNode("NULL\nLEAF", treeNodeID, tree.x, tree.x)
        nullLeaf.blackLevel = 2
        nullLeaf.parent = tree
        nullLeaf.phantomLeaf = True
        tree.left = nullLeaf
        addCmd("Connect", tree.graphicID, nullLeaf.graphicID, LINK_COLOR)
        
        self.resizeTree()		
        self.fixExtraBlackChild(tree, True)
        addCmd("SetLayer", nullLeaf.graphicID, 1)
        nullLeaf.blackLevel = 1
        self.fixNodeColor(nullLeaf)
        return

    def fixRightNull(self, tree):
        treeNodeID = self.nextIndex
        self.nextIndex += 1
        addCmd("SetText", 0, "Coloring 'Null Leaf' double black")
        
        addCmd("CreateCircle", treeNodeID, "NULL\nLEAF",  tree.x, tree.y)
        addCmd("SetForegroundColor", treeNodeID, FOREGROUND_BLACK)
        addCmd("SetBackgroundColor", treeNodeID, BACKGROUND_DOUBLE_BLACK)
        nullLeaf = RBNode("NULL\nLEAF", treeNodeID, tree.x, tree.x)
        nullLeaf.parent = tree
        nullLeaf.phantomLeaf = True
        nullLeaf.blackLevel = 2
        tree.right = nullLeaf
        addCmd("Connect", tree.graphicID, nullLeaf.graphicID, LINK_COLOR)
        
        self.resizeTree()
        
        self.fixExtraBlackChild(tree, False)
        
        addCmd("SetLayer", nullLeaf.graphicID, 1)
        nullLeaf.blackLevel = 1
        self.fixNodeColor(nullLeaf)
        return

    def findUncle(self, tree):
        if tree.parent == None:
            return None

        par  = tree.parent

        if par.parent == None:
            return None

        grandPar   = par.parent
        
        if grandPar.left == par:
            return grandPar.right
        else:
            return grandPar.left

    def blackLevel(self, tree):
        if tree == None:
            return 1
        else:
            return tree.blackLevel
# -----------------------------------------------------------
# Initialize Flask Backend
# -----------------------------------------------------------
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
rbt = Blueprint('rbt', __name__)
CORS(rbt)
myRBTree = RBTree(1000, 500)


# -----------------------------------------------------------
# API for different rbTree methods
# 
# 1. Insert: /rbTree/insert/<value>
# 2. Find: /rbTree/find/<value>
# 3. Delete: /rbTree/delete/<value>
# 4. Print(Inorder): /rbTree/print
# 
# -----------------------------------------------------------
@rbt.route('/', methods=['GET'] )
def create_circle():
    objectId, value = "1", "10"
    initX, initY = "0", "0" 
    action = {"CreateCircle" : objectId + "<;>" + value + "<;>" + initX + "<;>" + initY }
    return  jsonify(action)

@rbt.route('/rbTree/reset', methods=['GET'] )
def reset():
    myRBTree.reset()
    return json.dumps(["My RBTree is reloaded!!", "myRBTree nextIndex", myRBTree.nextIndex])

@rbt.route('/rbTree/insert/<value>', methods=['GET'] )
def getInsert(value):
    myRBTree.insert(value)
    return json.dumps(AnimationCommands)

@rbt.route('/rbTree/find/<value>', methods=['GET'] )
def getFind(value):
    myRBTree.find(value)
    return json.dumps(AnimationCommands)

@rbt.route('/rbTree/delete/<value>', methods=['GET'] )
def getDelete(value):
    myRBTree.delete(value)
    return json.dumps(AnimationCommands)

@rbt.route('/rbTree/print', methods=['GET'] )
def getPrint():
    myRBTree.print()
    return json.dumps(AnimationCommands)
    
@rbt.route('/rbTree/build', methods=['GET'] )
def getBuild(steps=10, Random=True):
    myRBTree.build(steps, Random)
    return json.dumps(AnimationCommands)