import QtQuick 2.0
import "globals.js" as Global 

Rectangle {
    id: button
    property alias text: label.text
    property alias iconSource: aimg.source
    signal clicked

    color: "black"
    border.width: 1
    border.color: "#101010"
    radius: 4
    height: 64
    width: 150
    Image {
        id: aimg
        anchors.leftMargin: 5
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        source: ""
    }
    Text {
        id: label
        text: ""
        font.pixelSize: Global.normalSize
        color: Global.textColor
        anchors.leftMargin: 5
        anchors.left: aimg.right
        anchors.verticalCenter: parent.verticalCenter
    }
    MouseArea {
        id: moar
        anchors.fill: parent
        onClicked: button.clicked()
    }
}
