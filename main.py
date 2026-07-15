from pathlib import Path
from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """程序主入口函数"""
    # 确保 data 目录存在
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        # print(f"已创建数据目录: {data_dir}")

    # 创建 QApplication 实例
    app = QApplication([])

    # 样式由 MainWindow.apply_theme() 加载，这里不再加载

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 进入事件循环
    app.exec()


if __name__ == "__main__":
    main()
