# 复利计算器：输入本金、年利率、年限，计算最终本息和
# 复利公式：最终金额 = 本金 × (1 + 年利率 / 每年复利次数) ^ (每年复利次数 × 年数)

principal = float(input("请输入本金（元）："))        # 本金 P
rate = float(input("请输入年利率（如 5 表示 5%）：")) / 100  # 年利率，输入 5 表示 5%，转成 0.05
years = float(input("请输入存款年限（年）："))          # 年数 t
n = int(input("请输入每年复利次数（每年 1 次填 1）："))  # 每年复利次数 n

# 复利计算
final_amount = principal * (1 + rate / n) ** (n * years)

# 输出结果，保留两位小数
print(f"最终本息和：{final_amount:.2f} 元")
