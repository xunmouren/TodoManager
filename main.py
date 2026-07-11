import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))
from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    # 创建应用程序实例
    app = QApplication([])
    # 拼接文件路径
    style_path = (Path(__file__).parent/"src"/"gui"/"style.qss")
    # 加载样式
    app.setStyleSheet(style_path.read_text(encoding="utf-8"))
    # 创建主窗口
    window = MainWindow()
    # 显示主窗口
    window.show()
    # 进入事件循环
    app.exec()

if __name__ == "__main__":
    main()