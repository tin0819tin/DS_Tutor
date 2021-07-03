var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document, "BST");
AM.DIYMode = true;

if (window.performance) {
  console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD || performance.navigation.type == performance.navigation.TYPE_NAVIGATE) {
  console.info( "This page is reloaded" );
  fetch('/bst/reset').then(function(response) {
			return response.json();
		  })
		  .then(function(myJson) {
			console.log(myJson);
		  });
}
else if(performance.navigation.type == performance.navigation.TYPE_BACK_FORWARD){
  window.location.reload();
}
else {
  console.info( "This page is not reloaded");
}

// ---- insert buttom event listener ----
$(function () {
  $("#insert").click(function () {
    var appdir = "/bst/insert/";
    var n = parseInt($("#insert-value").val());
    $.ajax({
      type: "GET",
      url: appdir + n,
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
    var appdir = "/bst/delete/";
    var n = parseInt($("#delete-value").val());
    $.ajax({
      type: "GET",
      url: appdir + n,
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
    var appdir = "/bst/find/";
    var n = parseInt($("#find-value").val());
    $.ajax({
      type: "GET",
      url: appdir + n,
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
    var appdir = "/bst/print";
    $.ajax({
      type: "GET",
      url: appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      AM.printMode = true;
      AM.StartNewAnimation(commands);
    });
  });
});

// ---- clear buttom event listener ----
$(function () {
  $("#clear").click(function () {
    var appdir = "/bst/clear";
    $.ajax({
      type: "GET",
      url:  appdir,
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
    var appdir = "/bst/build";
    $.ajax({
      type: "GET",
      url: appdir,
    }).done(function (data) {
      //console.log(data);
      var commands = JSON.parse(data);
      AM.StartNewAnimation(commands);
    });
  });
});
