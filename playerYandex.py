import vlc, time
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

	def __init__(self):

		self.PlayNstop = True
		self.inst = vlc.Instance()
		self.med = self.inst.media_new('https://s21vla.storage.yandex.net/get-mp3/e43431431c2e7b659335ff91aca7e990/00058ef5f63e5e17/rmusic/U2FsdGVkX1--0aBk2k4HtZ7ub3-sSs7wjohKZLJoJmcPDBFhG3gsC0_t0Ypsns8SJi6bXSdTEePEOo74VnJvA1xuXfMlRKm1v2bqoSEFMn4/5f9be9a91a2d780553ab2f831ec59ccf4d9ebbd444801b5292f999fc2f6a67df')
		self.p = self.med.player_new_from_media()
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.pushButton_2.clicked.connect(self.wwww)# Выполнить функцию browse_folder

	def wwww(self):
		if self.PlayNstop :
			self.p.play()
			self.PlayNstop = False
		else:
			self.p.pause()
			self.PlayNstop = True

def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = ExampleApp()  # Создаём объект класса ExampleApp
	window.show()  # Показываем окно
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  

#inst = vlc.Instance()
#med = inst.media_new('https://s46myt.storage.yandex.net/get-mp3/e43431431c2e7b659335ff91aca7e990/00058ed03f14fc36/rmusic/U2FsdGVkX1_1kHImJJFa7_az8qL-6_iSU_aYvOLV7kXMaMzS92YScXalOK-E3FczdqQnWumUZAq5hkmOcA2Uj_IScfqxl4wusZ_Q9r-5luI/0218e6e315ec609872b616fc9912ec738847612a24cebae5bbf12b0d9891376b')
#p = med.player_new_from_media()
#p.play()
#time.sleep(111)