import sys
from PySide6.QtWidgets import QApplication, QMainWindow


def main():
    # Punto de entrada: arranca la app y abre la ventana principal vacía.
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Liriel — Gestor de hojas D&D 5.5e")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()