"""主程序入口：主窗口框架来自 mainwindow.ui，计算器作为子控件嵌入。

界面（标签页、按钮）用 Qt Designer 拖拽生成，业务逻辑全部写在这里。
"""

import sys  # 标准库：传递命令行参数、读取打包后的临时资源目录
import traceback  # 标准库：把未捕获异常格式化成可读的堆栈
from pathlib import Path  # 标准库：拼接资源文件路径

from PySide6.QtCore import Qt  # Qt 命名空间，这里用居中对方的对齐枚举
from PySide6.QtGui import QIcon  # 图标类，用来设置窗口左上角与任务栏图标
from PySide6.QtWidgets import (  # 从控件模块导入界面元素
    QApplication,  # 应用程序对象，每个 GUI 程序有且只有一个
    QMainWindow,   # 主窗口基类，界面来自 mainwindow.ui
    QMessageBox,   # 消息框，这里用来展示未捕获的异常
)

from calculator import Calculator  # 复用上一轮写好的计算器控件
from ui_mainwindow import Ui_MainWindow  # uic 从 mainwindow.ui 生成的界面类


def resource_path(name: str) -> Path:
    """返回资源文件的绝对路径，兼容源码运行与 PyInstaller 打包两种场景。

    Args:
        name: 资源文件名，例如 "app.ico"。

    Returns:
        该资源在当前运行环境下的完整路径。
    """
    base = getattr(sys, "_MEIPASS", None)  # 打包后 PyInstaller 会把资源解压到临时目录
    if base is None:  # 源码运行时不存在 _MEIPASS
        base = Path(__file__).resolve().parent  # 退回到脚本所在目录
    return Path(base) / name  # 拼接出完整的资源路径


def install_excepthook() -> None:
    """安装全局异常钩子，让未捕获的异常以弹窗形式出现。

    打包成无控制台的 exe 后，异常只会让进程直接退出，
    用户看不到任何信息，因此必须在这里兜底。
    """

    def _hook(exc_type, exc_value, exc_tb) -> None:  # 定义真正的钩子函数
        detail = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))  # 完整堆栈
        box = QMessageBox()  # 手动构造消息框，方便塞入详细文本
        box.setIcon(QMessageBox.Icon.Critical)  # 用红色错误图标
        box.setWindowTitle("程序出错了")  # 弹窗标题
        box.setText(f"{exc_type.__name__}: {exc_value}")  # 一句话说明错误类型和原因
        box.setDetailedText(detail)  # 折叠区里的完整堆栈，方便排查
        box.exec()  # 阻塞显示，直到用户点确定

    sys.excepthook = _hook  # 把钩子挂到解释器上，之后所有未捕获异常都会走这里


class MainWindow(QMainWindow):
    """主窗口，负责装配界面与业务逻辑。"""

    def __init__(self) -> None:
        """初始化主窗口，并把手写的计算器控件嵌入「计算器」标签页。"""
        super().__init__()  # 调用父类构造函数，完成窗口基础初始化
        self.ui = Ui_MainWindow()  # 实例化 uic 生成的界面类
        self.ui.setupUi(self)  # 按 .ui 里的描述把控件挂到当前窗口上

        self.setWindowIcon(QIcon(str(resource_path("app.ico"))))  # 设置窗口与任务栏图标

        self._count = 0  # 首页按钮的点击计数
        self.ui.button.clicked.connect(self._on_click)  # 把按钮点击接到槽函数

        self.calculator = Calculator()  # 创建计算器控件实例
        self.ui.calculatorLayout.addWidget(  # 把计算器塞进「计算器」标签页的布局
            self.calculator,  # 被添加的控件
            0,  # 伸缩因子为 0，不抢占额外空间
            Qt.AlignmentFlag.AlignCenter,  # 在标签页内居中显示
        )  # 添加结束

    def _on_click(self) -> None:
        """首页按钮的点击处理：累加计数并刷新标签文字。"""
        self._count += 1  # 计数加一
        self.ui.label.setText(f"点击了 {self._count} 次")  # 把新计数显示到标签上


def main() -> int:
    """程序入口：创建应用、显示主窗口并进入事件循环。

    Returns:
        事件循环退出时的状态码，0 表示正常退出。
    """
    install_excepthook()  # 先装异常钩子，保证后续出错能被看到
    app = QApplication(sys.argv)  # 创建应用对象，接收命令行参数
    window = MainWindow()  # 实例化主窗口
    window.show()  # 把窗口显示到屏幕上
    return app.exec()  # 进入事件循环，直到窗口被关闭


if __name__ == "__main__":  # 仅当脚本被直接运行时执行
    sys.exit(main())  # 用 main 的返回值作为进程退出码
