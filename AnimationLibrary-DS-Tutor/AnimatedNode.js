var AnimatedNode = function (objectID, objectLabel) {
  this.objectID = objectID;
  this.objectLabel = objectLabel;
  this.x = 0;
  this.y = 0;
  this.radius = 20;
  this.onScene = false; // is it on canvas ready?
  this.isNode = true;
  this.isRect = false;

  this.nodeColor = "#D65A31";
  this.textColor = "#fff";

  // create node (circle + text) in this.node
  var circle = new createjs.Shape();
  circle.graphics.beginFill(this.nodeColor).drawCircle(0, 0, this.radius);
  this.circle = circle;

  var text = new createjs.Text(
    this.objectLabel.toString(),
    "15px Arial",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
  });
  this.text = text;

  //highlight circle
  var highlight = new createjs.Shape();
  highlight.graphics
    .setStrokeStyle(5)
    .beginStroke("#fdf912")
    .drawCircle(this.x, this.y, this.radius);
  this.highlightCircle = highlight;

  var node = new createjs.Container();
  node.addChild(this.circle, this.text);
  this.node = node;
};

AnimatedNode.prototype.constructor = AnimatedNode;

AnimatedNode.prototype.setXY = function (new_x, new_y) {
  this.x = new_x;
  this.y = new_y;
};

AnimatedNode.prototype.setNodeColor = function (hexString, stage) {
  //remove first
  stage.removeChild(this.node);
  //update
  this.nodeColor = hexString;

  var circle = new createjs.Shape();
  circle.graphics.beginFill(this.nodeColor).drawCircle(0, 0, this.radius);
  this.circle = circle;

  var node = new createjs.Container();
  node.addChild(this.circle, this.text);
  this.node = node;

  //draw
  this.node.x = this.x;
  this.node.y = this.y;
  stage.addChild(this.node);
  stage.update();
};

AnimatedNode.prototype.setTextColor = function (hexString) {
  this.textColor = hexString;

  var text = new createjs.Text(
    this.objectLabel.toString(),
    "15px Arial",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
  });
  this.text = text;

  var node = new createjs.Container();
  node.addChild(this.circle, this.text);
  this.node = node;
};

AnimatedNode.prototype.setText = function (newText, stage) {
  stage.removeChild(this.node);
  this.objectLabel = newText;

  var text = new createjs.Text(
    this.objectLabel.toString(),
    "15px Arial",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
  });
  this.text = text;

  var node = new createjs.Container();
  node.addChild(this.circle, this.text);
  this.node = node;

  //update
  this.onScene = true;
  this.node.x = this.x;
  this.node.y = this.y;
  stage.addChild(this.node);
  stage.update();
};

AnimatedNode.prototype.highlight = function (stage, node, highlightCircle, ms) {
  node.addChild(highlightCircle);
  stage.update();
  // theNode = this.node;
  // theHighlightCircle = this.highlightCircle;
  setTimeout(function () {
    //stage.removeChild(g);
    node.removeChild(highlightCircle);
    stage.update();
  }, ms);
};

AnimatedNode.prototype.draw = function (stage) {
  this.onScene = true;
  this.node.x = this.x;
  this.node.y = this.y;
  stage.addChild(this.node);
  stage.update();
};

AnimatedNode.prototype.remove = function (stage) {
  this.onScene = false;
  stage.removeChild(this.node);
  stage.update();
};

AnimatedNode.prototype.move = function (stage, ms) {
  createjs.Tween.get(this.node, { loop: false }).to(
    { x: this.x, y: this.y },
    ms,
    createjs.Ease.getPowInOut(4)
  );

  createjs.Ticker.interval = 5;
  createjs.Ticker.addEventListener("tick", stage);
  setTimeout(function () {
    createjs.Ticker.removeEventListener("tick", stage);
  }, ms);
};
