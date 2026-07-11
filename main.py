from pathlib import Path
from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    app = QApplication([])
    style_path = (
        Path(__file__).parent
        / "src"
        / "gui"
        / "style.qss"
    )
    app.setStyleSheet(
        style_path.read_text(
            encoding="utf-8"
        )
    )
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()