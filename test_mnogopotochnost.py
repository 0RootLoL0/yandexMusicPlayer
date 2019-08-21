from threading import Thread
import requests
import socket
import json
import vlc

headers = {
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
numTR = 0
LOCALHOST = "127.0.0.1"
PORT = 5591

# Возвращает содержимое playlist
def contentPlaylist(numder):
	url = "https://music.yandex.ru/handlers/playlist.jsx?owner=r00tl0l&kinds="+str(numder)+"&light=true&madeFor=&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.8926908172434902"
	r = requests.get(url, headers=headers)
	#print( json.loads(r.text))
	return json.loads(r.text)

# Возвращает ссылку на трек
def downloadTrack(idTrack, idAlibom):
	print(idTrack, idAlibom)
	url = "https://music.yandex.ru/api/v2.1/handlers/track/"+str(idTrack)+":"+str(idAlibom)+"/web-own_playlists-playlist-track-saved/download/m?hq=0&external-domain=music.yandex.ru&overembed=no&__t=1564398857526"
	r = requests.get(url, headers=headers)
	w = requests.get(json.loads(r.text)["src"]+"&format=json&external-domain=music.yandex.ru&overembed=no&__t=1564399055017")
	e = json.loads(w.text) 
	return "https://"+e["host"]+"/get-mp3/"+"e43431431c2e7b659335ff91aca7e990"+"/"+e["ts"]+e["path"]

# запуск плера 
def manupVlc(playlist, numTrack):
	if len(playlist) >= numTrack and numTrack >= 0:
		print(numTrack)
		inst = vlc.Instance()
		med = inst.media_new(downloadTrack(playlist[numTrack]["id"], playlist[numTrack]["albums"][0]["id"]))
		p = med.player_new_from_media()
		p.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, call_vlc, p)
		return p

# запуск трека
def playNm(hhui):
	def vlcplpl(NT):
			global p
			p.stop()
			p = manupVlc(playlist, NT)
			p.play()
	global numTR
	if hhui:
		if len(playlist) >= numTR:
			numTR += 1
	else:
		if numTR-1 > 0:
			numTR -= 1
	t1 = Thread(target=vlcplpl, args=(numTR,))
	t1.start()
	t1.join()

# CallBack VLC
def call_vlc(self, player):
	global p, playlist, numTR
	print("hui")
	if len(playlist) >= numTR:
		numTR += 1
	else:
		numTR = 0
	print(numTR)
	inst = vlc.Instance()
	med = inst.media_new(downloadTrack(playlist[numTR]["id"], playlist[numTR]["albums"][0]["id"]))
	p = med.player_new_from_media()
	p.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, call_vlc, p)
	p.play()


# Запрос playlist`а
playlist = contentPlaylist(1016)["playlist"]["tracks"]

# init первого трека
p = manupVlc(playlist, numTR)

# Запуск сокета (сервер)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(1)
print("Server started")
while True:
	clientConnection,clientAddress = server.accept()
	print("Connected clinet :" , clientAddress)
	data = clientConnection.recv(1024)
	print("From Client :" , data.decode())


	if data.decode() == "pause":
		Thread(target=p.pause).start()
		clientConnection.send(bytes("Ok pause",'UTF-8'))
	elif data.decode() == "play":
		Thread(target=p.play).start()
		clientConnection.send(bytes("Ok play",'UTF-8'))
	elif data.decode() == "back":
		playNm(False)
		clientConnection.send(bytes("Ok back",'UTF-8'))
	elif data.decode() == "onward":
		playNm(True)
		clientConnection.send(bytes("Ok onward",'UTF-8'))
	elif data.decode() == "returnName":
		rnm = json.dumps({"title": playlist[numTR]["title"], "artists": playlist[numTR]["artists"]})
		clientConnection.send(bytes(rnm,'UTF-8'))
	else:
		clientConnection.send(bytes("error",'UTF-8'))
	
	clientConnection.close()