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
# Define maxnHeap class
# -----------------------------------------------------------
class maxnHeap():
    
    def __init__(self, size) -> None:
        self.array = []
        self.size = size
    
    def insert(self, value):
        pass
    
    def removeMax(self):
        pass

    def clear(self):
        pass

    def buildHeap(self):
        pass

    def swap(self, idx1, idx2):
        pass

    def pushDown(self, idx):
        pass


# -----------------------------------------------------------
# Initialize Flask Backend
# -----------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
CORS(app)
myHeap = maxnHeap()


# -----------------------------------------------------------
# API for different maxnHeap methods
# 
# 1. Insert: /maxnHeap/insert/<value>
# 2. Remove Smallest: /maxnHeap/rMax
# 3. Clear Heap: /maxnHeap/clear
# 4. Build Heap: /maxnHeap/build
# 
# -----------------------------------------------------------
@app.route('/', methods=['GET'] )
def create_circle():
    objectId, value = "1", "10"
    initX, initY = "0", "0" 
    action = {"CreateCircle" : objectId + "<;>" + value + "<;>" + initX + "<;>" + initY }
    return  jsonify(action)

@app.route('/maxnHeap/insert/<value>' )
def getInsert(value):
    myHeap.insert(value)
    return json.dumps(AnimationCommands)

@app.route('/maxnHeap/rMax', methods=['GET'] )
def getRemoveMax():
    myHeap.removeMax()
    # tree = session['tree']
    return json.dumps(AnimationCommands)

@app.route('/maxnHeap/clear', methods=['GET'] )
def getClear():
    myHeap.clear()
    # tree = session['tree']
    return json.dumps(AnimationCommands)

@app.route('/maxnHeap/build', methods=['GET'] )
def getBuild():
    myHeap.buildHeap()
    return json.dumps(AnimationCommands)
