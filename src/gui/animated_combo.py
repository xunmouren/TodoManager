from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

class AnimatedComboBox(QComboBox):
    """带动画效果的下拉选择框，弹出时带有淡入动画。"""
    def __init__(self, parent=None):
        """初始化动画下拉框。"""
        super().__init__(parent)
        self.animation = None

    def showPopup(self):
        """重写弹出方法，添加淡入动画效果。"""
        super().showPopup()
        popup = self.view()
        popup.setWindowOpacity(0)
        self.animation = QPropertyAnimation(popup, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
