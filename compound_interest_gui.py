# 复利计算器（Tkinter 图形界面，含复利与单利对比表格）
# 复利公式：本金 × (1 + 年利率) ^ 年数
# 单利公式：本金 × (1 + 年利率 × 年数)

import tkinter as tk
from tkinter import ttk


def calculate(principal, rate):
    """计算 10、20、30 年的复利终值、单利终值及差额，返回 [(年数, 复利, 单利, 差额), ...]"""
    results = []
    for years in (10, 20, 30):
        compound = principal * (1 + rate) ** years   # 复利终值：利息滚存
        simple = principal * (1 + rate * years)      # 单利终值：利息不滚存
        diff = compound - simple                      # 差额：复利比单利多出的收益
        results.append((years, compound, simple, diff))
    return results


def clear_tree(tree):
    """清空表格中的所有行"""
    for item in tree.get_children():
        tree.delete(item)


def on_calculate(entry_principal, entry_rate, tree):
    """点击"计算"按钮时触发：读取输入、校验、在表格中显示结果"""
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

    # 计算并逐行填入表格
    clear_tree(tree)
    for years, compound, simple, diff in calculate(principal, rate):
        tree.insert(
            "", "end",
            values=(f"{years} 年", f"{compound:.2f}", f"{simple:.2f}", f"{diff:.2f}"),
        )


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
        command=lambda: on_calculate(entry_principal, entry_rate, tree),
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


def main():
    root = tk.Tk()
    build(root)
    root.mainloop()


if __name__ == "__main__":
    main()
