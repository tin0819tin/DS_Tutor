var Line = function (fromNode, toNode) {
  //both AnimatedNode object
  this.fromNode = fromNode;
  this.toNode = toNode;

  this.color = "#000";
  this.onScene = false;
  this.toBeRemoved = false;

  var line = new createjs.Shape();
  line.graphics.setStrokeStyle(3).beginStroke("rgba(0,0,0,1)");
  var from_x = this.fromNode.x;
  var from_y = this.fromNode.y;
  var to_x = this.toNode.x;
  var to_y = this.toNode.y;
  line.graphics.moveTo(from_x, from_y);
  line.graphics.lineTo(to_x, to_y);
  line.graphics.endStroke();
  this.line = line;
};

Line.prototype.setColor = function (hexString) {
  this.color = hexString;
};

Line.prototype.draw = function (stage) {
  this.onScene = true;
  var line = new createjs.Shape();
  line.graphics.setStrokeStyle(3).beginStroke("rgba(0,0,0,1)");
  var from_x = this.fromNode.x;
  var from_y = this.fromNode.y;
  var to_x = this.toNode.x;
  var to_y = this.toNode.y;
  line.graphics.moveTo(from_x, from_y);
  line.graphics.lineTo(to_x, to_y);
  line.graphics.endStroke();
  this.line = line;
  stage.addChildAt(this.line, 0);
  stage.update();
};

Line.prototype.remove = function (stage) {
  this.onScene = false;
  stage.removeChild(this.line);
  stage.update();
};
