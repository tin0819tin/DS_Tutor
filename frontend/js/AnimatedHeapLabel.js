//heap array label
function AnimatedHeapLabel(objectID, objectLabel) {
  this.objectID = objectID;
  this.label = objectLabel;
  this.x = 0;
  this.y = 0;
  this.onScene = false;

  // set to "#d9dce0" to disapper
  // this.textColor = "#fff";
  this.textColor = "##d9dce0";

  var text = new createjs.Text(
    this.label.toString(),
    "15px Haettenschweiler",
    this.textColor
  );
  text.set({
    textAlign: "center",
    textBaseline: "middle",
    x: this.x,
    y: this.y,
  });
  this.text = text;

  this.draw = function (stage) {
    this.onScene = true;
    var text = new createjs.Text(
      this.label.toString(),
      "15px Haettenschweiler",
      this.textColor
    );
    text.set({
      textAlign: "center",
      textBaseline: "middle",
      x: this.x,
      y: this.y,
    });
    this.text = text;
    stage.addChild(this.text);
    stage.update();
  };

  this.remove = function (stage) {
    this.onScene = false;
    stage.removeChild(this.text);
    stage.update();
  };

  this.setXY = function (newX, newY) {
    this.x = newX;
    this.y = newY;
  };

  // not used?
  this.move = function (stage, ms) {
    createjs.Tween.get(this.text, { loop: false }).to(
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

  this.setText = function (newText, stage) {
    //remove old text
    stage.removeChild(this.text);
    //store new text
    this.label = newText;

    var text = new createjs.Text(
      this.label.toString(),
      "15px Haettenschweiler",
      this.textColor
    );
    text.set({
      textAlign: "center",
      textBaseline: "middle",
      x: this.x,
      y: this.y,
    });
    this.text = text;

    // update
    stage.addChild(this.text);
    stage.update();
  };
}
