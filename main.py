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
	"Cookie": "yandexuid=6023013241564258923;"+"i=n/xrBXEYNdJ8X+3GnqYFheWPP4Fr8I6DlsBU88IB06FvXnWO+D6q4q16+tdUBdDLeU+pO9ap8kP/DqfqdfjNbUyk4hI=; yp=1565605796.rpoly.0#1566988197.shlos.1#1564874593.szm.0_8:2400x1350:2343x1170#1879623273.udn.cDpyMDB0bDBs; mda=0; cycada=MagFdoUHAVyTsVBYcwYEVj+ZDVwh9KIhTOCOA4vkxas=; Session_id=3:1564263273.5.0.1564263273959:MBP8bQ:4f.1|730767098.0.2|202770.226029.KFo-kF-58mjTeWTbjVa6vOt0uho; sessionid2=3:1564263273.5.0.1564263273959:MBP8bQ:4f.1|730767098.0.2|202770.977691.x4fpwlzcyiFtO2XHjwzYyClJM4w; L=AFFXaURHeG5HQGZUUk9KWUV9Ql9gfVsAIUpyFQcFIA==.1564263273.13939.322420.96a85f389598c29844f1385f911de503; yandex_login=r00tl0l; lastVisitedPage=%7B%22730767098%22%3A%22%2Fusers%2Fr00tl0l%2Fplaylists%22%7D; yabs-frequency=/4/200004OSFbq00000/; _ym_uid=1564325428420914521; _ym_d=1564325428; _ym_isad=2; bltsr=1; ys=wprid.1564385321744303-239963555370250067400035-sas1-1040; device_id=\"ade8863d0409e27949cc4b7e7a9292f270032c620\"; active-browser-timestamp=1564398801396; pepsi_year=today; instruction=1"} # 

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
