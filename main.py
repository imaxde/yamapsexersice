import sys
import requests
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel


class Mapp(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinates = [56.107161, 57.975429]
        self.scale = 12
        self.initUI()

    def getImage(self, ll, zoom):
        server_address = "https://static-maps.yandex.ru/v1?"
        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": ",".join(list(map(str, ll))),
            "z": str(zoom),
            "size": "450,450",
            "style": "tags.any:admin|stylers.visibility:off",
            "format": "json"}
        response = requests.get(server_address, params=params)
        return QImage().fromData(QByteArray(response.content))

    def initUI(self):
        self.setGeometry(100, 100, 450, 450)
        self.setWindowTitle("Карты")
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(450, 450)
        self.image.setPixmap(QPixmap(self.getImage(map(str, self.coordinates), self.scale)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            if self.scale > 0:
                self.scale -= 1
        if event.key() == Qt.Key.Key_PageDown:
            if self.scale < 21:
                self.scale += 1
        self.updateMap()

    def updateMap(self):
        self.image.setPixmap(QPixmap(self.getImage(map(str, self.coordinates), self.scale)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mapp()
    ex.show()
    sys.exit(app.exec())
