var server = "http://127.0.0.1:5000";
var OM = new ObjectManager();
var AM = new AnimationManager(OM, document, "MINH");
AM.DIYMode = true;

if (window.performance) {
  console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD || performance.navigation.type == performance.navigation.TYPE_NAVIGATE) {
  console.info( "This page is reloaded" );
  fetch('/minHeap/reset').then(function(response) {
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
    var appdir = "/minHeap/insert/";
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

// ---- rMin buttom event listener ----
$(function () {
  $("#rMin").click(function () {
    var appdir = "/minHeap/rMin";
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
    var appdir = "/minHeap/clear";
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
    var appdir = "/minHeap/build";
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
