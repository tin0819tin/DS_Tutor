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
      AM.StartNewAnimation(commands);
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
      AM.clearMode = true;
      AM.StartNewAnimation(commands);
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
      AM.StartNewAnimation(commands);
    });
  });
});
