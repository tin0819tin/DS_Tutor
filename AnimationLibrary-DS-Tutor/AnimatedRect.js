function AnimatedRect(objectID, val, w, h, x, y) {
  this.objectID = objectID;
  this.label = val;
  this.x = x;
  this.y = y;
  this.width = w;
  this.height = h;
  this.onScene = true; // useless, always on scene

  this.backgroundColor = "rgba(255, 255, 255, 0.5)";
  this.textColor = "#000";

  //create text & rectangle
  var rect = new createjs.Shape();
  rect.graphics
    .beginFill(this.backgroundColor)
    .drawRect(this.x, this.y, this.width, this.height);
  this.rect = rect;

  var border = new createjs.Shape();
  border.graphics
    .setStrokeStyle(2)
    .beginStroke("#000")
    .drawRect(this.x, this.y, this.width, this.height);
  this.border = border;

  var text = new createjs.Text(
    this.label.toString(),
    "12px Haettenschweiler",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
    x: this.x + this.width / 2,
    y: this.y + this.height / 2,
  });
  this.text = text;

  var rectangle = new createjs.Container();
  rectangle.addChild(this.rect, this.border, this.text);
  this.rectangle = rectangle;

  this.setXY = function (newX, newY) {
    this.x = newX;
    this.y = newY;
  };

  this.draw = function (stage) {
    stage.addChildAt(this.rectangle, 0);
    stage.update();
  };

  this.setText = function (newText, stage) {
    //remove old rectangle
    stage.removeChild(this.rectangle);
    //store new text
    this.label = newText;

    var text = new createjs.Text(
      this.label.toString(),
      "12px Haettenschweiler",
      this.textColor
    );
    text.set({
      textAlign: "center",
      textBaseline: "middle",
      x: this.x + this.width / 2,
      y: this.y + this.height / 2,
    });
    this.text = text;

    var rectangle = new createjs.Container();
    rectangle.addChild(this.rect, this.border, this.text);
    this.rectangle = rectangle;

    // update
    stage.addChildAt(this.rectangle, 0);
    stage.update();
  };
}
