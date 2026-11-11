"""第一个 PySide6 程序：界面来自 mainwindow.ui，可用 Qt Designer 拖拽修改。"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._count = 0
        self.ui.button.clicked.connect(self._on_click)

    def _on_click(self) -> None:
        self._count += 1
        self.ui.label.setText(f"点击了 {self._count} 次")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())