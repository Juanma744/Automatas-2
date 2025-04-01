import sys
from PyQt6.QtWidgets import QApplication
from Interfaz import AnalizadorCodigo

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AnalizadorCodigo()
    ventana.show()
    sys.exit(app.exec())

