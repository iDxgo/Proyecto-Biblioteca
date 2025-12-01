from PyQt5 import QtWidgets
import sys
from carga_ui.carga_login import Load_ui_login

def main():
    app = QtWidgets.QApplication(sys.argv)
    login = Load_ui_login()
    login.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()