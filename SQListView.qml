import QtQuick 2.0
import "globals.js" as Global

ListView {
    id: sqlistView
    signal clicked (string name, int uid)
    signal showing
    property Item reference

    state: "hidden"
    clip: true
    width: (parent.width - 16) / 2
    highlight: Rectangle {color: "darkgrey"; radius: 2; opacity:.3}
    highlightMoveDuration: 600

    function toggle() {
        if (sqlistView.state === "hidden")
            sqlistView.state = "showing"
        else
            sqlistView.state = "hidden"
    }

    function hide() {
	if (sqlistView.state === "showing") { sqlistView.state = "hidden"}
    }

    delegate: Text {
            id: delegateText
            text: name
            color: Global.textColor
            font.pixelSize: Global.bigSize
            height: Global.bigSize+4
            MouseArea {
                anchors.fill: parent
                onClicked: { sqlistView.currentIndex=index;
			     sqlistView.clicked(name, uid); }
            }
	}
    states: [
	State {
	    name: "hidden"
	    PropertyChanges {
		target: sqlistView
		x: reference.x
		y: reference.y 
		height: reference.height
		opacity: 0
		enabled: false
	    }
	}, State {
	    name: "showing"
	    PropertyChanges {
		target: sqlistView
		x: currentGenre.x
		y: (currentGenre.y + currentGenre.height) 
		height: playbutton.y - y
		opacity: 1
		enabled: true
	    }
	    StateChangeScript { script: sqlistView.showing() }
	}
    ]
    transitions: Transition {
	NumberAnimation {
	    target: sqlistView
	    properties: "x,y,opacity,height"
	    duration: 300
	    easing.type: Easing.InOutQuad
	}
    }
}
