// Initialization
const DS_Prob = ['BST', 'RBT', 'MINH', 'MAXH', 'BST', 'RBT', 'MINH', 'MAXH'];
const DS_Map = {'BST': 'bst', 'RBT': 'rbTree', 'MINH': 'minHeap', 'MAXH': 'maxHeap'};

const bstButton = document.getElementById("bst");
const minHeapButton = document.getElementById("minHeap");
const maxHeapButton = document.getElementById("maxHeap");
const rbTreeButton = document.getElementById("rbTree");
const replayButton = document.getElementById("replay");
const card = document.getElementById("card");
let cur_prob = 0;
let cur_commands = "";

// Fisher-Yates Shuffle
const shuffle = (array) => {
    for(let i=array.length-1; i > 0; i--){
        let j = Math.floor(Math.random()*(i+1));
        [array[i], array[j]] = [array[j], array[i]]
    }
}

// Decide whether the click is the right answer
const reply_click = (id) => {
    if (DS_Map[DS_Prob[cur_prob]] === id && cur_prob<DS_Prob.length-1){
        console.log("Correct", cur_prob);
        cur_prob += 1
        cur_commands = "";
        renderClear();
        disableBtn();
        console.log("Button has been disabled!")
        renderProb(cur_prob);
        // Enable in AM
    }
    else if(DS_Map[DS_Prob[cur_prob]] !== id){
        card.classList.remove('card-hidden');
        setTimeout(function() {
            card.classList.add('card-hidden');
        }, 1250);
    }
    else if(DS_Map[DS_Prob[cur_prob]] === id && cur_prob == 7){
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

// Disable the button when rendering
const disableBtn = () => {
    bstButton.disabled = true;
    minHeapButton.disabled = true;
    maxHeapButton.disabled = true;
    rbTreeButton.disabled = true;
    replayButton.disabled = true;

    // bstButton.classList.add('btns-disable');
    bstButton.classList.remove('option-btn-dark-hover');
    // minHeapButton.classList.add('tutor-btns-disable');
    minHeapButton.classList.remove('option-btn-dark-hover');
    // maxHeapButton.classList.add('tutor-btns-disable');
    maxHeapButton.classList.remove('option-btn-dark-hover');
    // rbTreeButton.classList.add('tutor-btns-disable');
    rbTreeButton.classList.remove('option-btn-dark-hover');
    replayButton.classList.add('tutor-btns-disable');
    replayButton.classList.remove('replay-btn-hover');
}

const enableBtn = () => {
    bstButton.disabled = false;
    minHeapButton.disabled = false;
    maxHeapButton.disabled = false;
    rbTreeButton.disabled = false;
    replayButton.disabled = false;

    bstButton.classList.add('option-btn-dark-hover');
    minHeapButton.classList.add('option-btn-dark-hover');
    maxHeapButton.classList.add('option-btn-dark-hover');
    rbTreeButton.classList.add('option-btn-dark-hover');
    replayButton.classList.remove('tutor-btns-disable');
    replayButton.classList.add('replay-btn-hover');
}

// Random the DS question and start the first question
const startProblem = () => {

    // Shuffle the Data Structure Questions
    shuffle(DS_Prob);
    console.log(DS_Prob);
    disableBtn();
    console.log("Button has been disabled!")
    renderProb(cur_prob);
    // Enable in AM
};


// Render the replayed Data Structure
const replay = () => {
    disableBtn();
    console.log("Button has been disabled!")
    renderProb(cur_prob);
    // Enable in AM
}

// Render the replayed Data Structure
const renderReplay = (ind) => {
    renderClear();
    const OM = new ObjectManager();
    const AM = new AnimationManager(OM, document, DS_Prob[ind]);
    // const AM = new AnimationManager(OM, document, "BST");
    AM.DIYMode = false;

    let cur = "/" + DS_Map[DS_Prob[ind]];
    // let cur = "/" +  "bst";
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


// Render the Data Structure
const renderProb = (ind) => {
    renderNum(ind);
    const OM = new ObjectManager();
    const AM = new AnimationManager(OM, document, DS_Prob[ind]);
    // const AM = new AnimationManager(OM, document, "BST");
    AM.DIYMode = false;

    let cur = "/" + DS_Map[DS_Prob[ind]];
    // let cur = "/" +  "bst";
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

// Clear the Canvas
const renderClear = () => {
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
}

// Render Question index
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

// Replay Event Listener
replayButton.addEventListener("click", replay);