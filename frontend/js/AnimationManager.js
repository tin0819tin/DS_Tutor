function AnimationManager(objectManager, document, dataStructure) {
  // Holder for all animated objects.
  // All animation is done by manipulating objects in\
  // this container
  this.animatedObjects = objectManager;

  // "BST", "MAXH", "MINH", "RBT"
  this.dataStructure = dataStructure;
  this.DIYMode = false;

  //node color when test mode
  this.testModeNodeColor = "#ff4d4d";

  //use for Print btns in BST, RBT
  this.printMode = false;
  this.printNullList = [];

  //use for clear function
  this.clearMode = false;

  //AnimationBlocks store processed commands, array of array of command string
  this.AnimationBlocks = [];

  //interval between blocks
  //Tweenjs animation time
  this.blocksInterval = 500;
  this.tweenjsAnimationTime = 500;

  //set NULL list
  this.NodesNullList = [];
  this.EdgesNullList = [];
  this.BackEdgesNullList = [];

  //to do each block animation
  //TODO
  this.startNextBlock = async function (commandsBlock) {
    return new Promise((resolve) => {
      //init
      var i = 0;

      //while loop, do all commands

      // --------------------------
      // the for loop inside must not use "i" for parameter, will cause bug
      // --------------------------

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

          // ------------
          // if test mode, scale x position by 0.9
          if (this.DIYMode == false) {
            nextCommand[3] = parseInt(nextCommand[3]) * 0.9;
          }
          // ------------

          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            if (
              this.dataStructure.toUpperCase() == "RBT" &&
              nextCommand[2] == "NULL\nLEAF"
            ) {
              //TODO
              nextCommand[2] = "NULL";
              this.animatedObjects.addNodeObject(
                parseInt(nextCommand[1]),
                nextCommand[2]
              );
            } else {
              this.animatedObjects.addNodeObject(
                parseInt(nextCommand[1]),
                parseInt(nextCommand[2])
              );
            }

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
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            if (nextCommand[2] == "") {
              this.animatedObjects.addNodeObject(
                parseInt(nextCommand[1]),
                nextCommand[2]
              );
            } else {
              this.animatedObjects.addNodeObject(
                parseInt(nextCommand[1]),
                parseInt(nextCommand[2])
              );
            }

            if (nextCommand.length > 4) {
              this.animatedObjects.setNodePosition(
                parseInt(nextCommand[1]),
                parseInt(nextCommand[3]),
                parseInt(nextCommand[4])
              );
            }
            // set heap node circle color
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].setNodeColor(
              this.testModeNodeColor,
              this.animatedObjects.stage
            );

            //draw
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
              this.animatedObjects.stage
            );
          }
        } else if (nextCommand[0].toUpperCase() == "CONNECT") {
          //record
          /*
          [1]: objectID of fromNode 
          [2]: objectID of toNode
          */
          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            this.animatedObjects.connectEdge(
              parseInt(nextCommand[1]),
              parseInt(nextCommand[2])
            );
            //draw later in drawConnection
          }
        } else if (nextCommand[0].toUpperCase() == "SETHIGHLIGHT") {
          //record & draw
          /*
          [1]: objectID
          */
          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            if (parseInt(nextCommand[2]) == 1) {
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].highlight(
                this.animatedObjects.stage,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].node,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])]
                  .highlightCircle,
                this.blocksInterval + 250
              );
            }
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            // is node
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].isNode ==
              true
            ) {
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].highlight(
                this.animatedObjects.stage,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].node,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])]
                  .highlightCircle,
                this.blocksInterval + 500
              );
            }
            // is rect
            else if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].isRect ==
              true
            ) {
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].highlight(
                this.animatedObjects.stage,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].rectangle,
                this.animatedObjects.Nodes[parseInt(nextCommand[1])]
                  .highlightRect,
                this.blocksInterval + 500
              );
            }
          }
        } else if (nextCommand[0].toUpperCase() == "MOVE") {
          //record
          /*
          [1]: objectID
          [2]: new_x
          [3]: new_y
          */

          // ------------
          // if test mode, scale x position by 0.9
          if (this.DIYMode == false) {
            nextCommand[2] = parseInt(nextCommand[2]) * 0.9;
          }
          // ------------

          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            // if the target is node object
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].isNode ==
              true
            ) {
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

              //remove all attach backedge
              //---------------------------
              // just for better visualization, not actually delete it, turn of this part won't affect
              if (
                this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                  null &&
                this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                  undefined
              ) {
                if (
                  this.animatedObjects.BackEdges[parseInt(nextCommand[1])][0] !=
                    null &&
                  this.animatedObjects.BackEdges[parseInt(nextCommand[1])][0] !=
                    undefined
                ) {
                  this.animatedObjects.BackEdges[
                    parseInt(nextCommand[1])
                  ][0].remove(this.animatedObjects.stage);
                }
              }
              //---------------------------
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
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            //move heap label object
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
        } else if (nextCommand[0].toUpperCase() == "CREATELABEL") {
          //record
          /* 
          [1]: objectID
          [2]: objectLabel
          [3]: x
          [4]: y
          */

          // ------------
          // if test mode, scale x position by 0.9
          if (this.DIYMode == false) {
            nextCommand[3] = parseInt(nextCommand[3]) * 0.9;
          }
          // ------------

          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            // if create status rectangle
            if (parseInt(nextCommand[1]) == 0) {
              //DIY mode
              if (this.DIYMode == true) {
                this.animatedObjects.addLabelObject(
                  parseInt(nextCommand[1]),
                  nextCommand[2]
                );
                //draw
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
                  this.animatedObjects.stage
                );
              }
              //test mode
              else if (this.DIYMode == false) {
                //do nothing
              }
            }

            // else do same thing as create node
            else {
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
            }
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            //target is status
            if (parseInt(nextCommand[1]) == 100) {
              //DIY mode
              if (this.DIYMode == true) {
                //record
                this.animatedObjects.addLabelObject(
                  parseInt(nextCommand[1]),
                  nextCommand[2]
                );
                //draw
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
                  this.animatedObjects.stage
                );
              }
              //test mode
              else if (this.DIYMode == false) {
                //do nothing
              }
            }

            // target is heap label
            else {
              //record
              this.animatedObjects.addHeapLabelObject(
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
              //(set #d9dce0 = disapper array)
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].textColor =
                "#d9dce0";

              //draw
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
                this.animatedObjects.stage
              );
            }
          }
        } else if (nextCommand[0].toUpperCase() == "SETTEXT") {
          //record & draw
          /*
          [1]: objectID
          [2]: new text
          */
          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != null &&
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != undefined
            ) {
              // target is status line
              if (parseInt(nextCommand[1]) == 0) {
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].setText(
                  nextCommand[2],
                  this.animatedObjects.stage
                );
              }
              // target is Node
              else {
                if (nextCommand[2] == "") {
                  nextCommand[2] = "0";
                }
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].setText(
                  parseInt(nextCommand[2]),
                  this.animatedObjects.stage
                );
              }
            }
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != null &&
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != undefined
            ) {
              //if target is status line
              if (parseInt(nextCommand[1]) == 100) {
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].setText(
                  nextCommand[2],
                  this.animatedObjects.stage
                );
              }
              // if target is Heap Rect or Heap Label
              else {
                if (
                  this.animatedObjects.Nodes[parseInt(nextCommand[1])] !=
                    null &&
                  this.animatedObjects.Nodes[parseInt(nextCommand[1])] !=
                    undefined
                ) {
                  this.animatedObjects.Nodes[parseInt(nextCommand[1])].setText(
                    nextCommand[2],
                    this.animatedObjects.stage
                  );
                }
              }
            }
          }
        } else if (nextCommand[0].toUpperCase() == "CREATEHIGHLIGHTCIRCLE") {
          //record
          /*
          [1]: objectID
          [3]: x
          [4]: y
          */

          // ------------
          // if test mode, scale x position by 0.9
          if (this.DIYMode == false) {
            nextCommand[3] = parseInt(nextCommand[3]) * 0.9;
          }
          // ------------

          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
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
          }
        } else if (nextCommand[0].toUpperCase() == "DELETE") {
          /*
          [1]: objectID
          */
          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            //if target is highlight circle
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] == null ||
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] == undefined
            ) {
              console.log(
                "Delete: ObjectID: " + nextCommand[1] + " doesn't exist"
              );
            } else {
              if (
                this.animatedObjects.Nodes[parseInt(nextCommand[1])].isNode ==
                false
              ) {
                this.animatedObjects.removeHighlightCircle(
                  parseInt(nextCommand[1])
                );
              }
              //if target is node
              else {
                if (this.printMode == false) {
                  //BST: case 1234
                  //remove attach line from stage
                  //remove attach line by set toBeRemoved = true in both Edges & BackEdges
                  if (
                    this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                      null &&
                    this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                      undefined
                  ) {
                    if (
                      this.animatedObjects.BackEdges[
                        parseInt(nextCommand[1])
                      ][0] != null &&
                      this.animatedObjects.BackEdges[
                        parseInt(nextCommand[1])
                      ][0] != undefined
                    ) {
                      this.animatedObjects.BackEdges[
                        parseInt(nextCommand[1])
                      ][0].toBeRemoved = true;
                      this.animatedObjects.BackEdges[
                        parseInt(nextCommand[1])
                      ][0].remove(this.animatedObjects.stage);
                    }
                  }
                  if (
                    this.animatedObjects.Edges[parseInt(nextCommand[1])] !=
                      null &&
                    this.animatedObjects.Edges[parseInt(nextCommand[1])] !=
                      undefined &&
                    this.animatedObjects.Edges[parseInt(nextCommand[1])] != []
                  ) {
                    for (
                      var j = 0;
                      j <
                      this.animatedObjects.Edges[parseInt(nextCommand[1])]
                        .length;
                      j++
                    ) {
                      this.animatedObjects.Edges[parseInt(nextCommand[1])][
                        j
                      ].toBeRemoved = true;
                      this.animatedObjects.Edges[parseInt(nextCommand[1])][
                        j
                      ].remove(this.animatedObjects.stage);
                    }
                  }

                  //remove node from stage & Nodes
                  this.animatedObjects.Nodes[parseInt(nextCommand[1])].remove(
                    this.animatedObjects.stage
                  );
                  this.NodesNullList.push(parseInt(nextCommand[1]));
                } else if (this.printMode == true) {
                  this.printNullList.push(parseInt(nextCommand[1]));
                }
              }
            }
          } else if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            //delete heap label (or node?)
            if (
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != null &&
              this.animatedObjects.Nodes[parseInt(nextCommand[1])] != undefined
            ) {
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].remove(
                this.animatedObjects.stage
              );
              this.NodesNullList.push(parseInt(nextCommand[1]));
            }
            //remove & set edges toBeRemove=true
            if (
              this.animatedObjects.Edges[parseInt(nextCommand[1])] != null &&
              this.animatedObjects.Edges[parseInt(nextCommand[1])] !=
                undefined &&
              this.animatedObjects.Edges[parseInt(nextCommand[1])] != []
            ) {
              for (
                var j = 0;
                j < this.animatedObjects.Edges[parseInt(nextCommand[1])].length;
                j++
              ) {
                this.animatedObjects.Edges[parseInt(nextCommand[1])][
                  j
                ].toBeRemoved = true;
                this.animatedObjects.Edges[parseInt(nextCommand[1])][j].remove(
                  this.animatedObjects.stage
                );
              }
            }
            //remove & set back edges toBeRemove=true
            if (
              this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                null &&
              this.animatedObjects.BackEdges[parseInt(nextCommand[1])] !=
                undefined
            ) {
              if (
                this.animatedObjects.BackEdges[parseInt(nextCommand[1])][0] !=
                  null &&
                this.animatedObjects.BackEdges[parseInt(nextCommand[1])][0] !=
                  undefined
              ) {
                this.animatedObjects.BackEdges[
                  parseInt(nextCommand[1])
                ][0].toBeRemoved = true;
                this.animatedObjects.BackEdges[
                  parseInt(nextCommand[1])
                ][0].remove(this.animatedObjects.stage);
              }
            }
          }
        } else if (nextCommand[0].toUpperCase() == "DISCONNECT") {
          /*
          [1]: fromNode
          [2]: toNode
          */
          if (
            this.dataStructure.toUpperCase() == "BST" ||
            this.dataStructure.toUpperCase() == "RBT"
          ) {
            //find that edge and mark toBeRemoved & remove from stage
            this.animatedObjects.BackEdges[
              parseInt(nextCommand[2])
            ][0].toBeRemoved = true;
            this.animatedObjects.BackEdges[parseInt(nextCommand[2])][0].remove(
              this.animatedObjects.stage
            );

            //remove from BackEdges list
            //removed from Edges list
            /*
            Do it in drawConnection function by detect toBeRemoved == true
          */
          }
        } else if (nextCommand[0].toUpperCase() == "SETBACKGROUNDCOLOR") {
          if (this.DIYMode == true) {
            if (this.dataStructure.toUpperCase() == "RBT") {
              /*
            [1]: objectID
            [2]: hex color 
            */
              // -------- customize color (black / red) --------
              if (nextCommand[2] == "#AAAAAA") {
                nextCommand[2] = "#555555";
              } else if (nextCommand[2] == "#FFAAAA") {
                nextCommand[2] = "#ff6262";
              }
              //-----------------------------------------------------
              this.animatedObjects.Nodes[parseInt(nextCommand[1])].setNodeColor(
                nextCommand[2],
                this.animatedObjects.stage
              );
            }
          }
          // test mode, set all node same color
          else if (this.DIYMode == false) {
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].setNodeColor(
              this.testModeNodeColor,
              this.animatedObjects.stage
            );
          }
        } else if (nextCommand[0].toUpperCase() == "SETFOREGROUNDCOLOR") {
          if (this.dataStructure.toUpperCase() == "RBT") {
            //TODO
            // not used
          }
        } else if (nextCommand[0].toUpperCase() == "CREATERECTANGLE") {
          /*
          [1]: objectID
          [2]: label
          [3]: width
          [4]: height
          [5]: x
          [6]: y
          */

          // ------------
          // if test mode, scale x position by 0.9
          if (this.DIYMode == false) {
            nextCommand[5] = parseInt(nextCommand[5]) * 0.9;
          }
          // ------------

          if (
            this.dataStructure.toUpperCase() == "MINH" ||
            this.dataStructure.toUpperCase() == "MAXH"
          ) {
            //record
            this.animatedObjects.addRectangleObject(
              parseInt(nextCommand[1]),
              nextCommand[2],
              parseInt(nextCommand[3]),
              parseInt(nextCommand[4]),
              parseInt(nextCommand[5]),
              parseInt(nextCommand[6])
            );
            //draw
            this.animatedObjects.Nodes[parseInt(nextCommand[1])].draw(
              this.animatedObjects.stage
            );
          }
        }

        i = i + 1;
      }
      resolve("end block ");
    });
  };

  this.drawConnection = function () {
    // update all edges
    return new Promise((resolve) => {
      for (var i = 0; i < this.animatedObjects.Edges.length; i++) {
        if (
          this.animatedObjects.Edges[i] != null &&
          this.animatedObjects.Edges[i] != undefined &&
          this.animatedObjects.Edges[i] != []
        ) {
          for (var j = 0; j < this.animatedObjects.Edges[i].length; j++) {
            if (this.animatedObjects.Edges[i][j].toBeRemoved == false) {
              if (this.animatedObjects.Edges[i][j].onScene == false) {
                this.animatedObjects.Edges[i][j].draw(
                  this.animatedObjects.stage
                );
              } else {
                //redraw
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
      //update BackEdges
      for (var i = 0; i < this.animatedObjects.BackEdges.length; i++) {
        if (
          this.animatedObjects.BackEdges[i] != null &&
          this.animatedObjects.BackEdges[i] != undefined &&
          this.animatedObjects.BackEdges[i] != []
        ) {
          for (var j = 0; j < this.animatedObjects.BackEdges[i].length; j++) {
            if (this.animatedObjects.BackEdges[i][j].toBeRemoved == true) {
              //remove from BackEdges list
              this.animatedObjects.BackEdges[i].splice(j, 1);
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

  //for BST & RBT
  this.clearPrintNodes = function () {
    return new Promise((resolve) => {
      if (this.printNullList.length > 0) {
        for (var i = 0; i < this.printNullList.length; i++) {
          var objectID = this.printNullList[i];
          this.animatedObjects.Nodes[objectID].remove(
            this.animatedObjects.stage
          );
          this.animatedObjects.Nodes[objectID] = null;
        }
      }
      //init
      this.printNullList = [];
      resolve("");
    });
  };

  // for delay time between blocks
  // -----------
  this.sleep = function (ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };

  this.delay = async function (ms) {
    return this.sleep(ms).then((v) => "start block ");
  };
  // -----------

  //parse flask returned array of commands
  this.StartNewAnimation = async function (commands) {
    //disable btns bar
    if (this.DIYMode == true) {
      this.disableBtns();
    }
    //initialize
    this.AnimationBlocks = [];
    var block = [];

    //if printMode or clearMode on, insert "SetText<;>0<;>" at the front of command
    //to clear status line
    if (this.printMode == true || this.clearMode == true) {
      //Tree
      if (
        this.dataStructure.toUpperCase() == "BST" ||
        this.dataStructure.toUpperCase() == "RBT"
      ) {
        commands.splice(0, 0, "SetText<;>0<;>");
      }
      //Heap
      else {
        commands.splice(0, 0, "SetText<;>100<;>");
      }
    }

    // animation speed setting
    // if DIY mode
    if (this.DIYMode == true) {
      // if dataStructure is RBTree and its DIYMode, set interval larger
      // bcz the SETTEXT is more complex
      if (this.dataStructure.toUpperCase() == "RBT") {
        this.blocksInterval = 1500;
      }
    }
    // if test mode
    else {
      this.blocksInterval = 400;
    }

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

    console.log("Animation blocks after processing:");
    console.log(this.AnimationBlocks);

    //clear previous print nodes for BST
    if (
      this.dataStructure.toUpperCase() == "BST" ||
      this.dataStructure.toUpperCase() == "RBT"
    ) {
      var clearPrint = await this.clearPrintNodes();
      clearPrint = "";
    }

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

    //init
    this.printMode = false;

    if (this.DIYMode == true) {
      //enable back btns bar
      this.enableBtns();
    } else {
      this.enableTutorBtn();
      console.log("Button has been enabled!");
    }
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
  this.enableTutorBtn = () => {
    const bstButton = document.getElementById("bst");
    const minHeapButton = document.getElementById("minHeap");
    const maxHeapButton = document.getElementById("maxHeap");
    const rbTreeButton = document.getElementById("rbTree");
    const replayButton = document.getElementById("replay");

    bstButton.disabled = false;
    minHeapButton.disabled = false;
    maxHeapButton.disabled = false;
    rbTreeButton.disabled = false;
    replayButton.disabled = false;

    bstButton.classList.add("option-btn-dark-hover");
    minHeapButton.classList.add("option-btn-dark-hover");
    maxHeapButton.classList.add("option-btn-dark-hover");
    rbTreeButton.classList.add("option-btn-dark-hover");
    replayButton.classList.remove("tutor-btns-disable");
    replayButton.classList.add("replay-btn-hover");
  };
}
