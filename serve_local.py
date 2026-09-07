#!/usr/bin/env python3
"""ICT DOJO 本地模式启动器（OpenWorker AI 底座）

一键完成两件事：
1. 读取本地 openworker-server 的 sidecar 令牌并注入 index.html
2. 在 http://localhost:8080 提供静态服务（浏览器跨源要求：必须从 localhost 打开）

用法：
    python serve_local.py            # 默认端口 8765 的 token，服务 8080
    python serve_local.py 8081 8766  # 自定义 页面端口 / OpenWorker端口

前置：先启动 openworker-server（默认端口 8765），令牌位于
    Windows:  %APPDATA%\\coworker\\sidecar-8765.token
    macOS/Linux: ~/.config/coworker/sidecar-8765.token
"""

import os
import re
import sys
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent.resolve()


def read_sidecar_token(ow_port: int) -> str:
    env_token = os.environ.get("COWORKER_API_TOKEN", "").strip()
    if env_token:
        return env_token
    state = os.environ.get("COWORKER_STATE_DIR")
    if state:
        p = Path(state) / f"sidecar-{ow_port}.token"
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        p = Path(appdata) / "coworker" / f"sidecar-{ow_port}.token" if appdata else None
    else:
        p = Path.home() / ".config" / "coworker" / f"sidecar-{ow_port}.token"
    if p and p.is_file():
        return p.read_text(encoding="utf-8").strip()
    return ""


class Handler(SimpleHTTPRequestHandler):
    injected_token = ""
    ow_port = 8765

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (ROOT / "index.html").read_text(encoding="utf-8")
            token = self.injected_token or read_sidecar_token(self.ow_port)
            if token:
                html = html.replace(
                    "const OW_INJECTED_TOKEN='';",
                    f"const OW_INJECTED_TOKEN={token!r};",
                    1,
                )
            ow_url = f"http://127.0.0.1:{self.ow_port}"
            html = html.replace(
                "const OW_INJECTED_URL='';",
                f"const OW_INJECTED_URL={ow_url!r};",
                1,
            )
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    page_port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    ow_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    Handler.ow_port = ow_port

    token = read_sidecar_token(ow_port)
    url = f"http://localhost:{page_port}/"

    print("=" * 56)
    print("ICT DOJO 本地模式 · OpenWorker AI 底座")
    print("=" * 56)
    print(f"页面地址   : {url}")
    print(f"OpenWorker : http://127.0.0.1:{ow_port}")
    if token:
        print(f"令牌注入   : 已读取 sidecar-{ow_port}.token 并注入页面")
    else:
        print(f"令牌注入   : 未找到 sidecar-{ow_port}.token（先启动 openworker-server）")
        print("              启动后刷新本页即可；也可在页面内手动粘贴令牌。")
    print("停止服务   : Ctrl+C")
    print("=" * 56)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    server = ThreadingHTTPServer(("127.0.0.1", page_port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
