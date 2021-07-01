var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document, "MINH");
AM.DIYMode = true;

// ---- insert buttom event listener ----
$(function () {
  $("#insert").click(function () {
    var appdir = "/minHeap/insert/";
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

// ---- rMin buttom event listener ----
$(function () {
  $("#rMin").click(function () {
    var appdir = "/minHeap/rMin";
    $.ajax({
      type: "GET",
      url: server + appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      console.log(commands);
      //AM.StartNewAnimation(commands);
    });
  });
});

// ---- clear buttom event listener ----
$(function () {
  $("#clear").click(function () {
    var appdir = "/minHeap/clear";
    $.ajax({
      type: "GET",
      url: server + appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      console.log(commands);
      //AM.StartNewAnimation(commands);
    });
  });
});

// ---- build buttom event listener ----
$(function () {
  $("#build").click(function () {
    var appdir = "/minHeap/build";
    $.ajax({
      type: "GET",
      url: server + appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      console.log(commands);
      //AM.StartNewAnimation(commands);
    });
  });
});

// ------ test ----------
// var stage = new createjs.Stage("canvas");
// var rect = new AnimatedRect(0, "-INF", 30, 25, 30, 50);
// var text = new AnimatedHeapLabel(1, 1, 30, 70);
// var rect2 = new AnimatedRect(2, "", 30, 25, 60, 50);
// var text2 = new AnimatedHeapLabel(4, 2, 60, 70);
// text.draw(stage);
// rect.draw(stage);
// text2.draw(stage);
// rect2.draw(stage);
// rect.setText("123", stage);
