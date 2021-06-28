var AnimatedHighlightCircle = function (objectID, init_x, init_y) {
  //create & set
  this.objectID = objectID;
  this.x = init_x;
  this.y = init_y;
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
