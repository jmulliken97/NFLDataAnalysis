import sys
from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    extra = {
        'font_family': 'Roboto',
        'font_size': '10px'  # Adjust the size
    }
    apply_stylesheet(app, theme='dark_teal.xml', extra=extra)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
