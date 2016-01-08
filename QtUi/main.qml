/*******************************************************************************
 * Copyright (c) 2016 Grzegorz Sygieda
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
*******************************************************************************/

import QtQuick 2.0
import Ubuntu.Components 0.1
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1

Rectangle {
    id: mainWindow
    width: 500
    height: 500
    color: "grey"

     // ad signals slots to clear code

    Rectangle {
        id: commandPanel
        height: 50
        color: "white"
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0
        border.width: 1
        border.color: "black"

        property int columns: 3
        property int rows: 3

        function refreshGrid() {
            commandModel.clear()
            for (var row=0; row<commandPanel.rows; row++) {
                for (var col=0; col<commandPanel.columns; col++) {
                    commandModel.append({"cmdName": "NONE", "cmdColorCode": "grey"})
                }
            }
        }

        function callCommand(cmd) {
            switch (cmd) {
                case 0:
                    console.log("none cmd - skipping")
                    break
                case 1:
                    control.forward()
                    break
                case 2:
                    control.backward()
                    break
                case 3:
                    control.left()
                    break
                case 4:
                    control.right()
                    break
            }
        }

        Text {
            id: tCols
            x: 16
            y: 18
            text: qsTr("Columns:")
            font.pixelSize: 12
        }

        TextField {
            id: teCols
            x: 77
            y: 18
            width: 19
            height: 20
            text: qsTr(commandPanel.columns.toString())
            font.pixelSize: 12
            validator: IntValidator{bottom:1; top: 9}
            horizontalAlignment: TextInput.AlignHCenter
            focus: true

            style: TextFieldStyle {
                        textColor: "black"
                        background: Rectangle {
                            radius: 20
                            color: "grey"
                            implicitWidth: 40
                            implicitHeight: 24
                            border.color: "black"
                            border.width: 1
                        }
            }

            onTextChanged: {
                commandPanel.columns = text
                commandPanel.refreshGrid()
            }
        }

        Text {
            id: tRows
            x: 105
            y: 18
            text: qsTr("Rows:")
            font.pixelSize: 12
        }

        TextField {
            id: teRows
            x: 148
            y: 18
            width: 19
            height: 20
            text: qsTr(commandPanel.rows.toString())
            font.pixelSize: 12
            validator: IntValidator{bottom:1; top: 9}
            horizontalAlignment: TextInput.AlignHCenter
            focus: true

            style: TextFieldStyle {
                        textColor: "black"
                        background: Rectangle {
                            radius: 20
                            color: "grey"
                            implicitWidth: 40
                            implicitHeight: 24
                            border.color: "black"
                            border.width: 1
                        }
                    }

            onTextChanged: {
                commandPanel.rows = text
                commandPanel.refreshGrid()
            }
        }

        Rectangle {
            id: startButton
            x: 313
            y: 10
            width: startButtonText.width + 20
            height: 30
            radius: 5
            antialiasing: true
            border.width: 2
            border.color: "black"
            color: "black"

            Text {
                id: startButtonText
                text: qsTr("START")
                anchors.centerIn: parent
                font.pixelSize: parent.height * .5
                style: Text.Normal
                color: "white"
                styleColor: "white"
            }

            MouseArea {
                id: startButtonMouseArea
                anchors.fill: parent

                onClicked: {
                    console.log("start button clicked")
                    commandTimer.start()
                    commandGrid.enabled = false
                }

                onPressed: {
                    startButton.color = "white"
                    startButtonText.color = "black"
                }

                onReleased: {
                    startButton.color = "black"
                    startButtonText.color = "white"
                }
            }
        }

        Rectangle {
            id: stopButton
            x: 413
            y: 10
            width: stopButtonText.width + 20
            height: 30
            radius: 5
            antialiasing: true
            border.width: 2
            border.color: "black"
            color: "black"

            Text {
                id: stopButtonText
                text: qsTr("STOP")
                anchors.centerIn: parent
                font.pixelSize: parent.height * .5
                style: Text.Normal
                color: "white"
                styleColor: "white"
            }

            MouseArea {
                id: stopButtonMouseArea
                anchors.fill: parent

                onClicked: {
                    console.log("stop button clicked")
                    commandTimer.stop()
                    commandGrid.enabled = true
                }

                onPressed: {
                    stopButton.color = "white"
                    stopButtonText.color = "black"
                }

                onReleased: {
                    stopButton.color = "black"
                    stopButtonText.color = "white"
                }
            }
        }

        Timer {
            id: commandTimer
            interval: 1000;
            running: false;
            repeat: true

            property int index: 1
            property variant cmd;

            onTriggered: {
                console.log("timer fired")
                if (index <= commandPanel.columns * commandPanel.rows) {
                    commandGrid.currentIndex = index - 1
                    cmd = commandGrid.contentItem.children[index]
                    console.log("cmd ", cmd.actualCommand)
                    commandPanel.callCommand(cmd.actualCommand)
                }
                else {
                    index = 0
                    running = false
                }
                index++
            }
          }

    }

    ListModel {
        // dynamicly populated
        id: commandModel

    }

    GridView {
        id: commandGrid
        z: 1
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: commandPanel.bottom
        anchors.topMargin: 0
        cellWidth: width / commandPanel.columns;
        cellHeight: height / commandPanel.rows;

        model: commandModel

        delegate: Item {

            id: commandItem

            objectName: "gridItem"

            property int actualCommand: 0
            property variant statesNames: ["NONE", "FORWARD", "BACKWARD", "LEFT", "RIGHT"]

            Rectangle {
                id: commandRect
                width: commandGrid.cellWidth
                height: commandGrid.cellHeight
                color: cmdColorCode
                border.color: commandItem.GridView.isCurrentItem ? "pink" : "black"
                border.width: commandItem.GridView.isCurrentItem ? 3 : 1

                MouseArea {
                    id: commandMouseArea
                    anchors.fill: parent
                    onClicked: {
                        commandGrid.currentIndex = index
                        actualCommand++
                        actualCommand = actualCommand >= 5 ? 0 : actualCommand
                        commandRect.state = statesNames[actualCommand]
                        console.log("grid index clicked ", commandGrid.currentIndex, actualCommand)
                    }
                }

                states: [
                    State {
                      name: "FORWARD"
                      PropertyChanges {target:commandRect; color:"green"}
                      PropertyChanges {target:commandName; text: qsTr("FORWARD")}
                    },
                    State {
                      name: "BACKWARD"
                      PropertyChanges {target:commandRect; color:"red"}
                      PropertyChanges {target:commandName; text: qsTr("BACKWARD")}
                    },
                    State {
                      name: "LEFT"
                      PropertyChanges {target:commandRect; color:"blue"}
                      PropertyChanges {target:commandName; text: qsTr("LEFT")}
                    },
                    State {
                      name: "RIGHT"
                      PropertyChanges {target:commandRect; color:"yellow"}
                      PropertyChanges {target:commandName; text: qsTr("RIGHT")}
                    }
                  ]

                Text {
                    id: commandName
                    text: qsTr(cmdName)
                    anchors.centerIn: commandRect
                }
            }
       }

       Component.onCompleted: currentIndex = -1

       flickableChildren: MouseArea {
           anchors.fill: parent
           onClicked: {
               commandGrid.currentIndex = -1
               console.log("out grid clicked")
           }
       }
    }
}
