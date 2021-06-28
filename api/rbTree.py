from flask import Flask, jsonify, session, Blueprint
from flask_cors import CORS
from datetime import timedelta
import os, json


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
# Define RBTree class
# -----------------------------------------------------------
class RBNode():

    def __init__(self, key, id, initialX, initialY):
        self.value = key
        self.graphID = id
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


class RBTree():
    
    def __init__(self):
        pass
    
    # Add any utility function if needed e.g. FindUncle, FindBlackLevel, SingleRotation etc.
    def insert(self, value):
        pass

    def find(self, value):
        pass

    def delete(self, value):
        pass

    def print(self):
        pass


# -----------------------------------------------------------
# Initialize Flask Backend
# -----------------------------------------------------------
rbt = Blueprint("rbt", __name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
CORS(rbt)
myRBTree = RBTree()


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

@rbt.route('/rbTree/insert/<value>' )
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