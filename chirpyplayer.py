from PyQt5.QtCore import QUrl, Qt, pyqtProperty
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class chirpyPlayer(QMediaPlayer):
	def __init__(self):
		super().__init__()
		self._prevSong=0
		self._skipped=False
		self._playlist=QMediaPlaylist(self)
		self.setPlaylist(self._playlist)
		self.currentMediaChanged.connect(self.unsetSkipped)
	def replacePlaylist(self,plist):
		self._playlist.clear()
		for i in range (plist.rowCount()):
			self._playlist.addMedia(QMediaContent(QUrl.fromLocalFile(
				plist.data(plist.index(i,0),Qt.UserRole))))
	def setSkipped(self):
		self._skipped=True
	def unsetSkipped(self):
		self._skipped=False
	@pyqtProperty(bool)
	def skipped(self):
		return self._skipped
	@skipped.setter
	def skipped(self, val):
		self._skipped = bool(val)
	@pyqtProperty(int)
	def previousId(self):
		return self._prevSong
	@previousId.setter
	def previousId(self, id):
		self._prevSong=id
