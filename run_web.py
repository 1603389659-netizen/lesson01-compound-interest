# -*- coding: utf-8 -*-
"""
复利计算器（网页版）启动器
运行本文件后会自动在浏览器中打开计算器页面：
  - 页面就在普通浏览器标签页里，可以自己切换、最小化、关闭、重新打开
  - 关闭标签页不影响数据；想彻底停止服务，回到此窗口按 Ctrl + C 即可
仅使用 Python 标准库，无需安装任何第三方包。
"""
import functools
import http.server
import os
import socketserver
import webbrowser

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PAGE = "compound_interest_web.html"

# 防止端口被上次的进程短暂占用导致启动失败
socketserver.TCPServer.allow_reuse_address = True

Handler = functools.partial(
    http.server.SimpleHTTPRequestHandler, directory=DIRECTORY
)


def main():
    url = f"http://127.0.0.1:{PORT}/{PAGE}"
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print("=" * 52)
        print("  复利计算器（网页版）已启动")
        print(f"  地址：{url}")
        print("  浏览器应已自动打开；如未打开，可手动复制上面的地址")
        print("  停止服务：按 Ctrl + C")
        print("=" * 52)
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止，再见！")


if __name__ == "__main__":
    main()
