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
    """点击"计算"按钮时触发：读取输入、校验、更新表格与曲线图"""
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


def build(root):
    """在给定 Tk 窗口上构建界面控件"""
    root.title("复利计算器")  # 窗口标题

    # 初始本金输入框
    tk.Label(root, text="初始本金：").grid(row=0, column=0, padx=10, pady=10)
    entry_principal = tk.Entry(root)
    entry_principal.grid(row=0, column=1, padx=10, pady=10)

    # 年利率（%）输入框
    tk.Label(root, text="年利率（%）：").grid(row=1, column=0, padx=10, pady=10)
    entry_rate = tk.Entry(root)
    entry_rate.grid(row=1, column=1, padx=10, pady=10)

    # 计算按钮
    tk.Button(
        root,
        text="计算",
        command=lambda: on_calculate(entry_principal, entry_rate, tree, fig, ax, canvas),
    ).grid(row=2, column=0, columnspan=2, pady=10)

    # 结果表格：年份 / 复利终值 / 单利终值 / 差额
    columns = ("year", "compound", "simple", "diff")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=3)
    tree.heading("year", text="年份")
    tree.heading("compound", text="复利终值（元）")
    tree.heading("simple", text="单利终值（元）")
    tree.heading("diff", text="差额（元）")
    tree.column("year", anchor="center", width=80)
    tree.column("compound", anchor="e", width=140)
    tree.column("simple", anchor="e", width=140)
    tree.column("diff", anchor="e", width=120)
    tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # 曲线图：0~30 年复利与单利增长曲线
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def main():
    root = tk.Tk()
    build(root)
    root.mainloop()


if __name__ == "__main__":
    main()
