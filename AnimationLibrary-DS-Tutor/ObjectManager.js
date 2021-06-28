function ObjectManager() {
  this.Nodes = [];
  this.Edges = [];
  this.BackEdges = [];
  this.highlightList = [];
  this.stage = new createjs.Stage("canvas");

  //TODO
  this.draw = function () {};

  this.addNodeObject = function (objectID, objectLabel) {
    if (this.Nodes[objectID] != null && this.Nodes[objectID] != undefined) {
      throw (
        "addNodeObject:Object with same ID (" +
        String(objectID) +
        ") already Exists!"
      );
    }
    var newNode = new AnimatedNode(objectID, objectLabel);
    this.Nodes[objectID] = newNode;
  };

  this.setNodePosition = function (objectID, newX, newY) {
    this.Nodes[objectID].setXY(newX, newY);
  };

  this.addLabelObject = function (objectID, objectLabel) {
    if (this.Nodes[objectID] != null && this.Nodes[objectID] != undefined) {
      throw new Error("addLabelObject: Object Already Exists!");
    }
    var newLabel = new AnimatedLabel(objectID, objectLabel);
    this.Nodes[objectID] = newLabel;
  };

  //not used
  this.pulsehighlight;

  //not used
  this.addHighlightNode = function (node) {
    this.highlightList.push(node);
  };

  //not used
  this.clearHighlightList = function () {
    this.highlightList = [];
  };

  //not used
  //highlight all nodes in this.highlightList //used in OM.draw()
  this.sequenceHighlight = function (ArrayOfNodes, stage) {
    var i = 0;
    createjs.Ticker.addEventListener("tick", handleTick);
    createjs.Ticker.framerate = 1;
    function handleTick() {
      if (i == ArrayOfNodes.length - 1) {
        createjs.Ticker.removeEventListener("tick", handleTick);
      }
      ArrayOfNodes[i].highlight(stage);
      i++;
    }
  };

  this.connectEdge = function (objectIDfrom, objectIDto) {
    var fromObj = this.Nodes[objectIDfrom];
    var toObj = this.Nodes[objectIDto];
    if (fromObj == null || toObj == null) {
      throw "Tried to connect two nodes, one didn't exist!";
    }
    var l = new Line(fromObj, toObj);
    if (
      this.Edges[objectIDfrom] == null ||
      this.Edges[objectIDfrom] == undefined
    ) {
      this.Edges[objectIDfrom] = [];
    }
    if (
      this.BackEdges[objectIDto] == null ||
      this.BackEdges[objectIDto] == undefined
    ) {
      this.BackEdges[objectIDto] = [];
    }
    this.Edges[objectIDfrom].push(l);
    this.BackEdges[objectIDto].push(l);
  };

  //for highlightCircle
  this.addHighlightCircle = function (objectID) {
    if (this.Nodes[objectID] != null && this.Nodes[objectID] != undefined) {
      throw (
        "addHighlightCircle: Object with same ID (" +
        String(objectID) +
        ") already Exists!"
      );
    }
    var newHighlightCircle = new AnimatedHighlightCircle(objectID);
    this.Nodes[objectID] = newHighlightCircle;
  };

  this.removeHighlightCircle = function (objectID) {
    if (this.Nodes[objectID] == null || this.Nodes[objectID] == undefined) {
      throw (
        "removeHighlightCircle: Object with same ID (" +
        String(objectID) +
        ") already does not Exists!"
      );
    }

    this.Nodes[objectID].remove(this.stage);
    this.Nodes[objectID] = null;
  };

  this.setCirclePosition = function (objectID, new_x, new_y) {
    this.Nodes[objectID].setXY(new_x, new_y);
  };
}
