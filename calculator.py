"""简易计算器：基于 PySide6 的四则运算图形界面。

表达式不使用 eval，而是用 ast 解析后按白名单逐节点计算，
避免用户输入被当作任意 Python 代码执行。
"""

import ast       # 标准库：把表达式解析成语法树，便于逐节点校验
import math      # 标准库：判断计算结果是不是无穷大或 NaN
import operator  # 标准库：提供 add / sub / mul / truediv / mod 等运算函数
import sys       # 标准库：传递命令行参数并返回进程退出码

from PySide6.QtCore import Qt  # Qt 基础命名空间，这里只用到对齐方式枚举
from PySide6.QtWidgets import (  # 从控件模块导入界面元素
    QApplication,  # 应用程序对象，每个 GUI 程序有且只有一个
    QGridLayout,   # 网格布局，用来摆放数字键与运算符键
    QLineEdit,     # 单行输入框，这里当作只读的显示屏使用
    QPushButton,   # 按钮控件，数字和运算符都用它
    QVBoxLayout,   # 垂直布局，用来纵向排列显示屏和键盘区
    QWidget,       # 基础窗口控件，计算器主类继承它
)

# 二元运算符白名单：键是语法树节点类型，值是对应的运算函数
_BIN_OPS = {
    ast.Add: operator.add,       # 加号 -> 加法
    ast.Sub: operator.sub,       # 减号 -> 减法
    ast.Mult: operator.mul,      # 乘号 -> 乘法
    ast.Div: operator.truediv,   # 除号 -> 真除法，除数为 0 会抛异常
    ast.Mod: operator.mod,       # 百分号 -> 取余
}

# 一元运算符白名单：只允许正号和负号
_UNARY_OPS = {
    ast.UAdd: operator.pos,  # 正号 -> 原样返回数值
    ast.USub: operator.neg,  # 负号 -> 取相反数
}

# 表达式最大长度，防止超长输入拖慢解析
_MAX_LENGTH = 100


def safe_eval(expression: str) -> float:
    """安全地计算一个只含数字与四则运算的表达式。

    Args:
        expression: 待计算的表达式字符串，例如 "1+2*3"。

    Returns:
        表达式的计算结果，统一为 float 类型。

    Raises:
        ValueError: 表达式为空、过长、语法错误或含不允许的语法时抛出。
    """
    text = expression.strip()  # 去掉首尾空白，避免全空格被误判为有效表达式
    if not text:  # 空表达式没有可计算的内容
        raise ValueError("表达式为空")  # 抛出明确的错误交给调用方展示
    if len(text) > _MAX_LENGTH:  # 超长输入直接拒绝
        raise ValueError("表达式过长")  # 给出可读的错误原因
    try:  # 解析可能失败，需要单独捕获
        tree = ast.parse(text, mode="eval")  # mode="eval" 只接受单条表达式，拒绝语句
    except SyntaxError as exc:  # 语法错误说明用户输入不合法
        raise ValueError("表达式格式错误") from exc  # 统一转换成 ValueError 便于上层处理
    return _eval_node(tree.body)  # 从根节点开始递归求值


def _eval_node(node: ast.AST) -> float:
    """递归计算语法树中的一个节点。

    Args:
        node: ast 模块解析出的节点对象。

    Returns:
        该节点对应的数值结果。

    Raises:
        ValueError: 节点类型不在白名单内时抛出。
    """
    if isinstance(node, ast.Constant):  # 叶子节点：数字常量
        if isinstance(node.value, (int, float)):  # 只接受数字，拒绝字符串等其他常量
            return float(node.value)  # 统一转成 float，方便后续计算与显示
        raise ValueError("只支持数字")  # 非数字常量一律拒绝
    if isinstance(node, ast.BinOp):  # 分支一：二元运算，例如 a + b
        left = _eval_node(node.left)  # 先递归求左操作数
        right = _eval_node(node.right)  # 再递归求右操作数
        func = _BIN_OPS.get(type(node.op))  # 按运算符类型查白名单
        if func is None:  # 不在白名单内说明是不支持的运算符
            raise ValueError("不支持的运算符")  # 拒绝执行
        return func(left, right)  # 调用白名单里的函数完成真正的计算
    if isinstance(node, ast.UnaryOp):  # 分支二：一元运算，例如 -5
        func = _UNARY_OPS.get(type(node.op))  # 查一元运算符白名单
        if func is None:  # 只允许正负号
            raise ValueError("不支持的运算符")  # 其他一元运算符一律拒绝
        return func(_eval_node(node.operand))  # 先求操作数，再取正或取负
    raise ValueError("不支持的表达式")  # 其余所有节点类型（函数调用、下标等）都拒绝


class Calculator(QWidget):
    """计算器主窗口，负责界面布局与按键交互。"""

    def __init__(self) -> None:
        """初始化窗口、显示屏与全部按键。"""
        super().__init__()  # 调用父类构造函数，完成 QWidget 的基础初始化
        self.setWindowTitle("简易计算器")  # 设置窗口标题栏的文字
        self.setFixedSize(320, 460)  # 固定窗口尺寸，避免缩放导致按键变形

        self._expression = ""  # 保存当前输入的表达式文本，空串表示还没有输入

        self.display = QLineEdit()  # 创建单行输入框作为显示屏
        self.display.setReadOnly(True)  # 设为只读，用户只能通过按钮输入
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 文字右对齐，符合计算器习惯
        self.display.setFixedHeight(70)  # 固定显示屏高度
        self.display.setText("0")  # 初始显示 0，而不是空白
        self.display.setStyleSheet(  # 用 QSS 调整显示屏的外观
            "font-size: 26px; padding: 8px; background: #ffffff;"  # 放大字号并留出内边距
            "border: 1px solid #d0d4dc; border-radius: 6px;"  # 浅灰边框与圆角
        )  # 样式表字符串结束

        root = QVBoxLayout(self)  # 根布局统一管理显示屏和键盘区
        root.setSpacing(10)  # 两个区块之间留 10 像素间隙
        root.addWidget(self.display)  # 显示屏放在最上方
        root.addLayout(self._build_keypad())  # 键盘区放在显示屏下方

    def _build_keypad(self) -> QGridLayout:
        """创建数字与运算符按键区。

        Returns:
            已完成布局与信号连接的 QGridLayout 实例。
        """
        grid = QGridLayout()  # 创建网格布局承载所有按键
        grid.setSpacing(6)  # 按键之间留 6 像素间隙

        keys = [  # 每个元组是 (显示文字, 行, 列)
            ("C", 0, 0), ("←", 0, 1), ("%", 0, 2), ("÷", 0, 3),  # 第一行：清除、退格、取余、除
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),  # 第二行：7 8 9 和乘号
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("−", 2, 3),  # 第三行：4 5 6 和减号
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),  # 第四行：1 2 3 和加号
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2),  # 第五行：0、小数点、等号
        ]

        for text, row, column in keys:  # 遍历按键定义，逐个创建按钮
            button = QPushButton(text)  # 用显示文字创建按钮
            button.setFixedHeight(52)  # 固定按钮高度，保证排列整齐
            button.setStyleSheet(  # 用 QSS 统一按钮外观
                "font-size: 18px; border: 1px solid #d0d4dc;"  # 字号与边框
                "border-radius: 6px; background: #ffffff;"  # 圆角与背景色
            )  # 样式表字符串结束
            button.clicked.connect(  # 把点击信号连接到统一处理函数
                lambda _checked=False, value=text: self._on_key(value)  # 用默认参数绑定当前文字
            )  # 信号连接结束
            span = 2 if text == "=" else 1  # 等号按钮横跨两列，视觉上更醒目
            grid.addWidget(button, row, column, 1, span)  # 把按钮放进指定行列

        return grid  # 返回组装好的网格布局

    def _on_key(self, key: str) -> None:
        """处理一次按键点击。

        Args:
            key: 被点击按钮上显示的文字。
        """
        if key == "C":  # 按下清除键
            self._expression = ""  # 清空内部表达式
        elif key == "←":  # 按下退格键
            self._expression = self._expression[:-1]  # 去掉最后一个字符
        elif key == "=":  # 按下等号键
            self._calculate()  # 交给专门的计算函数处理
            return  # 计算函数内部已更新显示，这里直接返回
        else:  # 其余情况都是数字或运算符
            self._expression += key  # 把字符追加到表达式末尾
        self.display.setText(self._expression or "0")  # 表达式为空时显示 0

    def _calculate(self) -> None:
        """计算当前表达式，并把结果写回显示屏。"""
        try:  # 计算过程可能抛出多种异常
            result = safe_eval(self._to_python(self._expression))  # 先转成 Python 语法再安全求值
        except ZeroDivisionError:  # 除数为 0 属于常见输入错误
            self._show_error("除数不能为 0")  # 给出针对性的提示
            return  # 结束本次计算
        except ValueError as exc:  # 空表达式、格式错误、不支持的语法都走这里
            self._show_error(str(exc))  # 把具体原因展示给用户
            return  # 结束本次计算
        if not math.isfinite(result):  # 结果溢出成无穷大或 NaN 时
            self._show_error("结果超出范围")  # 拒绝显示无意义的数值
            return  # 结束本次计算
        text = self._format_number(result)  # 把浮点数转成简洁的显示文本
        self._expression = text  # 把结果留在表达式里，支持连续计算
        self.display.setText(text)  # 更新显示屏

    def _to_python(self, expression: str) -> str:
        """把界面上的运算符符号转换成 Python 能识别的符号。

        Args:
            expression: 界面上显示的表达式，例如 "6×7"。

        Returns:
            可交给 ast 解析的等价表达式，例如 "6*7"。
        """
        return (  # 依次替换三种界面符号
            expression
            .replace("×", "*")  # 乘号转成星号
            .replace("÷", "/")  # 除号转成正斜杠
            .replace("−", "-")  # 全角减号转成半角减号
        )

    def _format_number(self, value: float) -> str:
        """把计算结果格式化成适合显示的字符串。

        Args:
            value: 已经计算出的数值。

        Returns:
            不含多余小数位和小数点的文本。
        """
        if value == int(value) and abs(value) < 1e15:  # 整数值且未超出安全范围
            return str(int(value))  # 显示成整数，去掉 ".0"
        return f"{value:.10g}"  # 其余情况保留最多 10 位有效数字

    def _show_error(self, message: str) -> None:
        """在显示屏上展示错误信息，并重置计算状态。

        Args:
            message: 要展示给用户的错误说明。
        """
        self.display.setText(f"错误：{message}")  # 把错误原因写到显示屏
        self._expression = ""  # 清空表达式，避免错误状态延续下去


def main() -> int:
    """程序入口：创建应用、显示窗口并进入事件循环。

    Returns:
        事件循环退出时的状态码，0 表示正常退出。
    """
    app = QApplication(sys.argv)  # 创建应用对象，接收命令行参数
    window = Calculator()  # 实例化计算器窗口
    window.show()  # 把窗口显示到屏幕上
    return app.exec()  # 进入事件循环，直到窗口被关闭


if __name__ == "__main__":  # 仅当脚本被直接运行时执行
    sys.exit(main())  # 用 main 的返回值作为进程退出码
