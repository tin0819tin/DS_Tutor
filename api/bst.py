from flask import Flask, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
CORS(app)

@app.route('/', methods=['GET'] )
def create_circle():
    objectId, value = "1", "10"
    initX, initY = "0", "0" 
    action = {"CreateCircle" : objectId + "<;>" + value + "<;>" + initX + "<;>" + initY }
    return  jsonify(action)

@app.route('/set/<value>' )
def setsession(value):
    tree = BST()
    tree.insert(value)
    session['tree'] = 'TREE'
    return  'ok'

@app.route('/get', methods=['GET'] )
def getsession():
    tree = session['tree']
    return tree


class BST():

    def __init__(self):
        self.root = None
    
    def insert(self, value):
        self.left = BSTNode(value)
    

class BSTNode():

    def __init__(self, key):
        self.value = key
        self.left_child = None
        self.right_child = None

# if __name__ == "__main__":
#     app.run(debug=True)