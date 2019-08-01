import sys
import vlc
import json
import requests
import threading
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle
from PyQt5.QtCore import QSize
import design


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
			"Cookie": "yandexuid=6023013241564258923; i=38JflLzr3WqxC3q1+cWx1HRhoOxBIrXdPEhaIU6g0spJiXgxFYQc6s8BkLF248fP5aIG53hB2NNp6UZttwBlVCkNNI8=; yp=1880007978.multib.1#1565870044.rpoly.0#1567252442.shlos.1#1564874593.szm.0_8%3A2400x1350%3A2343x1170#1880008099.udn.cDpyMDB0bDBs#1567239967.ygu.1#1880011080.yrtsi.1564651080; mda=0; cycada=0TrjoiwsRVjdvgFEYXIPfz+ZDVwh9KIhTOCOA4vkxas=; L=UmEFfWBKYW1QYFd6a2RwcFlpR31PDGV8B0hYLD10Xg==.1564648099.13944.363954.3559c8686c10a437f8711fdd09b05e85; lastVisitedPage=%7B%22730767098%22%3A%22%2Fusers%2Fr00tl0l%2Fplaylists%22%7D; yabs-frequency=/4/200301sLGLqI2pzT/brcmSAms8Hg-FMsiDaS0/; _ym_uid=1564325428420914521; _ym_d=1564325428; ys=udn.cDpyMDB0bDBs#wprid.1564649572948038-1564985967476405864100034-man1-3769; _ym_isad=2; pepsi_year=today; yandex_gid=213; zm=m-white_bender.gen.webp.css-https%3As3home-static_3Npl7m9F02lNQ92K0MEnUyfJ8p8%3Ac; _ym_wasSynced=%7B%22time%22%3A1564658842206%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; device_id=\"ade8863d0409e27949cc4b7e7a9292f270032c620\"; active-browser-timestamp=1564661912479; Session_id=3:1564648099.5.0.1564648099686:FSM7sA:86.1|730767098.0.2|202983.265396.Hcoxx__zBiYPKBi8F4nrMcgqCZ4; sessionid2=3:1564648099.5.0.1564648099686:FSM7sA:86.1|730767098.0.2|202983.797094.fog3frAeWjb9U9KrGaIzoPakv0M; yandex_login=r00tl0l; _ym_visorc_1028356=b; instruction=1"} # 
		self.PlayNstop = True
		self.showIS = False
		self.NT = 0
		self.playlist = self.contentPlaylist(101)["playlist"]["tracks"]
		self.manupVlc(self.NT)
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		
		self.label_2.setText(self.playlist[0]["title"])
		self.label_4.setText(self.playlist[0]["artists"][0]["name"])
		
		self.pushButton_3.clicked.connect(self.pluseNT)
		self.pushButton_2.clicked.connect(self.wwww)
		self.pushButton.clicked.connect(self.veechstNT)

		
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		self.tray_icon.activated.connect(self.action)
		self.tray_icon.show()
		self.hide()

	def test(self):
		inst = vlc.Instance()
		med = inst.media_new(self.downloadTrack(self.playlist[self.NT]["id"], self.playlist[self.NT]["albums"][0]["id"]))
		self.p = med.player_new_from_media()
		self.label_2.setText(self.playlist[self.NT]["title"])
		self.label_4.setText(self.playlist[self.NT]["artists"][0]["name"])

	def contentPlaylist(self, numder):
		url = "https://music.yandex.ru/handlers/playlist.jsx?owner=r00tl0l&kinds="+str(numder)+"&light=true&madeFor=&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.8926908172434902"
		r = requests.get(url, headers=self.headers)
		#print( json.loads(r.text))
		return json.loads(r.text)

	def downloadTrack(self, idTrack, idAlibom):
		url = "https://music.yandex.ru/api/v2.1/handlers/track/"+str(idTrack)+":"+str(idAlibom)+"/web-own_playlists-playlist-track-saved/download/m?hq=0&external-domain=music.yandex.ru&overembed=no&__t=1564398857526"
		r = requests.get(url, headers=self.headers)
		w = requests.get(json.loads(r.text)["src"]+"&format=json&external-domain=music.yandex.ru&overembed=no&__t=1564399055017")
		e = json.loads(w.text) 
		return "https://"+e["host"]+"/get-mp3/"+"e43431431c2e7b659335ff91aca7e990"+"/"+e["ts"]+e["path"]

	def action(self):
		if self.showIS:
			self.hide()
			self.showIS = False
		else:
			self.show()
			self.showIS = True
		print('System tray icon clicked.')

	def wwww(self):
		def vlcplpl(p, play):
			if play:
				p.play()
				print("play")
			else:
				p.pause()
				print("pause")

		t1 = threading.Thread(target=vlcplpl, args=(self.p, self.PlayNstop))
		t1.start()
		t1.join()
		if self.PlayNstop :
			self.PlayNstop = False
		else:
			self.PlayNstop = True

	def pluseNT(self):
		def vlcplpl(www, NT):
			www.p.stop()
			www.test()
			www.p.play()

		t1 = threading.Thread(target=vlcplpl, args=(self, self.NT))
		self.NT += 1
		t1.start()
		t1.join()

	def veechstNT(self):
		def vlcplpl(www, NT):
			www.p.stop()
			www.test()
			www.p.play()

		t1 = threading.Thread(target=vlcplpl, args=(self, self.NT))
		self.NT -= 1
		t1.start()
		t1.join()
	
	def manupVlc(self, numTrack):
		inst = vlc.Instance()
		med = inst.media_new(self.downloadTrack(self.playlist[numTrack]["id"], self.playlist[numTrack]["albums"][0]["id"]))
		self.p = med.player_new_from_media()

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