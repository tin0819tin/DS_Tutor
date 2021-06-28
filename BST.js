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
