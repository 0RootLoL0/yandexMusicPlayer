import sys
import json 
import socket
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle
from PyQt5.QtCore import QSize
import design  # подключаем дизаен


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

	def __init__(self):
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.SERVER = "127.0.0.1"  # адресс YaMPD
		self.PORT = 5592  # порт для YaMPD
		self.showIS = False  # переменная в которой храниться состояние окна ()
		self.pushButton_3.clicked.connect(self.onwardYaMPC)
		self.pushButton_2.clicked.connect(self.pauseYaMPC)
		self.pushButton.clicked.connect(self.backYaMPC)

		
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		self.tray_icon.activated.connect(self.action)
		self.tray_icon.show()
		self.hide()

	def pauseYaMPC(self): 
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((self.SERVER, self.PORT))
		client.sendall(bytes("pause",'UTF-8'))
		data = client.recv(1024)
		print(data.decode())
		client.close()
		self.hide()

	def backYaMPC(self):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((self.SERVER, self.PORT))
		client.sendall(bytes("back",'UTF-8'))
		data = client.recv(1024)
		print(data.decode())
		client.close()
		self.hide()

	def onwardYaMPC(self):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((self.SERVER, self.PORT))
		client.sendall(bytes("onward",'UTF-8'))
		data = client.recv(1024)
		print(data.decode())
		client.close()
		self.hide()


		
	def action(self):
		if self.showIS:
			self.hide()
			self.showIS = False
		else:
			client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client.connect((self.SERVER, self.PORT))
			client.sendall(bytes("returnName",'UTF-8'))
			data = client.recv(1024)
			rnj = json.loads(data.decode())
			client.close()
			self.label_2.setText(rnj["title"])
			self.label_4.setText(rnj["artists"][0]["name"])
			self.show()
			self.showIS = True
		print('System tray icon clicked.')

def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = ExampleApp()  # Создаём объект класса ExampleApp
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':
	main()  