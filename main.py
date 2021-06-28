from flask import Flask, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import os, json
from api.bst import bst
from api.minHeap import minH
from api.maxHeap import maxH
from api.rbTree import rbt

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello index"

app.register_blueprint(bst)
app.register_blueprint(minH)
app.register_blueprint(maxH)
app.register_blueprint(rbt)
