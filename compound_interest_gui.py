# -*- coding: utf-8 -*-
"""
复利计算器 —— macOS 风格 GUI（复刻设计稿）
功能：本金 + 每期追加投入的复利计算，逐年增长曲线，深 / 浅色主题切换
仅使用 Python 标准库 tkinter，无第三方依赖
"""
import tkinter as tk
from tkinter import font as tkfont
from ctypes import windll, c_int, byref, sizeof, Structure

# ==================== 主题配色 ====================
THEMES = {
    "light": {
        "bg": "#f5f5f7", "card": "#ffffff", "ink": "#1d1d1f", "sub": "#86868b",
        "faint": "#aeaeb2", "line": "#e8e8ed", "entry_bg": "#fafafc",
        "entry_border": "#dcdce1", "blue": "#0a7cff", "blue_btn": "#0a7cff",
        "green": "#1f9d55", "orange": "#c26a1f", "area": "#dcebfb",
        "grid": "#ececf1", "track": "#e9e9ee", "seg_on": "#0a7cff",
    },
    "dark": {
        "bg": "#1c1c1e", "card": "#2c2c2e", "ink": "#f5f5f7", "sub": "#98989f",
        "faint": "#6c6c70", "line": "#3a3a3c", "entry_bg": "#3a3a3c",
        "entry_border": "#48484a", "blue": "#409cff", "blue_btn": "#0a84ff",
        "green": "#30d158", "orange": "#ff9f0a", "area": "#1e3a5f",
        "grid": "#3a3a3c", "track": "#48484a", "seg_on": "#0a84ff",
    },
}
theme_name = "light"
C = THEMES[theme_name]

# ==================== 创建无边框主窗口 ====================
root = tk.Tk()
root.overrideredirect(True)
root.configure(bg=C["bg"])

WIN_W, WIN_H = 1124, 740
root.update_idletasks()
x = (root.winfo_screenwidth() - WIN_W) // 2
y = (root.winfo_screenheight() - WIN_H) // 4
root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

# Win11 窗口圆角
try:
    hwnd0 = root.winfo_id()
    pref = c_int(2)
    windll.dwmapi.DwmSetWindowAttribute(hwnd0, 33, byref(pref), sizeof(pref))

    class MARGINS(Structure):
        _fields_ = [("left", c_int), ("right", c_int),
                    ("top", c_int), ("bottom", c_int)]
    windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd0, byref(MARGINS(0, 0, 0, 1)))
except Exception:
    pass

# 启动时短暂置顶，保证窗口可见
def bring_to_front():
    try:
        h = root.winfo_id()
        windll.user32.SetWindowPos(h, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        windll.user32.SetForegroundWindow(h)
        root.after(3000, lambda: windll.user32.SetWindowPos(h, -2, 0, 0, 0, 0, 0x0001 | 0x0002))
    except Exception:
        pass
root.after(200, bring_to_front)

# ==================== 字体 ====================
_fams = tkfont.families(root)
FAM = "Microsoft YaHei UI" if "Microsoft YaHei UI" in _fams else "Microsoft YaHei"
f_title   = tkfont.Font(family=FAM, size=24, weight="bold")
f_en      = tkfont.Font(family="Segoe UI", size=11)
f_bar     = tkfont.Font(family=FAM, size=13, weight="bold")
f_label   = tkfont.Font(family=FAM, size=12, weight="bold")
f_entry   = tkfont.Font(family="Segoe UI", size=14)
f_btn     = tkfont.Font(family=FAM, size=15, weight="bold")
f_hero    = tkfont.Font(family="Segoe UI", size=33, weight="bold")
f_mid     = tkfont.Font(family=FAM, size=12)
f_stat_n  = tkfont.Font(family="Segoe UI", size=17, weight="bold")
f_chart_t = tkfont.Font(family=FAM, size=14, weight="bold")
f_legend  = tkfont.Font(family=FAM, size=12)
f_tick    = tkfont.Font(family="Segoe UI", size=11)
f_note    = tkfont.Font(family=FAM, size=10)

# ==================== 工具函数 ====================
def round_rect(cv, x1, y1, x2, y2, r=14, **kw):
    """Canvas 平滑圆角矩形"""
    p = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
         x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
         x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    return cv.create_polygon(p, smooth=True, **kw)

def money(v):
    return f"{v:,.2f}"

def nice_step(raw):
    """把任意步长取整为 1 / 2 / 5 × 10^k 的「漂亮步长」"""
    import math
    if raw <= 0:
        return 1
    base = 10 ** math.floor(math.log10(raw))
    for mul in (1, 2, 5, 10):
        if base * mul >= raw:
            return base * mul
    return base * 10

# ==================== 自定义标题栏 ====================
bar = tk.Frame(root, bg=C["bg"], height=48)
bar.pack(fill="x")
bar.pack_propagate(False)

for i, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    d = tk.Canvas(bar, width=14, height=14, bg=C["bg"], highlightthickness=0)
    d.place(x=18 + i * 22, y=17)
    d.create_oval(1, 1, 13, 13, fill=color, outline="")
    if i == 0:
        d.bind("<Button-1>", lambda e: root.destroy())
        d.configure(cursor="hand2")

bar_title = tk.Label(bar, text="复利计算器", bg=C["bg"], fg=C["ink"], font=f_bar)
bar_title.place(relx=0.5, rely=0.5, anchor="center")

# 拖动窗口
_drag = {"x": 0, "y": 0}
def _start(e):
    _drag.update(x=e.x_root - root.winfo_x(), y=e.y_root - root.winfo_y())
def _move(e):
    root.geometry(f"+{e.x_root - _drag['x']}+{e.y_root - _drag['y']}")
for w in (bar, bar_title):
    w.bind("<Button-1>", _start)
    w.bind("<B1-Motion>", _move)
root.bind("<Escape>", lambda e: root.destroy())

# ==================== 顶部标题行 ====================
header = tk.Frame(root, bg=C["bg"], height=86)
header.pack(fill="x")
header.pack_propagate(False)

title_box = tk.Frame(header, bg=C["bg"])
title_box.place(x=32, y=14)
label_title = tk.Label(title_box, text="💰 复利计算器", bg=C["bg"],
                       fg=C["ink"], font=f_title)
label_title.pack(anchor="w")
label_en = tk.Label(title_box, text="Compound Interest Calculator",
                    bg=C["bg"], fg=C["sub"], font=f_en)
label_en.pack(anchor="w", pady=(2, 0))

# 深 / 浅色分段切换
seg = tk.Canvas(header, width=150, height=38, bg=C["bg"], highlightthickness=0)
seg.place(relx=1.0, x=-32, y=20, anchor="ne")

# ==================== 主体两列布局 ====================
body = tk.Frame(root, bg=C["bg"])
body.pack(fill="both", expand=True, padx=28)
body.grid_columnconfigure(0, weight=0)
body.grid_columnconfigure(1, weight=1)
body.grid_rowconfigure(0, weight=0)
body.grid_rowconfigure(1, weight=1)

# ---------- 左侧：输入卡片 ----------
CARD_W = 505
card_in = tk.Canvas(body, width=CARD_W, height=302, bg=C["bg"],
                    highlightthickness=0)
card_in.grid(row=0, column=0, sticky="nw", padx=(0, 18), pady=(0, 16))

# 4 个输入框（父 widget 为 Canvas，圆角底色由 Canvas 绘制）
var_p   = tk.StringVar(value="10000")
var_r   = tk.StringVar(value="3")
var_n   = tk.StringVar(value="10")
var_add = tk.StringVar(value="500")
vars4 = [var_p, var_r, var_n, var_add]

entries = []
for v in vars4:
    e = tk.Entry(card_in, textvariable=v, font=f_entry, relief="flat",
                 bd=0, justify="left", insertwidth=1)
    entries.append(e)
    v.trace_add("write", lambda *a: compute())

# 两个按钮（自绘圆角 Canvas，挂载在输入卡片内）
btn_calc = tk.Canvas(body, width=236, height=50, bg=C["bg"],
                     highlightthickness=0, cursor="hand2")
btn_reset = tk.Canvas(body, width=236, height=50, bg=C["bg"],
                      highlightthickness=0, cursor="hand2")

# ---------- 左侧：结果卡片 ----------
card_res = tk.Canvas(body, width=CARD_W, height=238, bg=C["bg"],
                     highlightthickness=0)
card_res.grid(row=1, column=0, sticky="nw", padx=(0, 18))

# ---------- 右侧：图表卡片 ----------
card_chart = tk.Canvas(body, width=545, height=556, bg=C["bg"],
                       highlightthickness=0)
card_chart.grid(row=0, column=1, rowspan=2, sticky="nw")

# 底部说明
footer = tk.Label(root, text="追加投入按每期期末计入 · 输入即自动计算",
                  bg=C["bg"], fg=C["faint"], font=f_note)
footer.place(relx=0.5, rely=1.0, y=-14, anchor="center")

# ==================== 计算逻辑 ====================
def calc_series(p, r, n, add):
    """逐年递推：余额先按利率增值，期末再计入追加投入"""
    totals, principals = [p], [p]
    bal = p
    for _ in range(n):
        bal = bal * (1 + r) + add
        totals.append(bal)
        principals.append(principals[-1] + add)
    return totals, principals

def read_inputs():
    def num(v):
        try:
            return float(v)
        except ValueError:
            return 0.0
    p = max(num(var_p.get()), 0.0)
    r = num(var_r.get()) / 100.0
    n = int(max(num(var_n.get()), 0.0))
    n = max(0, min(n, 500))           # 防止异常输入卡死界面
    add = max(num(var_add.get()), 0.0)
    return p, r, n, add

# ==================== 绘制：输入卡片 ====================
def draw_input_card():
    cv = card_in
    cv.delete("all")
    cv.configure(bg=C["bg"])
    round_rect(cv, 0, 0, CARD_W, 302, r=18, fill=C["card"], outline="")

    labels = ["初始本金（元）", "每期利率（%）", "周期数量（期）", "每期追加投入（元）"]
    positions = [(26, 24), (268, 24), (26, 132), (268, 132)]  # 标签 x,y
    entry_xy = [(26, 56), (268, 56), (26, 164), (268, 164)]   # 输入框 x,y

    for (lx, ly), (ex, ey), e, lab in zip(positions, entry_xy, entries, labels):
        cv.create_text(lx, ly, text=lab, anchor="nw", fill=C["ink"], font=f_label)
        # 输入框圆角底
        round_rect(cv, ex, ey, ex + 211, ey + 44, r=10,
                   fill=C["entry_bg"], outline=C["entry_border"])
        e.configure(bg=C["entry_bg"], fg=C["ink"],
                    insertbackground=C["ink"], highlightthickness=0)
        cv.create_window(ex + 14, ey + 22, window=e, anchor="w",
                         width=185, height=30)

    # 按钮
    cv.create_window(26, 234, window=btn_calc, anchor="nw", width=236, height=50)
    cv.create_window(243, 234, window=btn_reset, anchor="nw", width=236, height=50)
    draw_buttons()

def draw_buttons(hover_calc=False, hover_reset=False):
    # 计算按钮
    btn_calc.delete("all")
    btn_calc.configure(bg=C["card"], highlightthickness=0)
    calc_color = "#3a93ff" if hover_calc else C["blue_btn"]
    round_rect(btn_calc, 0, 0, 236, 50, r=12, fill=calc_color, outline="")
    btn_calc.create_text(118, 25, text="计 算", fill="#ffffff", font=f_btn)

    # 重置按钮
    btn_reset.delete("all")
    btn_reset.configure(bg=C["card"], highlightthickness=0)
    reset_edge = C["ink"] if hover_reset else C["entry_border"]
    reset_fg = C["ink"] if hover_reset else C["sub"]
    round_rect(btn_reset, 0, 0, 236, 50, r=12,
               fill=C["card"], outline=reset_edge, width=1)
    btn_reset.create_text(118, 25, text="重 置", fill=reset_fg, font=f_btn)

btn_calc.bind("<Enter>", lambda e: draw_buttons(hover_calc=True))
btn_calc.bind("<Leave>", lambda e: draw_buttons())
btn_reset.bind("<Enter>", lambda e: draw_buttons(hover_reset=True))
btn_reset.bind("<Leave>", lambda e: draw_buttons())
btn_calc.bind("<Button-1>", lambda e: compute())
btn_reset.bind("<Button-1>", lambda e: reset_defaults())

# ==================== 绘制：结果卡片 ====================
def draw_result_card(total, interest, principal_sum, multiple):
    cv = card_res
    cv.delete("all")
    cv.configure(bg=C["bg"])
    round_rect(cv, 0, 0, CARD_W, 238, r=18, fill=C["card"], outline="")

    cv.create_text(26, 26, text="到期总额（连本带利）", anchor="nw",
                   fill=C["sub"], font=f_mid)
    cv.create_text(26, 58, text=f"￥ {money(total)}", anchor="nw",
                   fill=C["blue"], font=f_hero)
    cv.create_line(26, 128, CARD_W - 26, 128, fill=C["line"])

    stats = [
        ("总利息", f"￥ {money(interest)}", C["green"]),
        ("本金合计", f"￥ {money(principal_sum)}", C["orange"]),
        ("收益倍数", f"{multiple:.2f} ×", C["blue"]),
    ]
    for i, (lab, val, color) in enumerate(stats):
        cx = 26 + i * 158
        cv.create_text(cx, 150, text=lab, anchor="nw", fill=C["sub"], font=f_mid)
        cv.create_text(cx, 182, text=val, anchor="nw", fill=color, font=f_stat_n)

# ==================== 绘制：增长曲线 ====================
def draw_chart(totals, principals):
    cv = card_chart
    cv.delete("all")
    cv.configure(bg=C["bg"])
    W, H = 545, 556
    round_rect(cv, 0, 0, W, H, r=18, fill=C["card"], outline="")

    # 标题行
    cv.create_text(26, 26, text="📈 增长曲线", anchor="nw",
                   fill=C["ink"], font=f_chart_t)
    cv.create_text(W - 26, 30, text="蓝色为复利总值 · 虚线为本金合计",
                   anchor="ne", fill=C["sub"], font=f_note)

    # 图例
    cv.create_line(120, 74, 152, 74, fill=C["blue"], width=3)
    cv.create_text(160, 74, text="复利总值", anchor="w", fill=C["ink"], font=f_legend)
    cv.create_line(280, 74, 312, 74, fill=C["orange"], width=2, dash=(6, 4))
    cv.create_text(320, 74, text="本金合计", anchor="w", fill=C["ink"], font=f_legend)

    # 绘图区
    px1, px2, py1, py2 = 78, W - 40, 100, H - 70
    n = len(totals) - 1
    y_lo = min(min(totals), min(principals))          # 坐标下界（初始本金）
    y_hi_raw = max(max(totals), max(principals))     # 数据最高点
    if y_hi_raw <= y_lo:
        y_hi_raw = y_lo + 1

    # 漂亮步长：默认参数下为 2000，网格线即 1.0万 / 1.2万 / … / 1.8万
    step = nice_step((y_hi_raw - y_lo) / 5)
    ticks = []
    v = y_lo
    while v <= y_hi_raw + 1e-9:
        ticks.append(v)
        v += step
    if len(ticks) < 2:
        ticks.append(y_lo + step)
    y_max = max(ticks[-1] + step * 0.7, y_hi_raw * 1.02)
    y_min = y_lo

    def X(i):
        return px1 + (px2 - px1) * i / n if n else px1
    def Y(v):
        return py2 - (py2 - py1) * (v - y_min) / (y_max - y_min)

    # 横向网格线 + Y 轴标签（单位：万）
    for val in ticks:
        gy = Y(val)
        cv.create_line(px1, gy, px2, gy, fill=C["grid"])
        cv.create_text(px1 - 12, gy, text=f"{val/10000:.1f}万",
                       anchor="e", fill=C["sub"], font=f_tick)

    # X 轴刻度
    xstep = max(1, (n // 5) or 1)
    xticks = list(range(0, n + 1, xstep))
    if xticks[-1] != n:
        xticks.append(n)
    for i in xticks:
        cv.create_text(X(i), py2 + 14, text=str(i), anchor="n",
                       fill=C["sub"], font=f_tick)
    cv.create_text((px1 + px2) / 2, py2 + 42, text="期数",
                   fill=C["sub"], font=f_legend)

    # 面积填充（复利总值曲线下方）
    area_pts = [X(0), Y(totals[0])]
    for i in range(1, n + 1):
        area_pts += [X(i), Y(totals[i])]
    area_pts += [X(n), py2, X(0), py2]
    cv.create_polygon(area_pts, fill=C["area"], outline="")

    # 本金合计虚线
    pts_p = []
    for i in range(n + 1):
        pts_p += [X(i), Y(principals[i])]
    cv.create_line(pts_p, fill=C["orange"], width=2, dash=(6, 4),
                   capstyle="round")

    # 复利总值蓝色折线
    pts_t = []
    for i in range(n + 1):
        pts_t += [X(i), Y(totals[i])]
    cv.create_line(pts_t, fill=C["blue"], width=3, capstyle="round",
                   joinstyle="round")

# ==================== 主题切换分段控件 ====================
def draw_seg():
    seg.delete("all")
    seg.configure(bg=C["bg"])
    # 整体胶囊底
    round_rect(seg, 0, 0, 150, 38, r=10, fill=C["track"], outline="")
    if theme_name == "dark":
        round_rect(seg, 2, 2, 74, 36, r=9, fill=C["seg_on"], outline="")
        seg.create_text(38, 19, text="🌙 深色", fill="#ffffff", font=f_legend)
        seg.create_text(112, 19, text="☀️ 浅色", fill=C["sub"], font=f_legend)
    else:
        round_rect(seg, 76, 2, 148, 36, r=9, fill=C["seg_on"], outline="")
        seg.create_text(38, 19, text="🌙 深色", fill=C["sub"], font=f_legend)
        seg.create_text(112, 19, text="☀️ 浅色", fill="#ffffff", font=f_legend)

def toggle_theme(event=None):
    global theme_name, C
    theme_name = "dark" if theme_name == "light" else "light"
    C = THEMES[theme_name]
    apply_theme()

seg.bind("<Button-1>", toggle_theme)
seg.configure(cursor="hand2")

def apply_theme():
    root.configure(bg=C["bg"])
    bar.configure(bg=C["bg"])
    header.configure(bg=C["bg"])
    body.configure(bg=C["bg"])
    title_box.configure(bg=C["bg"])
    # 标题行两个 Label 重新着色
    label_title.configure(bg=C["bg"], fg=C["ink"])
    label_en.configure(bg=C["bg"], fg=C["sub"])
    bar_title.configure(bg=C["bg"], fg=C["ink"])
    footer.configure(bg=C["bg"], fg=C["faint"])
    for d in bar.winfo_children():
        if isinstance(d, tk.Canvas):
            d.configure(bg=C["bg"])
    draw_seg()
    draw_input_card()
    compute()

# ==================== 计算 / 重置入口 ====================
def compute():
    p, r, n, add = read_inputs()
    totals, principals = calc_series(p, r, n, add)
    total = totals[-1]
    principal_sum = principals[-1]
    interest = total - principal_sum
    multiple = total / principal_sum if principal_sum > 0 else 0
    draw_result_card(total, interest, principal_sum, multiple)
    draw_chart(totals, principals)

def reset_defaults():
    var_p.set("10000")
    var_r.set("3")
    var_n.set("10")
    var_add.set("500")
    compute()

# ==================== 首次渲染 ====================
draw_seg()
draw_input_card()
compute()

root.mainloop()
