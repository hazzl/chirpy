from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class chirpyPlayer(QMediaPlayer):
	def __init__(self):
		super().__init__()
		self._prevSong=None
		self._skipped=False
		self._playlist=QMediaPlaylist(self)
		self.setPlaylist(self._playlist)
	def replacePlaylist(self,plist):
		self._playlist.clear()
		for i in range (plist.rowCount()):
			self._playlist.addMedia(QMediaContent(QUrl.fromLocalFile(
				plist.data(plist.index(i,0),Qt.UserRole))))
	def skipped(self):
		self._skipped=True
