import QtQuick 2.0
import QtQuick.Controls 1.0
import "globals.js" as Global

Rectangle {
    id: screen
    width: 640
    height: 480
    color: "black"
    Rectangle {
	width: parent.width - 16
	anchors.horizontalCenter: parent.horizontalCenter
	IButton {
	    id: genreButton
	    text: "Genre"
	    anchors.top: parent.top
	    anchors.topMargin: 0
	    anchors.left: parent.left
	    anchors.leftMargin: 0
	    iconSource: "icons/Genre.png"
	    onClicked: genreList.toggle()
	}
	IButton {
	    id: artistButton
	    text: "Artist"
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.top: parent.top
	    iconSource: "icons/Artist.png"
	    onClicked: artistList.toggle()
	}
	IButton {
	    id: albumButton
	    text: "Album"
	    anchors.top: parent.top
	    anchors.right: parent.right
	    iconSource: "icons/Album.png"
	    onClicked: albumList.toggle()
	}
	SQListView {
	    id: genreList
	    objectName: "genreList"
	    reference: genreButton
	    model: genreModel
	    Component.onCompleted: {
		artistList.showing.connect(hide)
		albumList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
	}
	SQListView {
	    id: artistList
	    objectName: "artistList"
	    reference: artistButton
	    model: artistModel
	    Component.onCompleted: {
		genreList.showing.connect(hide)
		albumList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
	}
	SQListView {
	    id: albumList
	    objectName: "albumList"
	    model: albumModel
	    reference: artistButton
	    section.property: "category"
	    section.criteria: ViewSection.FullString
	    section.delegate: Text {
		text: section
		font.pixelSize: Global.normalSize
		font.italic: true
		color: "white"
		height: Global.bigSize
		verticalAlignment: Text.AlignBottom
		Rectangle {
		    color: Global.textColor
		    visible: section != ''
		    height: 2
		    width: 192
		    anchors.top: parent.baseline
		}
	    }
	    Component.onCompleted: {
		artistList.showing.connect(hide)
		genreList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
	}
	Image {
	    id: cover
	    objectName: "cover"
	    x: genreButton.x
	    y: genreButton.y + genreButton.height + 36
	    height: 256
	    width: 256
	    opacity: 1
	    fillMode: Image.PreserveAspectFit
	    states: State {
		name: "hidden"
		when: (genreList.state === 'showing')
		      || (artistList.state === 'showing')
		      || (albumList.state === 'showing')
		PropertyChanges {
		    target: cover
		    x: -width
		    opacity: 0
		}
	    }
	    transitions: Transition {
		NumberAnimation {
		    target: cover
		    properties: "x,opacity"
		    duration: 300
		    easing.type: Easing.InOutQuad
		}
	    }
	    Text {
		id: artistName
		anchors.bottom: cover.status == Image.Ready ? parent.top : albumTitle.top
		anchors.bottomMargin: 3
		anchors.horizontalCenter: parent.horizontalCenter
		font.pixelSize: Global.normalSize
		font.bold: true
		color: Global.textColor
	    }
	    Text {
		id: albumTitle
		anchors.top: parent.bottom
		anchors.topMargin: 3
		anchors.horizontalCenter: parent.horizontalCenter
		font.pixelSize: Global.normalSize
		color: Global.textColor
		Connections {
		    target: song
		    onMetaDataChanged: switch (key) {
				       case "AlbumTitle":
					   albumTitle.text = value
					   break
				       case "ContributingArtist":
					   artistName.text = value
				       }
		}
	    }
	}
    }
    ListView {
	id: playList
	signal clicked(int index)
	objectName: "playList"
	model: plistModel
	y: albumButton.y + albumButton.height + Global.smallSize
	height: playbutton.y - y - 3
	anchors.right: parent.right
	width: parent.width / 2
	clip: true
	preferredHighlightBegin: Global.normalSize * 4
	preferredHighlightEnd: Global.normalSize * 11
	highlightRangeMode: ListView.ApplyRange
	highlightMoveDuration: 600
	highlight: Rectangle {
	    color: "darkgrey"
	    opacity: .2
	}
	delegate: Text {
	    font.pixelSize: ListView.isCurrentItem ? Global.bigSize : Global.normalSize
	    color: Global.textColor
	    text: name
	    MouseArea {
		anchors.fill: parent
		onClicked: {
		    playList.currentIndex = index
		    playList.clicked(index)
		}
	    }
	    Behavior on font.pixelSize {
		NumberAnimation {
		    easing.type: Easing.InOutQuart
		    duration: 200
		}
	    }
	}
    }
    IButton {
	id: playbutton
	objectName: "playbutton"
	anchors.bottom: parent.bottom
	anchors.bottomMargin: 5
	anchors.left: parent.left
	anchors.leftMargin: 8
	width: 65
	iconSource: song.state === Global.PlayingState ? "icons/Pause.png" : "icons/Play.png"
	onClicked: song.state === Global.PlayingState ? song.pause() : song.play()
    }
    Slider {
	id: slider
	objectName: "slider"
	width: parent.width - 200
	height: Global.normalSize
	anchors.verticalCenter: playbutton.verticalCenter
	anchors.left: playbutton.right
	anchors.leftMargin: 8
	value: song.position / song.duration
	onPressedChanged: if (!pressed)
			      song.position = (song.duration * value)
    }
    Text {
	id: timer
	anchors.verticalCenter: slider.verticalCenter
	anchors.left: slider.right
	anchors.leftMargin: 10
	text: sec2min(Math.round(
			  slider.value * song.duration / 1000)) + "/" + sec2min(
		  Math.round(song.duration / 1000))
	font.pixelSize: Global.normalSize
	color: Global.textColor
	function sec2min(sec) {
	    var ret = ""
	    if (sec > 3599) {
		ret = Math.floor(sec / 3600).toString() + ":"
		sec %= 3600
	    }
	    var mins = Math.floor(sec / 60)
	    if ((ret.length > 0) && (mins < 10))
		ret += "0"
	    ret += mins.toString() + ":"
	    sec %= 60
	    if (sec < 10)
		ret += "0"
	    return ret + sec.toString()
	}
    }
}
