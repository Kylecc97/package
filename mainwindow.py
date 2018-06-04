import webbrowser
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
import UI_mainwindow
import camera_choose_gui
import sys
sys.path.append("/users/lyx/Documents/face_recognition/background")
class MainWindow(QMainWindow,UI_mainwindow.Ui_MainWindow):

    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)

    def on_pushButton_3_clicked(self):
        my_dialog = camera_choose_gui.Dialog()
        my_dialog.exec()

    def on_action_triggered(self):
        author_information = u'作者：LYX' + '\n'
        author_information += u'邮箱：kyleliu0313@gmail.com' + '\n'
        author_information += u'github：https://github.com/Kylecc97' + '\n'
        button = QMessageBox.question(self, '',author_information + '是否访问作者的github？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if button == QMessageBox.Yes:
            webbrowser.open('https://github.com/Kylecc97')
        else:
            pass

    def on_action_2_triggered(self):
        QMessageBox.information(self, u'操作说明', u'暂时无操作说明', QMessageBox.Yes)

    def on_action_PYQT_triggered(self):
        QMessageBox.aboutQt(self, '关于PYQT')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ui = MainWindow()
    Ui.show()
    sys.exit(app.exec_())
