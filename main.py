# main.py 顶部添加
import sys
import os

# 将当前目录添加到 Python 搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication


from src.gui.main_window import MainWindow


def main():

    app = QApplication([])

    app.setStyleSheet(
        open(
            "src/gui/style.qss",
            encoding="utf-8"
        ).read()
    )

    window = MainWindow()

    window.show()

    app.exec()


if __name__ == "__main__":
    main()