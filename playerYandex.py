import vlc, time
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize
import design  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

	def __init__(self):
		self.track = {'name': "Sleep When We're Dead", 'artist': 'ItaloBrothers', 'download': 'https://s112sas.storage.yandex.net/get-mp3/e43431431c2e7b659335ff91aca7e990/00058ef669438385/rmusic/U2FsdGVkX190ryo3y53-cmbOMuvX4eKBPWF_-IulKSoGc8nafNByOGkYQwNQVQ4DGQqFKd_HLez0YS_4rdACX4T9nvlJZDrlgTrm_cxtU54/fe661e80992acdf52467b7aee6f769a9c2f3136944ec938437121725b0da26d6'}
		self.PlayNstop = True
		self.inst = vlc.Instance()
		self.med = self.inst.media_new(self.track["download"])
		self.p = self.med.player_new_from_media()
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.pushButton_2.clicked.connect(self.wwww)# Выполнить функцию browse_folder
		self.label_2.setText(self.track["name"])
		self.label_4.setText(self.track["artist"])
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		self.tray_icon.activated.connect(self.action)
		self.tray_icon.show()
		self.hide()

	def action(self):
		self.show()
		print('System tray icon clicked.')

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
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  

#inst = vlc.Instance()
#med = inst.media_new('https://s46myt.storage.yandex.net/get-mp3/e43431431c2e7b659335ff91aca7e990/00058ed03f14fc36/rmusic/U2FsdGVkX1_1kHImJJFa7_az8qL-6_iSU_aYvOLV7kXMaMzS92YScXalOK-E3FczdqQnWumUZAq5hkmOcA2Uj_IScfqxl4wusZ_Q9r-5luI/0218e6e315ec609872b616fc9912ec738847612a24cebae5bbf12b0d9891376b')
#p = med.player_new_from_media()
#p.play()
#time.sleep(111)