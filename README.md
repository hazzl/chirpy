# chirpy
A media center application for small touch screens

This program leverages the power of Qt, python and sqlite to cobble together a media center application for touch based devices.

##Structure
Right now, the project consists of two parts: the scanner which builds a database of media files available and the main application which plays the media using a QtQuick user interface. For the time being these two parts are run indepently from each other. It is planned however, to integrate backgroud path scanning in the main application.

###Scanner
The scanner looks for media files under a file system path specified on the command line. It then builds a database of the metadata stored in these files. To run the scanner simply invoke it from the command line like this
```
    $ python3 scanner.py <path to scan>
```
###chirpy
The main program is -unsurprisingly- called chirpy and simply started like so:
```
    $ ./chirpy
```
##Dependencies
The program is written in python3 and needs the following libraries installed:

* Qt5
  * QtCore
  * QtMultimedia
  * QtQuick
* pyqt5
* gstreamer 1.0
  * python-gstreamer1.0
  * gir1.2-gst1.0
* sqlite3
