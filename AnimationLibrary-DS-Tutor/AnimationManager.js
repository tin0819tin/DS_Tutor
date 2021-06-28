function AnimationManager(objectManager, document) {
  // Holder for all animated objects.
  // All animation is done by manipulating objects in\
  // this container
  this.animatedObjects = objectManager;

  //this.commads store input array of commands from flask
  //AnimationBlocks store processed commands, array of array of command string
  this.commands = [];
  this.AnimationBlocks = [];

  //interval between blocks
  //Tweenjs animation time
  this.blocksInterval = 250;
  this.tweenjsAnimationTime = 500;

  //handle delete case
  this.deleteCase = 0;

  //set NULL list
  this.NodesNullList = [];
  this.EdgesNullList = [];
  this.BackEdgesNullList = [];

  //TODO
  this.startNextBlock = async function (commandsBlock) {
    return new Promise((resolve) => {
      //init
      var i = 0;

      //while loop, do all commands

      while (i < commandsBlock.length) {
        var nextCommand = commandsBlock[i].split("<;>");

        //type of commands
        if (nextCommand[0].toUpperCase() == "CREATECIRCLE") {
          //record
          /*
          [1]: objectID
          [2]: label
          [3]: x
          [4]: y
          */
          this.animatedObjects.addNodeObject(
            parseInt(nextCommand[1]),
            parseInt(nextCommand[2])
          );
          if (nextCommand.length > 4) {
            this.animatedObjects.setNodePosition(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[3]),
              parseInt(nextCommand[4])
            );
          }
          //draw
          this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
            this.animatedObjects.stage
          );
        } else if (nextCommand[0].toUpperCase() == "CONNECT") {
          //record
          /*
          [1]: objectID of fromNode 
          [2]: objectID of toNode
          */
          this.animatedObjects.connectEdge(
            parseInt(nextCommand[1]),
            parseInt(nextCommand[2])
          );
          //draw later in drawConnection
        } else if (nextCommand[0].toUpperCase() == "SETHIGHLIGHT") {
          //record & draw
          /*
          [1]: objectID
          */
          if (parseInt(nextCommand[2]) == 1) {
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].highlight(
              this.animatedObjects.stage,
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].node,
              this.animatedObjects.Nodes[parseInt(nextCommand[1])]
                .highlightCircle,
              this.blocksInterval + 250
            );
          }
        } else if (nextCommand[0].toUpperCase() == "MOVE") {
          //record
          /*
          [1]: objectID
          [2]: new_x
          [3]: new_y
          */

          // if the target is node object
          if (
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].isNode == true
          ) {
            this.animatedObjects.setNodePosition(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[2]),
              parseInt(nextCommand[3])
            );
            //remove attach line first?
            //use tweenjs to draw animation in 500ms (this.tweenjsAniamtionTime)
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].move(
              this.animatedObjects.stage,
              this.tweenjsAnimationTime
            );
          }
          // the target is highlight circle
          else {
            this.animatedObjects.setCirclePosition(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[2]),
              parseInt(nextCommand[3])
            );
            //use tweenjs to draw animation in 500ms this.tweenjsAniamtionTime)
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].move(
              this.animatedObjects.stage,
              this.tweenjsAnimationTime
            );
          }
        } else if (nextCommand[0].toUpperCase() == "CREATELABEL") {
          //record
          /* 
          [1]: objectID
          [2]: objectLabel
          */
          this.animatedObjects.addLabelObject(
            parseInt(nextCommand[1]),
            nextCommand[2]
          );
          //draw
          this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
            this.animatedObjects.stage
          );
        } else if (nextCommand[0].toUpperCase() == "SETTEXT") {
          //record & draw
          /*
          [1]: objectID
          [2]: new text
          */
          this.animatedObjects.Nodes[parseInt(nextCommand[1])].setText(
            nextCommand[2],
            this.animatedObjects.stage
          );

          //which delete case?
          if (nextCommand[2].includes("Node to delete has two child") == true) {
            this.deleteCase = 4;
          } else if (
            nextCommand[2].includes("Node to delete is a leaf.") == true
          ) {
            this.deleteCase = 1;
          } else if (
            nextCommand[2].includes("Node to delete has no left child.") == true
          ) {
            this.deleteCase = 2;
          } else if (
            nextCommand[2].includes("Node to delete has no right child.") ==
            true
          ) {
            this.deleteCase = 3;
          }
        } else if (nextCommand[0].toUpperCase() == "CREATEHIGHLIGHTCIRCLE") {
          //record
          /*
          [1]: objectID
          [3]: x
          [4]: y
          */
          // ID一定是奇數嗎？

          this.animatedObjects.addHighlightCircle(parseInt(nextCommand[1]));
          if (nextCommand.length > 4) {
            this.animatedObjects.setCirclePosition(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[3]),
              parseInt(nextCommand[4])
            );
          }
          //draw
          this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
            this.animatedObjects.stage
          );
        } else if (nextCommand[0].toUpperCase() == "DELETE") {
          /*
          [1]: objectID
          */
          //if target is highlight circle
          if (
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].isNode == false
          ) {
            this.animatedObjects.removeHighlightCircle(
              parseInt(nextCommand[1])
            );
          }
          //if target is node
          else {
            //TODO
            /*
            case1: delete leaf
            case2: delete node has no left child (one right child)
            case3: delete node has no right child (one left child)
            case4: delete node has 2 children
            */
            if (this.deleteCase == 1) {
              //remove attach edge from stage & marked toBeRemoved true
              this.animatedObjects.BackEdges[
                parseInt(nextCommand[1])
              ][0].remove(this.animatedObjects.stage);
              this.animatedObjects.BackEdges[
                parseInt(nextCommand[1])
              ][0].toBeRemoved = true;
              //remove from BackEdges list
              // var removeEdge =
              //   this.animatedObjects.BackEdges[parseInt(nextCommand[1])][0];
              this.BackEdgesNullList.push(parseInt(nextCommand[1]));
              //remove from Edges list
              /*
                Do it in drawConnection function by detect toBeRemoved == true
              */
              //remove node and set null
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].remove(
                this.animatedObjects.stage
              );
              this.NodesNullList.push(parseInt(nextCommand[1]));
            } else if (this.deleteCase == 2) {
            }
          }
        }

        i = i + 1;
      }
      resolve("end block ");
    });
  };

  this.drawConnection = function () {
    return new Promise((resolve) => {
      for (var i = 0; i < this.animatedObjects.Edges.length; i++) {
        if (
          this.animatedObjects.Edges[i] != null &&
          this.animatedObjects.Edges[i] != undefined
        ) {
          for (var j = 0; j < this.animatedObjects.Edges[i].length; j++) {
            if (this.animatedObjects.Edges[i][j].toBeRemoved == false) {
              if (this.animatedObjects.Edges[i][j].onScene == false) {
                this.animatedObjects.Edges[i][j].draw(
                  this.animatedObjects.stage
                );
              } else if (this.animatedObjects.Edges[i][j].onScene == true) {
                this.animatedObjects.Edges[i][j].remove(
                  this.animatedObjects.stage
                );
                this.animatedObjects.Edges[i][j].draw(
                  this.animatedObjects.stage
                );
              }
            } else if (this.animatedObjects.Edges[i][j].toBeRemoved == true) {
              //remove edge in Edge list
              this.animatedObjects.Edges[i].splice(j, 1);
            }
          }
        }
      }
      resolve("");
    });
  };

  this.setNULL = function () {
    return new Promise((resolve) => {
      //set node or edge objects null
      if (this.NodesNullList.length > 0) {
        for (var i = 0; i < this.NodesNullList.length; i++) {
          var objectID = this.NodesNullList[i];
          this.animatedObjects.Nodes[objectID] = null;
        }
      }
      if (this.EdgesNullList.length > 0) {
        for (var i = 0; i < this.EdgesNullList.length; i++) {
          var objectID = this.EdgesNullList[i];
          this.animatedObjects.Edges[objectID] = null;
        }
      }
      if (this.BackEdgesNullList.length > 0) {
        for (var i = 0; i < this.BackEdgesNullList.length; i++) {
          var objectID = this.BackEdgesNullList[i];
          this.animatedObjects.BackEdges[objectID] = null;
        }
      }
      //init
      this.NodesNullList = [];
      this.EdgesNullList = [];
      this.BackEdgesNullList = [];
      resolve("");
    });
  };

  this.sleep = function (ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };

  this.delay = async function (ms) {
    return this.sleep(ms).then((v) => "start block ");
  };

  //parse flask returned array of commands
  this.StartNewAnimation = async function (commands) {
    //disable btns bar
    this.disableBtns();

    //initialize
    this.commands = commands;
    this.AnimationBlocks = [];
    var block = [];
    this.deleteCase = 0;
    //parse commands, separated by "STEP<;>"
    for (var i = 0; i < commands.length; i++) {
      if (commands[i] == "Step<;>") {
        this.AnimationBlocks.push(block);
        block = [];
      } else {
        block.push(commands[i]);
      }
    }
    if (block.length >= 1) {
      this.AnimationBlocks.push(block);
    }

    console.log("Animation blocks after process:");
    console.log(this.AnimationBlocks);

    //use for-loop + await to do each blocks of animations
    for (var x = 0; x < this.AnimationBlocks.length; x++) {
      var delay1 = await this.delay(this.blocksInterval);
      console.log(delay1 + x);
      var res = await this.startNextBlock(this.AnimationBlocks[x]);
      var settingSomethingNull = await this.setNULL();
      var tweenjsAnimationTime = await this.delay(this.tweenjsAnimationTime);
      var res2 = await this.drawConnection();
      settingSomethingNull = "";
      tweenjsAnimationTime = "";
      console.log(res + res2 + x);
    }
    console.log("Finish animation!");
    //enable back btns bar
    this.enableBtns();
  };

  this.disableBtns = function () {
    document.getElementById("btns-bar").classList.add("btns-disable");
    document.getElementById("animation-text").innerHTML = "Start animation...";
    document.getElementById("hidden-text").classList.remove("text-disable");
  };

  this.enableBtns = function () {
    document.getElementById("btns-bar").classList.remove("btns-disable");
    document.getElementById("animation-text").innerHTML = "";
    document.getElementById("hidden-text").classList.add("text-disable");
  };
}
