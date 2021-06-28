// ---- animation practice ----

// var node = new AnimatedNode(1, 3);
// node.setXY(800, 250);

// var stage = new createjs.Stage("canvas");

// function init() {
//   node.draw(stage);

//   createjs.Ticker.addEventListener("tick", handleTick);
//   createjs.Ticker.framerate = 30;
// }

// function handleTick(event) {
//   // Actions carried out each tick (aka frame)
//   node.setXY(node.x + 5, node.y + 5);
//   node.draw(stage);
//   if (node.x > stage.canvas.width) {
//     node.x = 0;
//   }
//   if (node.y > stage.canvas.height) {
//     node.y = 0;
//   }
//   stage.update(event);
// }

// ---- code below ----

var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document);

// ---- insert buttom event listener ----
$(function () {
  $("#insert").click(function () {
    var appdir = "/bst/insert/";
    var n = parseInt($("#insert-value").val());
    $.ajax({
      type: "GET",
      url: server + appdir + n,
    }).done(function (data) {
      //console.log(data);
      $("#insert-value").val("");
      var commands = JSON.parse(data);
      AM.StartNewAnimation(commands);
    });
  });
});

//---async test---
// function Foo(i) {
//   return new Promise((resolve) => {
//     setTimeout(function () {
//       resolve(i);
//     }, Math.random() * 1000);
//   });
// }

// async function Cool() {
//   for (var j = 0; j < 5; j++) {
//     var val = await Foo(j);
//     console.log(val);
//   }
//   console.log("done");
// }

// Cool();

var stage = new createjs.Stage("canvas");
node = new AnimatedHighlightCircle(2, 500, 250);
node.draw(stage);
node.setXY(800, 250);
node.move(stage, 1000);
