# import sys
# sys.path.append(str(Path(__file__).parent / "src"))
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from src.gui.main_window import MainWindow
from src.core.config import Config


def load_qss():
    """加载 QSS 样式文件"""
    style_path = Path(__file__).parent / "src" / "gui" / "style.qss"
    return style_path.read_text(encoding="utf-8")


def apply_theme(app):
    """应用主题配置"""
    config = Config()
    settings = config.load()
    color = settings.get("color", "#6366f1")

    qss = load_qss()
    qss = qss.replace("PRIMARY_COLOR", color)
    app.setStyleSheet(qss)


def main():
    """主入口函数"""
    app = QApplication([])

    # 加载主题
    apply_theme(app)

    # 设置窗口图标
    app.setWindowIcon(QIcon("./icons/main.ico"))

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
