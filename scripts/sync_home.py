#!/usr/bin/env python3
"""把首页（index.html）里写死的兜底版本号/安装包大小，同步成各产品 latest.json 里的最新值。

浏览器里首页会用 assets/latest.js 实时读取 latest.json，所以访客看到的总是最新的；
HTML 里写的数字只在脚本没运行时（无 JS、搜索引擎爬虫、请求失败）才显示，发版时用这个脚本刷新。

用法（在仓库根目录）：
    python3 scripts/sync_home.py          # 改写 index.html
    python3 scripts/sync_home.py --check  # 只检查；有过期数字就退出码 1，不改文件
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
MANIFESTS = {"bluewhale": ROOT / "bluewhale" / "latest.json", "radar": ROOT / "radar" / "latest.json"}

# 与 assets/latest.js 的格式保持一致：Math.round(n / 1048576) 是四舍五入（0.5 向上）
def fmt_meta(version: str, size: int) -> str:
    mb = math.floor(size / 1048576 + 0.5)
    return f"v{version} · 约 {mb} MB（{size:,} 字节）"

PATTERN = re.compile(r'(data-latest="(?P<name>\w+)" data-field="(?P<field>tag|meta)">)(?P<text>[^<]*)')


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    data = {}
    for name, path in MANIFESTS.items():
        m = json.loads(path.read_text(encoding="utf-8"))
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(m["version"])) or int(m["installer_size"]) <= 0:
            sys.exit(f"{path} 的 version 或 installer_size 不合法，已停止")
        data[name] = m

    html = HOME.read_text(encoding="utf-8")
    changes = []

    def repl(match):
        m = data.get(match["name"])
        if m is None:
            sys.exit(f"index.html 里有未知产品 data-latest=\"{match['name']}\"")
        new = f"v{m['version']}" if match["field"] == "tag" else fmt_meta(m["version"], int(m["installer_size"]))
        if new != match["text"]:
            changes.append((match["name"], match["field"], match["text"], new))
        return match[1] + new

    new_html = PATTERN.sub(repl, html)
    if not PATTERN.search(html):
        sys.exit("index.html 里没找到 data-latest 元素，脚本需要更新")

    if not changes:
        print("首页兜底数字已是最新，无需改动。")
        return 0
    for name, field, old, new in changes:
        print(f"[{name}/{field}] {old}  ->  {new}")
    if check_only:
        print("首页兜底数字已过期。运行 python3 scripts/sync_home.py 同步。")
        return 1
    HOME.write_text(new_html, encoding="utf-8")
    print("已更新 index.html，记得提交。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
