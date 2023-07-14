from frontend.modules import ui_mdwidget
from PyQt5 import QtWidgets as qtw


class MdWidget(qtw.QWidget, ui_mdwidget.Ui_Form):
    def __init__(self, parent=None):
        super(MdWidget, self).__init__(parent)
        self.setupUi(self)
        self.test()

    def test(self):
        self.a1_value.setText("Hello")
        return
