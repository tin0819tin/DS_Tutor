function AnimatedLabel(objectID, objectLabel) {
  this.objectID = objectID;
  this.label = objectLabel; //show text
  this.x = 0;
  this.y = 450;
  this.width = 1000;
  this.height = 50;
  this.onScene = true; // useless, always on scene

  this.backgroundColor = "rgba(255, 255, 255, 0.5)";
  this.textColor = "#000";

  //create text & rectangle
  var rect = new createjs.Shape();
  rect.graphics
    .beginFill(this.backgroundColor)
    .drawRect(this.x, this.y, this.width, this.height);
  this.rect = rect;

  var text = new createjs.Text(
    this.label.toString(),
    "18px Haettenschweiler",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
    x: this.width / 2,
    y: 500 - this.height / 2 - 10,
  });
  this.text = text;

  var text_container = new createjs.Container();
  text_container.addChild(this.rect, this.text);
  this.status = text_container;

  this.draw = function (stage) {
    stage.addChild(this.status);
    stage.update();
  };

  this.setText = function (newText, stage) {
    //remove old text
    stage.removeChild(this.status);
    //store new text
    this.label = newText;

    var text = new createjs.Text(
      this.label.toString(),
      "18px Haettenschweiler",
      this.textColor
    );
    text.set({
      textAlign: "center",
      textBaseline: "middle",
      x: this.width / 2,
      y: 500 - this.height / 2 - 10,
    });
    this.text = text;

    var text_container = new createjs.Container();
    text_container.addChild(this.rect, this.text);
    this.status = text_container;

    // update
    stage.addChild(this.status);
    stage.update();
  };
}
