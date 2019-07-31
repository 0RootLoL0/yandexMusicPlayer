import vlc, time
import json
import requests
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize
import design  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

	def __init__(self):
		self.headers = {
			"Host": "music.yandex.ru",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
			"Accept": "application/json; q=1.0, text/*; q=0.8, */*; q=0.1",
			"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate, br",
			"X-Retpath-Y": "https%3A%2F%2Fmusic.yandex.ru%2Fusers%2Fr00tl0l%2Fplaylists",
			"X-Current-UID": "730767098",
			"X-Requested-With": "XMLHttpRequest",
			"Connection": "keep-alive",
			"Referer": "https://music.yandex.ru/users/r00tl0l/playlists",
			"Cookie": "yandexuid=6023013241564258923;"+"i=n/xrBXEYNdJ8X+3GnqYFheWPP4Fr8I6DlsBU88IB06FvXnWO+D6q4q16+tdUBdDLeU+pO9ap8kP/DqfqdfjNbUyk4hI=; yp=1565605796.rpoly.0#1566988197.shlos.1#1564874593.szm.0_8:2400x1350:2343x1170#1879623273.udn.cDpyMDB0bDBs; mda=0; cycada=MagFdoUHAVyTsVBYcwYEVj+ZDVwh9KIhTOCOA4vkxas=; Session_id=3:1564263273.5.0.1564263273959:MBP8bQ:4f.1|730767098.0.2|202770.226029.KFo-kF-58mjTeWTbjVa6vOt0uho; sessionid2=3:1564263273.5.0.1564263273959:MBP8bQ:4f.1|730767098.0.2|202770.977691.x4fpwlzcyiFtO2XHjwzYyClJM4w; L=AFFXaURHeG5HQGZUUk9KWUV9Ql9gfVsAIUpyFQcFIA==.1564263273.13939.322420.96a85f389598c29844f1385f911de503; yandex_login=r00tl0l; lastVisitedPage=%7B%22730767098%22%3A%22%2Fusers%2Fr00tl0l%2Fplaylists%22%7D; yabs-frequency=/4/200004OSFbq00000/; _ym_uid=1564325428420914521; _ym_d=1564325428; _ym_isad=2; bltsr=1; ys=wprid.1564385321744303-239963555370250067400035-sas1-1040; device_id=\"ade8863d0409e27949cc4b7e7a9292f270032c620\"; active-browser-timestamp=1564398801396; pepsi_year=today; instruction=1"} # 
		self.PlayNstop = True
		self.inst = vlc.Instance()
		self.playlist = self.contentPlaylist(101)["playlist"]["tracks"]
		self.med = self.inst.media_new(self.downloadTrack(self.playlist[0]["id"], self.playlist[0]["albums"][0]["id"]))
		self.p = self.med.player_new_from_media()
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.pushButton_2.clicked.connect(self.wwww)# Выполнить функцию browse_folder
		self.label_2.setText(self.playlist[0]["title"])
		self.label_4.setText(self.playlist[0]["artists"][0]["name"])
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		self.tray_icon.activated.connect(self.action)
		self.tray_icon.show()
		self.hide()

	def contentPlaylist(self, numder):
		url = "https://music.yandex.ru/handlers/playlist.jsx?owner=r00tl0l&kinds="+str(numder)+"&light=true&madeFor=&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.8926908172434902"
		r = requests.get(url, headers=self.headers)
		return json.loads(r.text)

	def downloadTrack(self, idTrack, idAlibom):
		url = "https://music.yandex.ru/api/v2.1/handlers/track/"+str(idTrack)+":"+str(idAlibom)+"/web-own_playlists-playlist-track-saved/download/m?hq=0&external-domain=music.yandex.ru&overembed=no&__t=1564398857526"
		r = requests.get(url, headers=self.headers)
		w = requests.get(json.loads(r.text)["src"]+"&format=json&external-domain=music.yandex.ru&overembed=no&__t=1564399055017")
		e = json.loads(w.text) 
		return "https://"+e["host"]+"/get-mp3/"+"e43431431c2e7b659335ff91aca7e990"+"/"+e["ts"]+e["path"]

	def action(self):
		self.show()
		print('System tray icon clicked.')

	def vlcplpl(self, p, play):
		if play:
			p.play()
			print("play")
		else:
			p.pause()
			print("stop")

	def wwww(self):
		def vlcplpl(p, play):
			if play:
				p.play()
				print("play")
			else:
				p.pause()
				print("stop")

		t1 = threading.Thread(target=vlcplpl, args=(self.p, self.PlayNstop))
		t1.start()
		t1.join()
		if self.PlayNstop :
			self.PlayNstop = False
		else:
			self.PlayNstop = True

def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = ExampleApp()  # Создаём объект класса ExampleApp
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  

#inst = vlc.Instance()
#med = inst.media_new('https://s46myt.storage.yandex.net/get-mp3/e43431431c2e7b659335ff91aca7e990/00058ed03f14fc36/rmusic/U2FsdGVkX1_1kHImJJFa7_az8qL-6_iSU_aYvOLV7kXMaMzS92YScXalOK-E3FczdqQnWumUZAq5hkmOcA2Uj_IScfqxl4wusZ_Q9r-5luI/0218e6e315ec609872b616fc9912ec738847612a24cebae5bbf12b0d9891376b')
#p = med.player_new_from_media()
#p.play()
#time.sleep(111)