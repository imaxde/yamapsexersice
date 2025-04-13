import sys
import requests
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit


class Mapp(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinates = [56.107161, 57.975429]
        self.focus_point = [0, 0]
        self.zoom = 12
        self.theme = True
        self.initUI()

    def getImage(self):
        server_address = "https://static-maps.yandex.ru/v1?"
        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": ",".join(list(map(str, self.coordinates))),
            "z": str(self.zoom),
            "size": "450,450",
            "theme": "light" if self.theme else "dark",
            "format": "json"}
        if self.focus_point[0]:
            params["pt"] = ",".join(list(map(str, self.focus_point))) + ",flag"
        response = requests.get(server_address, params=params)
        return QImage().fromData(QByteArray(response.content))

    def initUI(self):
        self.setGeometry(100, 100, 450, 500)
        self.setWindowTitle("Карты")
        self.themeBtn = QPushButton("🌑", self)
        self.themeBtn.move(10, 460)
        self.themeBtn.resize(30, 30)
        self.themeBtn.setToolTip("Сменить тему")
        self.themeBtn.clicked.connect(self.changeTheme)
        self.field = QLineEdit(self)
        self.field.move(59, 460)
        self.field.resize(180, 30)
        self.field.setPlaceholderText("Поиск")
        self.searchBtn = QPushButton("🔎", self)
        self.searchBtn.move(240, 460)
        self.searchBtn.resize(30, 30)
        self.searchBtn.setToolTip("Искать")
        self.searchBtn.clicked.connect(self.geoSearch)
        self.resetBtn = QPushButton("↩️", self)
        self.resetBtn.move(270, 460)
        self.resetBtn.resize(30, 30)
        self.resetBtn.setToolTip("Сброс поискового результата")
        self.resetBtn.clicked.connect(self.resetSearch)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(450, 450)
        self.image.setPixmap(QPixmap(self.getImage()))

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key.Key_Minus or event.key() == Qt.Key.Key_PageUp) and self.zoom > 0:
            self.zoom -= 1
        elif (event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_PageDown) and self.zoom < 21:
            self.zoom += 1
        elif event.key() == Qt.Key.Key_Up and self.coordinates[1] < 85:
            self.coordinates[1] += 10 / (2 ** (self.zoom - 1))
        elif event.key() == Qt.Key.Key_Down and self.coordinates[1] > -85:
            self.coordinates[1] -= 10 / (2 ** (self.zoom - 1))
        elif event.key() == Qt.Key.Key_Right and self.zoom < 179:
            self.coordinates[0] += 10 / (2 ** (self.zoom - 1))
        elif event.key() == Qt.Key.Key_Left and self.zoom > -179:
            self.coordinates[0] -= 10 / (2 ** (self.zoom - 1))
        self.updateMap()

    def changeTheme(self):
        self.theme = not self.theme
        self.themeBtn.setText("🌑" if self.theme else "🌕")
        self.updateMap()

    def updateMap(self):
        self.coordinates[0] = round(self.coordinates[0], 6)
        self.coordinates[1] = round(self.coordinates[1], 6)
        self.image.setPixmap(QPixmap(self.getImage()))

    def geoSearch(self):
        url = "https://search-maps.yandex.ru/v1/"
        org_search_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "text": self.field.text(),
            "lang": "ru_RU",
            "ll": ",".join(list(map(str, self.coordinates)))
        }
        response = requests.get(url, params=org_search_params)
        data = response.json()
        self.focus_point = data["features"][0]["geometry"]["coordinates"]
        self.coordinates = self.focus_point.copy()
        self.zoom = 17
        self.field.clearFocus()
        self.updateMap()

    def resetSearch(self):
        self.field.clear()
        self.field.clearFocus()
        self.focus_point = [0, 0]
        self.updateMap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mapp()
    ex.show()
    sys.exit(app.exec())
