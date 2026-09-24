# 复利计算器（Tkinter 图形界面，含复利/单利对比表格与增长曲线图）
# 复利公式：本金 × (1 + 年利率) ^ 年数
# 单利公式：本金 × (1 + 年利率 × 年数)

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")  # 使用 Tkinter 后端
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 让 matplotlib 正常显示中文与负号
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 统一中文字体
UI_FONT = "Microsoft YaHei"


# ---------- 计算逻辑（不随界面美化改动）----------
def calculate(principal, rate):
    """计算 10、20、30 年的复利终值、单利终值及差额，用于表格展示"""
    results = []
    for years in (10, 20, 30):
        compound = principal * (1 + rate) ** years   # 复利终值
        simple = principal * (1 + rate * years)      # 单利终值
        diff = compound - simple                      # 差额
        results.append((years, compound, simple, diff))
    return results


def calculate_series(principal, rate, max_years=30):
    """生成 0~max_years 每一年的复利与单利序列，用于绘制曲线"""
    years = list(range(0, max_years + 1))
    compound = [principal * (1 + rate) ** y for y in years]   # 复利曲线
    simple = [principal * (1 + rate * y) for y in years]     # 单利曲线
    return years, compound, simple


def clear_tree(tree):
    """清空表格中的所有行"""
    for item in tree.get_children():
        tree.delete(item)


def plot_curves(fig, ax, canvas, principal, rate):
    """在图上绘制复利与单利增长曲线"""
    ax.clear()
    years, compound, simple = calculate_series(principal, rate)
    ax.plot(years, compound, label="复利", color="tab:red", marker="o", markersize=3)
    ax.plot(years, simple, label="单利", color="tab:blue", marker="s", markersize=3)
    ax.set_xlabel("年份")
    ax.set_ylabel("金额（元）")
    ax.set_title("复利与单利增长曲线（0~30 年）")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    canvas.draw()


def on_calculate(entry_principal, entry_rate, tree, fig, ax, canvas):
    """点击"开始计算"按钮时触发：读取输入、校验、更新表格与曲线图"""
    try:
        principal = float(entry_principal.get())            # 读取本金
        rate = float(entry_rate.get()) / 100                # 百分数转小数：5 → 0.05
    except ValueError:
        clear_tree(tree)
        tree.insert("", "end", values=("-", "请输入有效数字", "", ""))  # 非数字提示
        return

    # 输入校验：本金必须大于 0，年利率不能为负数
    if principal <= 0:
        clear_tree(tree)
        tree.insert("", "end", values=("-", "本金必须大于 0", "", ""))
        return
    if rate < 0:
        clear_tree(tree)
        tree.insert("", "end", values=("-", "年利率不能为负数", "", ""))
        return

    # 更新 10/20/30 年对比表格
    clear_tree(tree)
    for years, compound, simple, diff in calculate(principal, rate):
        tree.insert(
            "", "end",
            values=(f"{years} 年", f"{compound:.2f}", f"{simple:.2f}", f"{diff:.2f}"),
        )

    # 更新曲线图
    plot_curves(fig, ax, canvas, principal, rate)


# ---------- 界面美化与布局 ----------
def setup_style():
    """统一 ttk 样式与字体（浅色清爽风格）"""
    style = ttk.Style()
    style.theme_use("clam")  # 跨平台、可控的简洁主题
    BG = "#ffffff"  # 统一白色背景，消除控件灰块
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG)
    # 标题 / 副标题 / 字段标签（背景与窗口一致，无灰底）
    style.configure("Title.TLabel", font=(UI_FONT, 18, "bold"), foreground="#1f3a5f", background=BG)
    style.configure("Subtitle.TLabel", font=(UI_FONT, 11), foreground="#5a6b7b", background=BG)
    style.configure("Field.TLabel", font=(UI_FONT, 10), foreground="#333333", background=BG)
    # 输入框：白底、细边框
    style.configure(
        "TEntry",
        fieldbackground="white",
        background=BG,
        bordercolor="#cccccc",
        lightcolor="#cccccc",
        darkcolor="#cccccc",
        padding=6,
    )
    # 计算按钮：扁平、无立体边框
    style.configure(
        "Calc.TButton",
        font=(UI_FONT, 11, "bold"),
        foreground="white",
        background="#2d7ff9",
        borderwidth=0,
        focusthickness=0,
        padding=(22, 10),
    )
    style.map(
        "Calc.TButton",
        background=[("active", "#1f6feb"), ("pressed", "#1252a8")],
    )
    # 表格：行高、字体、白底
    style.configure(
        "Treeview",
        font=(UI_FONT, 10),
        rowheight=28,
        background="white",
        fieldbackground="white",
        borderwidth=0,
    )
    style.configure("Treeview.Heading", font=(UI_FONT, 10, "bold"), background="#f1f4f8", foreground="#1f3a5f")
    # 表格选中时用浅蓝高亮，避免深灰
    style.map("Treeview", background=[("selected", "#e6f0fa")], foreground=[("selected", "#1f3a5f")])
    return style


def center_window(root, width, height):
    """将窗口设置为指定大小并居中显示"""
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")


def build(root):
    """在给定 Tk 窗口上构建界面控件"""
    root.title("复利计算器")
    root.configure(bg="#ffffff")  # 窗口白色背景
    center_window(root, 820, 600)  # 压缩高度，适配普通屏幕完整显示
    root.configure(padx=24, pady=14)
    setup_style()

    # 两列等宽扩展，使表格与图表对齐
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # 顶部标题与副标题（直接显示在白色背景上，无灰块）
    ttk.Label(root, text="复利计算器", style="Title.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(0, 2)
    )
    ttk.Label(root, text="复利与单利收益对比", style="Subtitle.TLabel").grid(
        row=1, column=0, columnspan=2, pady=(0, 12)
    )

    # 输入区：本金、年利率同一行对齐，无灰底包围
    input_frame = ttk.Frame(root)
    input_frame.grid(row=2, column=0, columnspan=2, pady=4)
    ttk.Label(input_frame, text="初始本金：", style="Field.TLabel").grid(
        row=0, column=0, padx=4, pady=6, sticky="e"
    )
    entry_principal = ttk.Entry(input_frame, width=16)
    entry_principal.grid(row=0, column=1, padx=8, pady=6)
    ttk.Label(input_frame, text="年利率（%）：", style="Field.TLabel").grid(
        row=0, column=2, padx=4, pady=6, sticky="e"
    )
    entry_rate = ttk.Entry(input_frame, width=16)
    entry_rate.grid(row=0, column=3, padx=8, pady=6)

    # 计算按钮：扁平简洁
    ttk.Button(
        root,
        text="开始计算",
        style="Calc.TButton",
        command=lambda: on_calculate(entry_principal, entry_rate, tree, fig, ax, canvas),
    ).grid(row=3, column=0, columnspan=2, pady=(6, 8))

    # 结果表格：仅 3 行，减少多余空白
    columns = ("year", "compound", "simple", "diff")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=3)
    tree.heading("year", text="年份", anchor="center")
    tree.heading("compound", text="复利终值（元）", anchor="center")
    tree.heading("simple", text="单利终值（元）", anchor="center")
    tree.heading("diff", text="差额（元）", anchor="center")
    tree.column("year", anchor="center", width=90)
    tree.column("compound", anchor="center", width=150)
    tree.column("simple", anchor="center", width=150)
    tree.column("diff", anchor="center", width=130)
    tree.grid(row=4, column=0, columnspan=2, sticky="ew", padx=6, pady=(0, 8))

    # 曲线图：降低高度避免被裁切，sticky 与表格对齐
    fig = Figure(figsize=(7.2, 2.6), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, sticky="ew", padx=6, pady=2)

    # 输入框默认值，并启动即自动计算一次，避免空白表格与空白坐标轴
    entry_principal.insert(0, "10000")
    entry_rate.insert(0, "5")
    on_calculate(entry_principal, entry_rate, tree, fig, ax, canvas)
    return entry_principal, entry_rate, tree, fig, ax, canvas


def main():
    root = tk.Tk()
    build(root)
    root.mainloop()


if __name__ == "__main__":
    main()
