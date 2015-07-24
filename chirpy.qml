﻿import QtQuick 2.0
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
	SQLabel {
            id: currentGenre
            objectName: "currentGenre"
            anchors.left: genreButton.left
	    anchors.top: genreButton.bottom
        }
	SQLabel {
            id: currentArtist
            objectName: "currentArtist"
            anchors.left: artistButton.left
            anchors.top: artistButton.bottom
        }
	SQLabel {
            id: currentAlbum
            objectName: "currentAlbum"
            anchors.right: albumButton.right
            anchors.top: albumButton.bottom
        }
        SQListView {
            id: genreList
	    reference: currentGenre
            model: genreModel
	    onClicked: { currentGenre.text = name; currentGenre.uid = uid
		    currentArtist.text="" ; currentArtist.uid=0 ;
		    currentAlbum.text=""; currentAlbum.uid=0}
	    Component.onCompleted: {
		artistList.showing.connect(hide)
		albumList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
        }
	SQListView {
	    id: artistList
	    reference: currentArtist
	    model: artistModel
	    onClicked: { currentArtist.text = name; currentArtist.uid = uid
		    currentAlbum.text = "" ; currentAlbum.uid = 0}
	    Component.onCompleted: {
		genreList.showing.connect(hide)
		albumList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
	}
	SQListView {
	    id: albumList
	    model: albumModel
	    onClicked: { currentAlbum.text = name; currentAlbum.uid = uid ; }
	    reference: currentArtist
	    Component.onCompleted: {
		artistList.showing.connect(hide)
		genreList.showing.connect(hide)
		playbutton.clicked.connect(hide)
	    }
	}
    }
    ListView {
	id: playList
	signal clicked(int index)
	objectName: "playList"
	model: plistModel
        anchors.bottom: playbutton.top
	anchors.right: parent.right
	height: 110
	width: parent.width/2
	clip: true
	preferredHighlightBegin: Global.normalSize
	preferredHighlightEnd: 4*Global.normalSize
	highlightRangeMode: ListView.ApplyRange
	highlight: Rectangle { color: "darkgrey"; opacity: .2 }
	delegate: Text {
	    font.pixelSize: ListView.isCurrentItem ? Global.bigSize : Global.normalSize
	    color: Global.textColor
	    text: name
	    MouseArea {
		anchors.fill:parent
		onClicked:  {playList.currentIndex = index;
			playList.clicked(index);}
	    }
	    Behavior on font.pixelSize { NumberAnimation { easing.type: Easing.InOutQuart; duration: 200 }}
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
        iconSource: song.state ===  Global.PlayingState ? "icons/Pause.png" : "icons/Play.png"
        onClicked: song.state === Global.PlayingState ? song.pause() : song.play()
    }

    Slider {
        id: slider
        width: parent.width - 180
        height: Global.normalSize
        anchors.verticalCenter: playbutton.verticalCenter
        anchors.left: playbutton.right
        anchors.leftMargin: 8
        value: song.position / song.duration
        onPressedChanged: if (!pressed) song.position=(song.duration * value)
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
            var ret = Math.floor(sec / 60).toString() + ":"
            var secs = sec % 60
            if (secs < 10) ret += "0"
            return ret + secs.toString()
        }
    }
}
