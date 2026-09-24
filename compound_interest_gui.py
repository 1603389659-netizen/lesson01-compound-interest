# 复利计算器（Tkinter 基础图形界面）
# 复利公式：本金 × (1 + 年利率) ^ 年数

import tkinter as tk


def calculate(principal, rate):
    """计算 10、20、30 年的复利终值，返回 [(年数, 终值), ...]"""
    results = []
    for years in (10, 20, 30):
        amount = principal * (1 + rate) ** years  # 复利终值
        results.append((years, amount))
    return results


def on_calculate(entry_principal, entry_rate, result_label):
    """点击"计算"按钮时触发：读取输入、校验、显示结果"""
    try:
        principal = float(entry_principal.get())            # 读取本金
        rate = float(entry_rate.get()) / 100                # 百分数转小数：5 → 0.05
    except ValueError:
        result_label.config(text="请输入有效数字")           # 输入非数字时提示
        return

    # 输入校验：本金必须大于 0，年利率不能为负数
    if principal <= 0:
        result_label.config(text="本金必须大于 0")
        return
    if rate < 0:
        result_label.config(text="年利率不能为负数")
        return

    # 计算并展示 10/20/30 年复利终值
    results = calculate(principal, rate)
    text = "\n".join(f"{y} 年复利终值：{a:.2f} 元" for y, a in results)
    result_label.config(text=text)


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
        command=lambda: on_calculate(entry_principal, entry_rate, result_label),
    ).grid(row=2, column=0, columnspan=2, pady=10)

    # 结果显示区域
    result_label = tk.Label(root, text="")
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def main():
    root = tk.Tk()
    build(root)
    root.mainloop()


if __name__ == "__main__":
    main()
