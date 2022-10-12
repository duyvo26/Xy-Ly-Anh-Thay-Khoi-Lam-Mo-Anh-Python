# import  CheAnh
#
# CheAnh.CheAnh(100, 200, 300,"img.jpg", 2)


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("main.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()