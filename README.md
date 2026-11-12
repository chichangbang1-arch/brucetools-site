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
