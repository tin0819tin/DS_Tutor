var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document, "MAXH");
AM.DIYMode = true;

if (window.performance) {
  console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
  console.info( "This page is reloaded" );
  fetch('/maxHeap/reset').then(function(response) {
			return response.json();
		  })
		  .then(function(myJson) {
			console.log(myJson);
		  });
} else {
  console.info( "This page is not reloaded");
}

// ---- insert buttom event listener ----
$(function () {
  $("#insert").click(function () {
    var appdir = "/maxHeap/insert/";
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

// ---- rMax buttom event listener ----
$(function () {
  $("#rMax").click(function () {
    var appdir = "/maxHeap/rMax";
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

// ---- clear buttom event listener ----
$(function () {
  $("#clear").click(function () {
    var appdir = "/maxHeap/clear";
    $.ajax({
      type: "GET",
      url: appdir,
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
    var appdir = "/maxHeap/build";
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
