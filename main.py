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
        if event.key() == Qt.Key.Key_PageUp and self.scale > 0:
            self.scale -= 1
        elif event.key() == Qt.Key.Key_PageDown and self.scale < 21:
            self.scale += 1
        elif event.key() == Qt.Key.Key_Up and self.coordinates[1] < 85:
            self.coordinates[1] += 10 / (2 ** (self.scale - 1))
        elif event.key() == Qt.Key.Key_Down and self.coordinates[1] > -85:
            self.coordinates[1] -= 10 / (2 ** (self.scale - 1))
        elif event.key() == Qt.Key.Key_Right and self.scale < 179:
            self.coordinates[0] += 10 / (2 ** (self.scale - 1))
        elif event.key() == Qt.Key.Key_Left and self.scale > -179:
            self.coordinates[0] -= 10 / (2 ** (self.scale - 1))
        self.updateMap()

    def updateMap(self):
        self.coordinates[0] = round(self.coordinates[0], 6)
        self.coordinates[1] = round(self.coordinates[1], 6)
        self.image.setPixmap(QPixmap(self.getImage(map(str, self.coordinates), self.scale)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mapp()
    ex.show()
    sys.exit(app.exec())
