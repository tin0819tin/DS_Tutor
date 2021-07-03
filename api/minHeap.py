import re
from urllib.response import addclosehook
from flask import Flask, jsonify, session, Blueprint
from flask_cors import CORS
from datetime import timedelta
import os
import json
import math
import random


# -----------------------------------------------------------
# Define some static variables
# -----------------------------------------------------------
LINK_COLOR = "#007700"
HIGHLIGHT_CIRCLE_COLOR = "#007700"
FOREGROUND_COLOR = "#ED7211"
BACKGROUND_COLOR = "#EEFFEE"
PRINT_COLOR = FOREGROUND_COLOR

WIDTH_DELTA = 50
HEIGHT_DELTA = 50
STARTING_Y = 50
CANVAS_WIDTH = 1000
CANVAS_HEGHT = 500


FIRST_PRINT_POS_X = 50
PRINT_VERTICAL_GAP = 20
PRINT_HORIZONTAL_GAP = 50

ARRAY_ELEM_WIDTH = 30
ARRAY_ELEM_HEIGHT = 25
ARRAY_INITIAL_X = 30

ARRAY_Y_POS = 40
ARRAY_LABEL_Y_POS = 28

ARRAY_SIZE = 32   # fixed size

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


def Print(x):
    # print(x)
    pass
# -----------------------------------------------------------
# Define minHeap class
# -----------------------------------------------------------


class minHeap():

    def __init__(self, size=ARRAY_SIZE):
        self.size = size  # fixed array size
        self.nextIndex = 0
        self.HeapXPositions = [0, 450, 250, 650, 150, 350, 550, 750, 100, 200, 300, 400, 500, 600,
                               700, 800, 75, 125, 175, 225, 275, 325, 375, 425, 475, 525, 575, 625, 675, 725, 775, 825]
        self.HeapYPositions = [0, 100, 170, 170, 240, 240, 240, 240, 310, 310, 310, 310, 310, 310,
                               310, 310, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380, 380]
        self.createArray()
        self.first = True
        self.oper_list = []
    
    def reset(self):
        self.size = ARRAY_SIZE  # fixed array size
        self.nextIndex += 1
        self.createArray()
        self.first = True
        self.oper_list = []
        pass

    def insert(self, value, build=False):
        if value == "":
            return
        if not (self.first or build):
            clearCmd()
        self.first = False
        if self.currentHeapSize >= ARRAY_SIZE - 1:
            addCmd("SetText", self.descriptLabel1, "Heap Full!")
            # return self.commands
            Print(self.arrayData)
            return

        addCmd("SetText", self.descriptLabel1, "Inserting Element: " + value)
        addCmd("Step")
        addCmd("SetText", self.descriptLabel1, "Inserting Element: ")
        self.currentHeapSize += 1
        self.arrayData[self.currentHeapSize] = value
        addCmd("CreateCircle", self.circleObjs[self.currentHeapSize], "",
               self.HeapXPositions[self.currentHeapSize], self.HeapYPositions[self.currentHeapSize])
        addCmd("CreateLabel", self.descriptLabel2, value, 600, 460,  1)
        if self.currentHeapSize > 1:
            addCmd("Connect", self.circleObjs[math.floor(
                self.currentHeapSize / 2)], self.circleObjs[self.currentHeapSize])

        addCmd("Move", self.descriptLabel2,
               self.HeapXPositions[self.currentHeapSize], self.HeapYPositions[self.currentHeapSize])
        addCmd("Step")
        addCmd("SetText", self.circleObjs[self.currentHeapSize], value)
        addCmd("delete", self.descriptLabel2)
        addCmd("SetText", self.arrayRects[self.currentHeapSize], value)

        currentIndex = self.currentHeapSize
        parentIndex = math.floor(currentIndex / 2)

        if currentIndex > 1:
            self.setIndexHighlight(currentIndex, 1)
            self.setIndexHighlight(parentIndex, 1)
            addCmd("Step")
            self.setIndexHighlight(currentIndex, 0)
            self.setIndexHighlight(parentIndex, 0)

        # for min heap
        while currentIndex > 1 and float(self.arrayData[currentIndex]) < float(self.arrayData[parentIndex]):
            self.swap(currentIndex, parentIndex)
            currentIndex = parentIndex
            parentIndex = math.floor(parentIndex / 2)
            if currentIndex > 1:
                self.setIndexHighlight(currentIndex, 1)
                self.setIndexHighlight(parentIndex, 1)
                addCmd("Step")
                self.setIndexHighlight(currentIndex, 0)
                self.setIndexHighlight(parentIndex, 0)

        addCmd("SetText", self.descriptLabel1, "")
        # return self.commands;
        Print(self.arrayData)
        return

    def removeMin(self, build=False):
        if not (self.first or build):
            clearCmd()
        self.first = False
        addCmd("SetText", self.descriptLabel1, "")

        if self.currentHeapSize == 0:
            addCmd("SetText", self.descriptLabel1,
                   "Heap is empty, cannot remove smallest element")
            Print(self.arrayData)
            return

        addCmd("SetText", self.descriptLabel1, "Removing element:")
        addCmd("CreateLabel", self.descriptLabel2,
               self.arrayData[1],  self.HeapXPositions[1], self.HeapYPositions[1], 0)
        addCmd("SetText", self.circleObjs[1], "")
        addCmd("Move", self.descriptLabel2,  600, 460)
        addCmd("Step")
        addCmd("Delete", self.descriptLabel2)
        addCmd("SetText", self.descriptLabel1,
               "Removing element: " + self.arrayData[1])
        self.arrayData[1] = ""

        if self.currentHeapSize > 1:
            addCmd("SetText", self.arrayRects[1], "")
            addCmd("SetText", self.arrayRects[self.currentHeapSize], "")
            self.swap(1, self.currentHeapSize)
            addCmd("Delete", self.circleObjs[self.currentHeapSize])
            self.currentHeapSize -= 1
            self.pushDown(1)
        else:
            addCmd("SetText", self.arrayRects[1], "")
            addCmd("Delete", self.circleObjs[self.currentHeapSize])
            self.currentHeapSize -= 1
        Print(self.arrayData)
        return

    def clear(self):
        clearCmd()
        while self.currentHeapSize > 0:
            addCmd("Delete", self.circleObjs[self.currentHeapSize])
            addCmd("SetText", self.arrayRects[self.currentHeapSize], "")
            self.arrayData[self.currentHeapSize] = ''   # modified
            self.currentHeapSize -= 1
        Print(self.arrayData)
        return

    def buildHeap(self, steps, Random):    # TODO: self.normalizeNumber
        operation = ['insert', 'removeMin']
        if Random:
            self.oper_list = random.choices(operation, weights = [5, 2], k = 40)

        current_stpes = 0
        for oper in self.oper_list:
            if oper == 'insert':
                self.insert(str(random.randrange(999)), build=True)
                current_stpes += 1

            if oper == 'removeMin' and self.currentHeapSize > 0:
                self.removeMin(build=True)
                current_stpes += 1

            addCmd("Step")
            if current_stpes >= steps:
                break
        # clearCmd()
        # self.clear()
        # for i in range(1, ARRAY_SIZE):
        #     # self.arrayData[i] = self.normalizeNumber(String(ARRAY_SIZE - i), 4);
        #     addCmd("CreateCircle", self.circleObjs[i], self.arrayData[i],
        #            self.HeapXPositions[i], self.HeapYPositions[i])
        #     addCmd("SetText", self.arrayRects[i], self.arrayData[i])
        #     if i > 1:
        #         addCmd("Connect", self.circleObjs[math.floor(
        #             i/2)], self.circleObjs[i])
        # 
        # addCmd("Step")
        # self.currentHeapSize = ARRAY_SIZE - 1
        # nextElem = self.currentHeapSize
        # while nextElem > 0:
        #     self.pushDown(nextElem)
        #     nextElem = nextElem - 1
        # Print(self.arrayData)
        return

    def swap(self, idx1, idx2):
        addCmd("SetText", self.arrayRects[idx1], "")
        addCmd("SetText", self.arrayRects[idx2], "")
        addCmd("SetText", self.circleObjs[idx1], "")
        addCmd("SetText", self.circleObjs[idx2], "")
        addCmd("CreateLabel", self.swapLabel1,
               self.arrayData[idx1], self.ArrayXPositions[idx1], ARRAY_Y_POS)
        addCmd("CreateLabel", self.swapLabel2,
               self.arrayData[idx2], self.ArrayXPositions[idx2], ARRAY_Y_POS)
        addCmd("CreateLabel", self.swapLabel3,
               self.arrayData[idx1], self.HeapXPositions[idx1], self.HeapYPositions[idx1])
        addCmd("CreateLabel", self.swapLabel4,
               self.arrayData[idx2], self.HeapXPositions[idx2], self.HeapYPositions[idx2])
        addCmd("Move", self.swapLabel1,
               self.ArrayXPositions[idx2], ARRAY_Y_POS)
        addCmd("Move", self.swapLabel2,
               self.ArrayXPositions[idx1], ARRAY_Y_POS)
        addCmd("Move", self.swapLabel3,
               self.HeapXPositions[idx2], self.HeapYPositions[idx2])
        addCmd("Move", self.swapLabel4,
               self.HeapXPositions[idx1], self.HeapYPositions[idx1])
        tmp = self.arrayData[idx1]
        self.arrayData[idx1] = self.arrayData[idx2]
        self.arrayData[idx2] = tmp
        addCmd("Step")
        addCmd("SetText", self.arrayRects[idx1], self.arrayData[idx1])
        addCmd("SetText", self.arrayRects[idx2], self.arrayData[idx2])
        addCmd("SetText", self.circleObjs[idx1], self.arrayData[idx1])
        addCmd("SetText", self.circleObjs[idx2], self.arrayData[idx2])
        addCmd("Delete", self.swapLabel1)
        addCmd("Delete", self.swapLabel2)
        addCmd("Delete", self.swapLabel3)
        addCmd("Delete", self.swapLabel4)
        return

    def pushDown(self, idx):
        while True:
            if idx*2 > self.currentHeapSize:
                return

            smallestIndex = 2*idx

            if idx*2 + 1 <= self.currentHeapSize:
                self.setIndexHighlight(2*idx, 1)
                self.setIndexHighlight(2*idx + 1, 1)
                addCmd("Step")
                self.setIndexHighlight(2*idx, 0)
                self.setIndexHighlight(2*idx + 1, 0)
                if float(self.arrayData[2*idx + 1]) < float(self.arrayData[2*idx]):
                    smallestIndex = 2*idx + 1

            self.setIndexHighlight(idx, 1)
            self.setIndexHighlight(smallestIndex, 1)
            addCmd("Step")
            self.setIndexHighlight(idx, 0)
            self.setIndexHighlight(smallestIndex, 0)

            if float(self.arrayData[smallestIndex]) < float(self.arrayData[idx]):
                self.swap(smallestIndex, idx)
                idx = smallestIndex
            else:
                return

    # other functions
    def createArray(self):
        # print('into create array')
        self.arrayData = [''] * ARRAY_SIZE
        self.arrayLabels = [''] * ARRAY_SIZE
        self.arrayRects = [''] * ARRAY_SIZE
        self.circleObjs = [''] * ARRAY_SIZE
        self.ArrayXPositions = [''] * ARRAY_SIZE
        self.currentHeapSize = 0

        for i in range(ARRAY_SIZE):
            self.ArrayXPositions[i] = ARRAY_INITIAL_X + i * ARRAY_ELEM_WIDTH
            self.arrayLabels[i] = self.nextIndex
            self.nextIndex += 1
            self.arrayRects[i] = self.nextIndex
            self.nextIndex += 1
            self.circleObjs[i] = self.nextIndex
            self.nextIndex += 1
            addCmd("CreateRectangle", self.arrayRects[i], "", ARRAY_ELEM_WIDTH,
                   ARRAY_ELEM_HEIGHT, self.ArrayXPositions[i], ARRAY_Y_POS)
            addCmd("CreateLabel", self.arrayLabels[i], i,
                   self.ArrayXPositions[i]+15, ARRAY_LABEL_Y_POS)
            addCmd("SetForegroundColor", self.arrayLabels[i], "#0000FF")

        addCmd("SetText", self.arrayRects[0], "-INF")
        self.swapLabel1 = self.nextIndex
        self.nextIndex += 1
        self.swapLabel2 = self.nextIndex
        self.nextIndex += 1
        self.swapLabel3 = self.nextIndex
        self.nextIndex += 1
        self.swapLabel4 = self.nextIndex
        self.nextIndex += 1
        self.descriptLabel1 = self.nextIndex
        self.nextIndex += 1
        self.descriptLabel2 = self.nextIndex
        self.nextIndex += 1
        addCmd("CreateLabel", self.descriptLabel1, "", 20, 10,  0)
        # print(AnimationCommands)
        # self.animationManager.StartNewAnimation(self.commands)
        # self.animationManager.skipForward()
        # self.animationManager.clearHistory()

    def setIndexHighlight(self, index, highlightVal):
        addCmd("SetHighlight", self.circleObjs[index], highlightVal)
        addCmd("SetHighlight", self.arrayRects[index], highlightVal)


# -----------------------------------------------------------
# Initialize Flask Backend
# -----------------------------------------------------------
minH = Blueprint('minH', __name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
CORS(minH)
myHeap = minHeap()


# -----------------------------------------------------------
# API for different minHeap methods
#
# 1. Insert: /minHeap/insert/<value>
# 2. Remove Smallest: /minHeap/rMin
# 3. Clear Heap: /minHeap/clear
# 4. Build Heap: /minHeap/build
#
# -----------------------------------------------------------
@minH.route('/', methods=['GET'])
def create_circle():
    objectId, value = "1", "10"
    initX, initY = "0", "0"
    action = {"CreateCircle": objectId + "<;>" +
              value + "<;>" + initX + "<;>" + initY}
    return jsonify(action)

@minH.route('/minHeap/reset', methods=['GET'])
def reset():
    myHeap.reset()
    return json.dumps(["My heap is reloaded!!", "myHeap nextIndex", myHeap.nextIndex])

@minH.route('/minHeap/insert/<value>', methods=['GET'])
def getInsert(value):
    myHeap.insert(value)
    return json.dumps(AnimationCommands)


@minH.route('/minHeap/rMin', methods=['GET'])
def getRemoveMin():
    myHeap.removeMin()
    # tree = session['tree']
    return json.dumps(AnimationCommands)


@minH.route('/minHeap/clear', methods=['GET'])
def getClear():
    myHeap.clear()
    # tree = session['tree']
    return json.dumps(AnimationCommands)


@minH.route('/minHeap/build', methods=['GET'])
def getBuild(steps=10, Random=True):
    myHeap.buildHeap(steps, Random)
    return json.dumps(AnimationCommands)
