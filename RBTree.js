var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document, "RBT");
AM.DIYMode = true;

// ---- insert buttom event listener ----
$(function () {
  $("#insert").click(function () {
    var appdir = "/rbTree/insert/";
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

// ---- delete buttom event listener ----
$(function () {
  $("#delete").click(function () {
    var appdir = "/rbTree/delete/";
    var n = parseInt($("#delete-value").val());
    $.ajax({
      type: "GET",
      url: server + appdir + n,
    }).done(function (data) {
      //console.log(data);
      $("#delete-value").val("");
      var commands = JSON.parse(data);
      AM.StartNewAnimation(commands);
    });
  });
});

// ---- find buttom event listener ----
$(function () {
  $("#find").click(function () {
    var appdir = "/rbTree/find/";
    var n = parseInt($("#find-value").val());
    $.ajax({
      type: "GET",
      url: server + appdir + n,
    }).done(function (data) {
      //console.log(data);
      $("#find-value").val("");
      var commands = JSON.parse(data);
      AM.StartNewAnimation(commands);
    });
  });
});

// ---- print buttom event listener ----
$(function () {
  $("#print").click(function () {
    var appdir = "/rbTree/print";
    $.ajax({
      type: "GET",
      url: server + appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      AM.printMode = true;
      AM.StartNewAnimation(commands);
    });
  });
});
