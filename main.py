from flask import Flask, jsonify, session, render_template
from flask_cors import CORS
from datetime import timedelta
import os, json
from api.bst import bst
from api.minHeap import minH
from api.maxHeap import maxH
from api.rbTree import rbt

app = Flask(__name__, template_folder="ds_html", static_folder="frontend")
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bst')
def BST():
    return render_template('BST.html')

app.register_blueprint(bst)
app.register_blueprint(minH)
app.register_blueprint(maxH)
app.register_blueprint(rbt)
