from flask import Flask, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import os, json


# -----------------------------------------------------------
# Define some static variables
# -----------------------------------------------------------
LINK_COLOR = "#007700"
HIGHLIGHT_CIRCLE_COLOR = "#007700"
FOREGROUND_COLOR = "#ED7211"
BACKGROUND_COLOR = "#EEFFEE"
PRINT_COLOR = FOREGROUND_COLOR

WIDTH_DELTA  = 50
HEIGHT_DELTA = 50
STARTING_Y = 50
CANVAS_WIDTH = 1000
CANVAS_HEGHT = 500


FIRST_PRINT_POS_X  = 50
PRINT_VERTICAL_GAP  = 20
PRINT_HORIZONTAL_GAP = 50

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
# Define BST class
# -----------------------------------------------------------
class BSTNode():

    def __init__(self, key, id, initialX, initialY):
        self.value = key
        self.graphID = id
        self.x = initialX
        self.y = initialY
        self.left = None
        self.right = None
        self.parent = None

        # For tree root in resize tree
        self.leftWidth = WIDTH_DELTA//2
        self.rightWidth = WIDTH_DELTA//2

class BST():

    def __init__(self):
        self.root = None
        self.nextIndex = 0
        addCmd("CreateLabel", 0, "", 20, 10, 0)
        self.nextIndex += 1
        self.startingX = CANVAS_WIDTH//2
        self.first_print_pos_y = CANVAS_HEGHT - 2 * PRINT_VERTICAL_GAP
        self.print_max = CANVAS_WIDTH - 10
    
    def insert(self, value):
        # TODO: Normalize value
        
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        
        if self.root == None:
            if self.nextIndex > 2:
                clearCmd()
            addCmd("SetText", 0, "Inserting "+value)
            addCmd("CreateCircle", self.nextIndex, value, self.startingX, STARTING_Y)
            addCmd("SetForegroundColor", self.nextIndex, FOREGROUND_COLOR)
            addCmd("SetBackgroundColor", self.nextIndex, BACKGROUND_COLOR)
            addCmd("Step")
            self.root = BSTNode(value, self.nextIndex, self.startingX, STARTING_Y)
            self.nextIndex += 1
        else:
            clearCmd()
            addCmd("SetText", 0, "Inserting "+value)
            addCmd("CreateCircle", self.nextIndex, value, 100, 100)
            addCmd("SetForegroundColor", self.nextIndex, FOREGROUND_COLOR)
            addCmd("SetBackgroundColor", self.nextIndex, BACKGROUND_COLOR)
            addCmd("Step")
            insertNode = BSTNode(value, self.nextIndex, 100, 100)

            self.nextIndex += 1
            # addCmd("SetHighlight", insertNode.graphID, 1)
            self.insertElem(insertNode, self.root)
            self.resizeTree()
        
        addCmd("SetText", 0, "")

    def insertElem(self, node:BSTNode, tree:BSTNode):
        addCmd("SetHighlight", tree.graphID, 1)
        addCmd("SetHighlight", node.graphID, 1)

        if int(node.value) < int(tree.value):
            addCmd("SetText", 0, node.value + " < " + tree.value + ". Looking at left subtree")
        else:
            addCmd("SetText", 0, node.value + " >= " + tree.value + ". Looking at right subtree")
        addCmd("Step")
        addCmd("SetHighlight", tree.graphID, 0)
        addCmd("SetHighlight", node.graphID, 0)

        if int(node.value) < int(tree.value):
            if tree.left == None:
                addCmd("SetText", 0, "Found null tree, inserting element in left subtree")
                addCmd("SetHighlight", node.graphID, 0)
                tree.left = node 
                node.parent = tree
                addCmd("Connect", tree.graphID, node.graphID, LINK_COLOR)
                # node.x, node.y = tree.x - WIDTH_DELTA//2, tree.y + WIDTH_DELTA//2
                # addCmd("Move", node.graphID, node.x, node.y)

            else:
                addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                addCmd("Step")
                addCmd("Delete", self.highlightID)
                self.insertElem(node, tree.left)

        else:
            if tree.right == None:
                addCmd("SetText", 0, "Found null tree, inserting element in right subtree")
                addCmd("SetHighlight", node.graphID, 0)
                tree.right = node 
                node.parent = tree
                addCmd("Connect", tree.graphID, node.graphID, LINK_COLOR)
                # node.x, node.y = tree.x + WIDTH_DELTA//2, tree.y + WIDTH_DELTA
                # addCmd("Move", node.graphID, node.x, node.y)

            else:
                addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                addCmd("Step")
                addCmd("Delete", self.highlightID)
                self.insertElem(node, tree.right)
            

    def resizeTree(self):
        startingPoint = self.startingX

        if self.root != None:
            if self.root.leftWidth > startingPoint:
                startingPoint = self.root.leftWidth
            elif self.root.rightWidth > startingPoint:
                startingPoint = max(self.root.leftWidth, 2*startingPoint-self.root.rightWidth)
            self.setNewPos(self.root, startingPoint, STARTING_Y, 0)
            self.adjustAnimatePos(self.root)
            addCmd("Step")
    

    def resizeWidth(self, tree:BSTNode):
        if tree == None:
            return 0
        tree.leftWidth = max(self.resizeTree(tree.left), WIDTH_DELTA//2)
        tree.rightWidth = max(self.resizeTree(tree.right), WIDTH_DELTA//2)
        return tree.leftWidth + tree.rightWidth
    

    def adjustAnimatePos(self, tree:BSTNode):
        if tree != None:
            addCmd("Move", tree.graphID, tree.x, tree.y)
            self.adjustAnimatePos(tree.left)
            self.adjustAnimatePos(tree.right)


    def setNewPos(self, tree:BSTNode, xPos, yPos, side):
        if tree != None:
            tree.y = yPos
            if side == -1: # Adjust left subtree x pos
                xPos = xPos - tree.rightWidth 
            elif side == 1: # Adjust right subtree x pos
                xPos = xPos + tree.leftWidth
            tree.x = xPos
            self.setNewPos(tree.left, xPos, yPos + HEIGHT_DELTA, -1)
            self.setNewPos(tree.right, xPos, yPos + HEIGHT_DELTA, 1)

        
    def find(self, value):
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        
        clearCmd()
        self.doFind(self.root, value)

    def doFind(self, tree:BSTNode, value):
        addCmd("SetText", 0, "Searching for " + value)

        if tree != None:
            addCmd("SetHighlight", tree.graphID, 1)

            if int(tree.value) == int(value):
                addCmd("SetText", 0, "Searching for " + value + " : " + tree.value + " = " + value + " (Element found!)")
                addCmd("Step")
                addCmd("SetText", 0, "Found:" + value)
                addCmd("SetHighlight", tree.graphID, 0)
            
            else:
                if int(tree.value) > int(value):
                    addCmd("SetText", 0, "Searching for " + value + " : " + value + " < " + tree.value + " (look to left subtree)")
                    addCmd("Step")
                    addCmd("SetHighlight", tree.graphID, 0)

                    if tree.left != None:
                        addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                        addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                        addCmd("Step")
                        addCmd("Delete", self.highlightID)
                    
                    self.doFind(tree.left, value)
                
                else:
                    addCmd("SetText", 0, "Searching for " + value + " : " + value + " > " + tree.value + " (look to right subtree)")
                    addCmd("Step")
                    addCmd("SetHighlight", tree.graphID, 0)

                    if tree.left != None:
                        addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                        addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                        addCmd("Step")
                        addCmd("Delete", self.highlightID)
                    
                    self.doFind(tree.right, value)
        else:
            addCmd("SetText", 0, "Searching for "+value+" : " + "< Empty Tree > (Element not found)")
            addCmd("Step")
            addCmd("SetText", 0, "Searching for "+value+" : " + " (Element not found)")



    def delete(self, value):

        clearCmd()
        addCmd("SetText", 0, "Deleting "+value)
        addCmd("Step")
        addCmd("SetText", 0, "")
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        self.treeDelete(self.root, value)
        addCmd("SetText", 0, "")
    
    def treeDelete(self, tree:BSTNode, value):
        
        leftchild = False

        if tree != None:
            if tree.parent != None and tree.parent.left == tree:
                leftchild = True

            addCmd("SetHighlight", tree.graphID, 1)

            if int(value) < int(tree.value):
                addCmd("SetText", 0, value + " < " + tree.value + ".  Looking at left subtree")
            elif int(value) > int(tree.value):
                addCmd("SetText", 0, value + " > " + tree.value + ".  Looking at right subtree")
            else:
                addCmd("SetText", 0, value + " == " + tree.value + ".  Found node to delete")
            addCmd("Step")
            addCmd("SetHighlight", tree.graphID, 0)

            # Start to Delete the Node

            if int(value) == int(tree.value):

                if tree.left == None and tree.right == None: # First Case: Delete Leaf Node
                    addCmd("SetText", 0, "Node to delete is a leaf.  Delete it.")
                    addCmd("Delete", tree.graphID)

                    if leftchild and tree.parent != None:
                        tree.parent.left = None
                    elif tree.parent != None:
                        tree.parent.right = None
                    else:
                        self.root = None

                    self.resizeTree()
                    addCmd("Step")

                elif tree.left == None: # Second Case: Node have no left child
                    addCmd("SetText", 0, "Node to delete has no left child.  \nSet parent of deleted node to right child of deleted node.")
                    if tree.parent != None:
                        addCmd("Disconnect", tree.parent.graphID, tree.graphID)
                        addCmd("Connect",  tree.parent.graphID, tree.right.graphID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tree.graphID)

                        if leftchild:
                            tree.parent.left = tree.right
                        else:
                            tree.parent.right = tree.right

                        tree.right.parent = tree.parent

                    else:
                        addCmd("Delete", tree.graphID)
                        self.root = tree.right
                        self.root.parent = None
                    
                    self.resizeTree()
                
                elif tree.right == None: # Third Case: Node have no right child
                    addCmd("SetText", 0, "Node to delete has no right child.  \nSet parent of deleted node to left child of deleted node.")
                    if tree.parent != None:
                        addCmd("Disconnect", tree.parent.graphID, tree.graphID)
                        addCmd("Connect",  tree.parent.graphID, tree.left.graphID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tree.graphID)

                        if leftchild:
                            tree.parent.left = tree.left
                        else:
                            tree.parent.right = tree.left
                            
                        tree.left.parent = tree.parent

                    else:
                        addCmd("Delete", tree.graphID)
                        self.root = tree.left
                        self.root.parent = None
                    
                    self.resizeTree()
                
                else: # Fourth Case: Node have both children
                    addCmd("SetText", 0, "Node to delete has two childern.  \nFind largest node in left subtree.")
                    
                    self.highlightID = self.nextIndex
                    self.nextIndex += 1
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                    tmp = tree.left
                    addCmd("Move", self.highlightID, tmp.x, tmp.y)
                    addCmd("Step")

                    while tmp.right != None:
                        tmp = tmp.right
                        addCmd("Move", self.highlightID, tmp.x, tmp.y)
                        addCmd("Step")
                    
                    addCmd("SetText", tree.graphID, "")
                    labelID = self.nextIndex
                    self.nextIndex += 1
                    addCmd("CreateLabel", labelID, tmp.value, tmp.x, tmp.y)
                    tree.value = tmp.value
                    addCmd("Move", labelID, tree.x, tree.y)
                    addCmd("SetText", 0, "Copy largest value " + tree.value + " of left subtree into node to delete.")
                    addCmd("Step")

                    addCmd("SetHighlight", tree.graphID, 0)
                    addCmd("Delete", labelID)
                    addCmd("SetText", tree.graphID, tree.value)
                    addCmd("Delete", self.highlightID)
                    addCmd("SetText", 0, "Remove node whose value we copied.")

                    if tmp.left == None:
                        if tmp.parent != tree:
                            tmp.parent.right = None
                        else:
                            tree.left = None

                        addCmd("Delete", tmp.graphID)
                    
                    else:
                        addCmd("Disconnect", tmp.parent.graphID, tmp.graphID)
                        addCmd("Connect", tmp.parent.graphID, tmp.left.graphID, LINK_COLOR)
                        addCmd("Step")
                        addCmd("Delete", tmp.graphID)

                        if tmp.parent != tree:
                            tmp.parent.right = tmp.left
                            tmp.left.parent = tmp.parent
                        else:
                            tree.left = tmp.left
                            tmp.left.parent = tree
                    
                    self.resizeTree()                    
                

            elif int(value) < int(tree.value):

                if tree.left != None:
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                    addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
                    addCmd("Step")
                    addCmd("Delete", self.highlightID)
                
                self.treeDelete(tree.left, value)

            else:

                if tree.right != None:
                    addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, tree.x, tree.y)
                    addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
                    addCmd("Step")
                    addCmd("Delete", self.highlightID)
                
                self.treeDelete(tree.right, value)

        
        else:
            addCmd("SetText", 0, "Elemet "+value+" not found, could not delete")
        

    def print(self):
        
        if self.root != None:
            clearCmd()
            self.highlightID = self.nextIndex
            self.nextIndex += 1
            firstLabel = self.nextIndex
            addCmd("CreateHighlightCircle", self.highlightID, HIGHLIGHT_CIRCLE_COLOR, self.root.x, self.root.y)
            self.xPosOfNextLabel, self.yPosOfNextLabel = FIRST_PRINT_POS_X, self.first_print_pos_y
            self.printTree(self.root)
            addCmd("Delete", self.highlightID)
            addCmd("Step")

            for i in range(firstLabel, self.nextIndex):
                addCmd("Delete", i)
            

    def printTree(self, tree:BSTNode):
        addCmd("Step")

        if tree.left != None:
            addCmd("Move", self.highlightID, tree.left.x, tree.left.y)
            self.printTree(tree.left)
            addCmd("Move", self.highlightID, tree.x, tree.y)
            addCmd("Step")
        
        nextLabelID = self.nextIndex
        self.nextIndex += 1

        addCmd("CreateLabel", nextLabelID, tree.value, tree.x, tree.y)
        addCmd("SetForegroundColor", nextLabelID, PRINT_COLOR)
        addCmd("Move", nextLabelID, self.xPosOfNextLabel, self.yPosOfNextLabel)
        addCmd("Step")

        self.xPosOfNextLabel += PRINT_HORIZONTAL_GAP
        if self.xPosOfNextLabel > self.print_max:
            self.xPosOfNextLabel = FIRST_PRINT_POS_X
            self.yPosOfNextLabel += PRINT_VERTICAL_GAP
        
        if tree.right != None:
            addCmd("Move", self.highlightID, tree.right.x, tree.right.y)
            self.printTree(tree.right)
            addCmd("Move", self.highlightID, tree.x, tree.y)
            addCmd("Step")
        
        return
        

# -----------------------------------------------------------
# Initialize Flask Backend
# -----------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
CORS(app)
myTree = BST()


# -----------------------------------------------------------
# API for different BST methods
# 
# 1. Insert: /bst/insert/<value>
# 2. Find: /bst/find/<value>
# 3. Delete: /bst/delete/<value>
# 4. Print(Inorder): /bst/print
# 
# -----------------------------------------------------------
@app.route('/', methods=['GET'] )
def create_circle():
    objectId, value = "1", "10"
    initX, initY = "0", "0" 
    action = {"CreateCircle" : objectId + "<;>" + value + "<;>" + initX + "<;>" + initY }
    return  jsonify(action)

@app.route('/bst/insert/<value>' )
def getInsert(value):
    myTree.insert(value)
    # session['tree'] = 'TREE'
    # AnimationCommands.append("Try to send this command")
    # AnimationCommands.append("Send second command")
    return json.dumps(AnimationCommands)

@app.route('/bst/find/<value>', methods=['GET'] )
def getFind(value):
    myTree.find(value)
    # tree = session['tree']
    return json.dumps(AnimationCommands)

@app.route('/bst/delete/<value>', methods=['GET'] )
def getDelete(value):
    myTree.delete(value)
    # tree = session['tree']
    return json.dumps(AnimationCommands)

@app.route('/bst/print', methods=['GET'] )
def getPrint():
    myTree.print()
    # tree = session['tree']
    return json.dumps(AnimationCommands)



# if __name__ == "__main__":
#     app.run(debug=True)