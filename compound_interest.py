# 交互版复利计算器（含复利与单利对比）
# 复利公式：本金 × (1 + 年利率) ^ 年数，每年利息滚入下一年的本金
# 单利公式：本金 × (1 + 年利率 × 年数)，每年利息只按最初本金计算

principal = float(input("请输入本金（元）："))               # 本金 P，用户输入
rate = float(input("请输入年利率（如 5 表示 5%）：")) / 100   # 年利率，百分数转小数：5 → 0.05

# 输入检查：本金必须大于 0，年利率不能为负数
if principal <= 0:
    print("本金必须大于 0")       # 本金不合法，提示后不计算
elif rate < 0:
    print("年利率不能为负数")     # 负利率不合法，提示后不计算
else:
    # 表头：分别列出年数、复利终值、单利终值、差额
    print(f"{'年数':<6}{'复利终值（元）':<18}{'单利终值（元）':<18}{'差额（元）'}")
    # 分别计算 10、20、30 年的结果
    for years in (10, 20, 30):
        compound = principal * (1 + rate) ** years   # 复利终值：利息滚存
        simple = principal * (1 + rate * years)      # 单利终值：利息不滚存
        diff = compound - simple                     # 差额：复利比单利多出的收益
        print(f"{years:<10}{compound:<20.2f}{simple:<20.2f}{diff:.2f}")
