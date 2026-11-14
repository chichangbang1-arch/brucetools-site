# brucetools-site

brucetools.com 的静态站点源码。

- `index.html` — 首页
- `bluewhale/index.html` — 蓝鲸视频下载器下载页
- `assets/` — 样式、脚本、图片
- `_headers` — Cloudflare Pages 响应头配置

改完推到 main，Cloudflare Pages 会自动部署。

## 品牌与交互

- `assets/logo-mark.png`：导航/页脚的 BT 品牌标；配套 ICO/PNG/apple-touch-icon 用于浏览器图标。旧 SVG 已移入 `_local_qa/`，蓝鲸产品图标不变。
- `assets/brand.css` / `assets/motion.js`：两页共用，自包含；仅精细指针启用跟随高光和轻倾斜，系统减少动态效果时关闭。
- `_local_qa/home-desktop.png` 为本地审阅截图，未被页面引用；`_local_qa/check.py` 为隔离浏览器检查脚本。

- `assets/logo-tools-lockup.webp`：仅用于首页大尺寸品牌收尾区，懒加载；`assets/og-card.jpg` 用于两页分享卡片。提供的图片字节保持不变。
- 静态网格、径向辉光、渐变描边不依赖鼠标；环境呼吸及指针动效在减少动态效果模式下禁用。

- 本轮审阅截图：`_local_qa/home-desktop.png`（桌面全页）、`_local_qa/home-mobile-390.png`（390px 手机全页）。

## 更新清单镜像

`bluewhale/latest.json` 是蓝鲸视频下载器更新清单的备用地址（GitHub 连不上时客户端会来这里取）。
每次发布新版，把发布包里的 `latest.json` 原样覆盖到这里。清单带签名，镜像无法伪造更新。

## 安装包下载（R2）

蓝鲸下载器的“下载 Windows 版”按钮走 `https://download.brucetools.com/<安装包文件名>`（Cloudflare R2 存储桶 `brucetools-downloads`），
GitHub 发行页作为备用下载。每次发新版：安装包上传到 GitHub Release，同时上传到这个存储桶，再改下载页链接。

## 发版检查清单（蓝鲸 / 雷达每次发新版都要做）

1. 覆盖对应的 `latest.json`（`bluewhale/latest.json` 或 `radar/latest.json`）。
2. 改下载页（`bluewhale/index.html` 或 `radar/index.html`）里的版本号、安装包链接、SHA-256、大小。
3. **同步首页兜底数字**：在仓库根目录运行 `python3 scripts/sync_home.py`，然后提交 `index.html`。
   首页在浏览器里会自己读 `latest.json`，访客看到的总是新版本；但 HTML 里写死的数字
   （无脚本、搜索引擎爬虫、请求失败时显示）不会自己变，漏了这步就会和下载页对不上。
   只想检查不想改：`python3 scripts/sync_home.py --check`，有过期数字时退出码为 1。
4. 推送 main 前再跑一次 `--check`，确认输出“已是最新”。
