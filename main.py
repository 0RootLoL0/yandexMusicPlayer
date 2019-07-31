import json
import time
import requests

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
	"Cookie": "куки из браузера"} # 

## второй шаг узнать содержимае плейлиста
def contentPlaylist(numder):
	url = "https://music.yandex.ru/handlers/playlist.jsx?owner=r00tl0l&kinds="+str(numder)+"&light=true&madeFor=&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.8926908172434902"
	r = requests.get(url, headers=headers)
	return json.loads(r.text)

def downloadTrack(idTrack, idAlibom):
	url = "https://music.yandex.ru/api/v2.1/handlers/track/"+str(idTrack)+":"+str(idAlibom)+"/web-own_playlists-playlist-track-saved/download/m?hq=0&external-domain=music.yandex.ru&overembed=no&__t=1564398857526"
	r = requests.get(url, headers=headers)
	w = requests.get(json.loads(r.text)["src"]+"&format=json&external-domain=music.yandex.ru&overembed=no&__t=1564399055017")
	e = json.loads(w.text) 
	return "https://"+e["host"]+"/get-mp3/"+"e43431431c2e7b659335ff91aca7e990"+"/"+e["ts"]+e["path"]

wer = []

for track in contentPlaylist(101)["playlist"]["tracks"]:
	we = track["title"]
	wr = track["artists"][0]["name"]
	wt = downloadTrack(track["id"], track["albums"][0]["id"])
	print({"name": we, "artist": wr, "download": wt})
