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

class BSTNode():
    pass

class BST():
    pass
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
    
    def insert(self, value):
        # TODO: Normalize value
        
        self.highlightID = self.nextIndex
        self.nextIndex += 1
        
        if self.root == None:
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
        pass

    def delete(self, value):
        pass

    def print(self):
        pass

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
    return jsonify(myTree.root.value)

@app.route('/bst/delete/<value>', methods=['GET'] )
def getDelete(value):
    myTree.delete(value)
    # tree = session['tree']
    return jsonify(myTree.root.value)

@app.route('/bst/print', methods=['GET'] )
def getPrint():
    myTree.print()
    # tree = session['tree']
    return jsonify(myTree.root.value)



# if __name__ == "__main__":
#     app.run(debug=True)