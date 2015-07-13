import QtQuick 2.0
import "globals.js" as Global

ListView {
    id: sqlistView
    signal clicked (string name, int uid)

    state: "hidden"
    width: (parent.width - 16) / 2
    highlight: Rectangle {color:"steelblue"}
    spacing: Global.bigSize * 1.2
    function toggle() {
        if (sqlistView.state === "hidden")
            sqlistView.state = "showing"
        else
            sqlistView.state = "hidden"
    }
    delegate: Item {
        Text {
            id: delegateText
            text: name
            color: Global.textColor
            font.pixelSize: Global.bigSize
            anchors.verticalCenter: parent.verticalCenter
            MouseArea {
                anchors.fill: parent
                onClicked: sqlistView.clicked(name, uid)
            }
        }
    }
}
