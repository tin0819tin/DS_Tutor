var Line = function (fromNode, toNode) {
  //both AnimatedNode object
  this.fromNode = fromNode;
  this.toNode = toNode;

  this.color = "#000";
  this.onScene = false;

  this.line = new createjs.Shape();
  this.line.graphics.setStrokeStyle(3).beginStroke("rgba(0,0,0,1)");
};

Line.prototype.setColor = function (hexString) {
  this.color = hexString;
};

Line.prototype.draw = function (stage) {
  this.onScene = true;
  this.line.graphics.moveTo(this.fromNode.x, this.fromNode.y);
  this.line.graphics.lineTo(this.toNode.x, this.toNode.y);
  this.line.graphics.endStroke();
  stage.addChildAt(this.line, 0);
  stage.update();
};

Line.prototype.remove = function (stage) {
  this.onScene = false;
  stage.removeChild(this.line);
  stage.update();
};
