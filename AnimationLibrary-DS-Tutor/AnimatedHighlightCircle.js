var AnimatedHighlightCircle = function (objectID) {
  //create
  this.objectID = objectID;
  this.x = 0;
  this.y = 0;
  this.radius = 20;

  //circle
  var highlight = new createjs.Shape();
  highlight.graphics
    .setStrokeStyle(5)
    .beginStroke("#FF3232")
    .drawCircle(this.x, this.y, this.radius);
  this.highlightCircle = highlight;
};
AnimatedHighlightCircle.prototype.constructor = AnimatedHighlightCircle;

//setXY

AnimatedHighlightCircle.prototype.setXY = function (new_x, new_y) {
  this.x = new_x;
  this.y = new_y;
};

//draw

AnimatedHighlightCircle.prototype.draw = function (stage) {
  this.highlightCircle.x = this.x;
  this.highlightCircle.y = this.y;
  stage.addChild(this.highlightCircle);
  stage.update();
};

//remove

AnimatedHighlightCircle.prototype.remove = function (stage) {
  stage.removeChild(this.highlightCircle);
  stage.update();
};

//move

AnimatedHighlightCircle.prototype.move = function (stage, ms) {
  createjs.Tween.get(this.highlightCircle, { loop: false }).to(
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
