// Initialization
let DS = [];
const OM = new ObjectManager();
const AM = new AnimationManager(OM, document, "BST");
AM.DIYMode = false;

// Show the Canvas and start questions

const showCanvas = () => {
  let x = document.getElementById("hide");
  let y = document.getElementById("Init");
  let z = document.getElementById("option");
  console.log(x, y);
  if (x.style.display == "none") {
    x.style.display = "block";
  }
  if (z.style.display == "none") {
    z.style.display = "block";
  }
  if (y.style.display !== "none") {
    y.style.display = "none";
  }
  startProblem();
};

// Random the DS question and check the answer
const startProblem = () => {
  //First reset
  fetch("/bst/reset")
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      console.log(myJson);
    });

  fetch("/bst/build")
    .then(function (response) {
      var myJson = response.json();
      console.log(myJson, myJson.length);
      return myJson;
    })
    .then(function (myJson) {
      console.log(myJson);
      // var commands = JSON.parse(myJson)
      AM.StartNewAnimation(myJson);
    });
};
