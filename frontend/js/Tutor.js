// Initialization
const DS_Prob = ['BST', 'RBT', 'MINH', 'MAXH', 'BST', 'RBT', 'MINH', 'MAXH'];
const DS_Map = {'BST': 'bst', 'RBT': 'rbTree', 'MINH': 'minHeap', 'MAXH': 'maxHeap'};

const bstButton = document.getElementById("bst");
const minHeapButton = document.getElementById("minHeap");
const maxHeapButton = document.getElementById("maxHeap");
const rbTreeButton = document.getElementById("rbTree");
const replayButton = document.getElementById("replay");
let cur_prob = 0;
let cur_commands = "";
// let 

// Fisher-Yates Shuffle
const shuffle = (array) => {
    for(let i=array.length-1; i > 0; i--){
        let j = Math.floor(Math.random()*(i+1));
        [array[i], array[j]] = [array[j], array[i]]
    }
}

const reply_click = (id) => {
    if (DS_Map[DS_Prob[cur_prob]] === id && cur_prob<DS_Prob.length-1){
        console.log("Correct", cur_prob);
        cur_prob += 1
        cur_commands = "";
        renderClear();
        renderProb(cur_prob);
    }
    else if(cur_prob == 7){
        console.log("Finish");
        let finish = document.getElementById("Finish");
        let x = document.getElementById("hide");
        let z = document.getElementById("option");
        if (x.style.display == "block") {
            x.style.display = "none";
          }
          if (z.style.display == "block") {
            z.style.display = "none";
          }
          if (finish.style.display == "none") {
            finish.style.display = "block";
          }
    }
}

// Random the DS question and check the answer
const startProblem = () => {

    // Shuffle the Data Structure Questions
    shuffle(DS_Prob);
    console.log(DS_Prob);
    renderProb(cur_prob);
};

const replay = () => {
    renderReplay(cur_prob);
}

const renderReplay = (ind) => {
    renderClear();
    const OM = new ObjectManager();
    // const AM = new AnimationManager(OM, document, DS_Prob[ind]);
    const AM = new AnimationManager(OM, document, "BST");
    AM.DIYMode = false;

    // let cur = "/" + DS_Map[DS_Prob[ind]];
    let cur = "/" +  "bst";
    console.log(cur);
    // Reset Everytime
    fetch( cur + "/reset")
    .then(function (response) {
        return response.json();
    })
    .then(function (myJson) {
        console.log(myJson);
    });
    AM.StartNewAnimation(cur_commands);
}

const renderProb = (ind) => {
    renderNum(ind);
    const OM = new ObjectManager();
    // const AM = new AnimationManager(OM, document, DS_Prob[ind]);
    const AM = new AnimationManager(OM, document, "BST");
    AM.DIYMode = false;

    // let cur = "/" + DS_Map[DS_Prob[ind]];
    let cur = "/" +  "bst";
    console.log(cur);
    // Reset Everytime
    fetch( cur + "/reset")
    .then(function (response) {
        return response.json();
    })
    .then(function (myJson) {
        console.log(myJson);
    });

    fetch( cur + "/build")
    .then(function (response) {
        var myJson = response.json();
        console.log(myJson, myJson.length);
        return myJson;
    })
    .then(function (myJson) {
        console.log(myJson);
        cur_commands = myJson;
        AM.StartNewAnimation(cur_commands);
    });
}

const renderClear = () => {
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
}

const renderNum = (ind) => {
    let rendernum = "Question: " + (ind+1).toString() + "/8";
    document.getElementById("question-index").innerHTML = rendernum;
}

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

  replayButton.addEventListener("click", replay);