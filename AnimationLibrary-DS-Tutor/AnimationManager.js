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

  //TODO
  this.startNextBlock = async function (commandsBlock) {
    return new Promise((resolve) => {
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
          if (parseInt(nextCommand[1]) % 2 == 0) {
            this.animatedObjects.setNodePosition(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[2]),
              parseInt(nextCommand[3])
            );
            //use tweenjs to draw animation in 500ms (this.tweenjsAniamtionTime)
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].move(
              this.animatedObjects.stage,
              this.tweenjsAnimationTime
            );
          }
          // the target is highlight circle
          else {
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
        } else if (nextCommand[0].toUpperCase() == "CREATEHIGHLIGHTCIRCLE") {
          //TODO
          //or don't do
        } else if (nextCommand[0].toUpperCase() == "DELETE") {
          //TODO
          //if target is highlight circle
          if (parseInt(nextCommand[1]) % 2 != 0) {
          }
          //TODO
          //if target is node
          else {
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
            this.animatedObjects.Edges[i][j].draw(this.animatedObjects.stage);
          }
        }
      }
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
    //enable back btns bar
    this.disableBtns();

    //initialize
    this.commands = commands;
    this.AnimationBlocks = [];
    var block = [];
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
      var tweenjsAnimationTime = await this.delay(this.tweenjsAnimationTime);
      var res2 = await this.drawConnection();
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
