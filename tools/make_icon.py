"""生成计算器图标 app.ico（多尺寸），无需外部素材、无版权问题。"""

import sys

from PIL import Image, ImageDraw

SIZE = 256  # 先按 256x256 绘制，最后再缩放成多尺寸

BG = (36, 52, 71, 255)        # 机身深蓝灰
SCREEN = (232, 240, 250, 255)  # 显示屏浅色
KEY = (96, 112, 136, 255)      # 普通按键
ACCENT = (45, 127, 249, 255)   # 等号按键强调色


def draw() -> Image.Image:
    """绘制 256x256 的图标底图。

    Returns:
        绘制完成的 RGBA 图像。
    """
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((16, 8, 240, 248), radius=36, fill=BG)   # 机身
    d.rounded_rectangle((40, 34, 216, 96), radius=12, fill=SCREEN)  # 显示屏

    x0, y0 = 40, 122  # 按键区左上角
    cell_w, cell_h, gap = 48, 30, 8  # 按键宽、高与间距

    for row in range(3):
        for col in range(3):
            x = x0 + col * (cell_w + gap)
            y = y0 + row * (cell_h + gap)
            d.rounded_rectangle((x, y, x + cell_w, y + cell_h), radius=8, fill=KEY)

    # 右下角改成强调色（等号键）
    ex = x0 + 2 * (cell_w + gap)
    ey = y0 + 2 * (cell_h + gap)
    d.rounded_rectangle((ex, ey, ex + cell_w, ey + cell_h), radius=8, fill=ACCENT)

    # 在显示屏上画两条横线，暗示数字
    d.rounded_rectangle((150, 50, 200, 60), radius=5, fill=(120, 140, 165, 255))
    d.rounded_rectangle((150, 70, 186, 80), radius=5, fill=(170, 185, 205, 255))

    return img


def main() -> int:
    """生成并保存 app.ico。

    Returns:
        进程退出码，0 表示成功。
    """
    if len(sys.argv) < 2:  # 需要输出路径
        print("用法: python make_icon.py <输出路径>")
        return 1

    out = sys.argv[1]
    base = draw()
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    base.save(out, format="ICO", sizes=sizes)
    print(f"已生成: {out}")
    return 0


if __name__ == "__main__":  # 仅当脚本被直接运行时执行
    sys.exit(main())
