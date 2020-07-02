from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class MessengerApp(clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()  # инициализация родителей
        self.setupUi(self)  # инициализация UI
        self.sendButton.pressed.connect(self.sendMessege)
        self.last_message_time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)

    def sendMessege(self):
        username = self.username_line.text()
        password = self.lineEdit_2.text()
        text = self.messageEdit.toPlainText()

        if not username:
            self.addText('ERROR: username is empty!')
            self.addText(' ')
            return
        if not password:
            self.addText('ERROR: password is empty!')
            self.addText(' ')
            return
        if not text:
            self.addText('ERROR: text is empty!')
            self.addText(' ')
            return

        response = requests.post('http://127.0.0.1:5000/send',
                                 json={"username": username,
                                       "password": password, "text": text})
        if not response.json()['ok']:
            self.addText('ERROR: Access denied')
            self.addText(' ')
            return

        self.messageEdit.clear()
        self.messageEdit.repaint()

    def addText(self, text):
        self.messageBrowser.append(text)
        self.messageBrowser.repaint()

    def getUpdates(self):
        response = requests.get(
            'http://127.0.0.1:5000/history',
            params={'after': self.last_message_time})
        data = response.json()
        for message in data['messages']:
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
            self.addText(beauty_time + '' + message['username'])
            self.addText(message['text'])
            self.addText(' ')
            self.last_message_time = message['time']


app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
app.exec_()
