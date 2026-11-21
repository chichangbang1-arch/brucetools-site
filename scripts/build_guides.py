#!/usr/bin/env python3
"""生成 /guide/ 下的教程页（给搜索引擎收录用）。

用法：在仓库根目录运行  python3 scripts/build_guides.py
新增一个平台：在 GUIDES 里加一项，重新运行，再把新地址加进 sitemap.xml。
页面只写已经验证过的事实；版本号不写进教程页，统一指向 /bluewhale/ 下载页。
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://brucetools.com"

ICON_DL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/></svg>')
ICON = {
    "list": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/></svg>',
    "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg>',
    "faq": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.3 9.3a2.8 2.8 0 0 1 5.4.9c0 1.9-2.7 2.3-2.7 4"/><path d="M12 17.5h.01"/></svg>',
    "link": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
}

RIGHTS = ("请只下载你自己有权保存的内容，用于个人学习或备份。软件不会破解付费内容，也不会绕过平台的访问限制；"
          "下载他人作品再传播可能侵犯著作权，请自行判断并承担责任。")

GUIDES = [
    {
        "slug": "shipinhao",
        "name": "视频号",
        "title": "视频号视频怎么下载到电脑？2026 实测方法与步骤",
        "h1": "视频号视频怎么下载到电脑",
        "desc": "微信视频号官方没有下载按钮。这里整理了把视频号视频保存到电脑的几种办法，以及用免费的蓝鲸视频下载器（Windows / Mac）粘贴链接下载的具体步骤和常见问题。",
        "lede": "微信视频号官方没有“下载”按钮：手机上只能收藏和转发，电脑上的视频号助手是用来发视频的。想把视频存进电脑，需要借助工具。下面先说有哪些办法，再给出最省事的一种的具体步骤。",
        "ways_sub": "按上手难度从低到高",
        "ways": [
            ("蓝鲸视频下载器（图形界面）", "免费的电脑软件，在软件里登录一次视频号，之后粘贴链接就能下载，有下载列表和失败重试。支持 Windows 10 / 11 和 Mac（Intel 芯片）。"),
            ("抓包类工具", "原理是拦截微信的网络请求，通常要装证书、配代理，步骤多，对新手不太友好。"),
            ("手机录屏", "不用装软件，但画质和声音都会打折扣，长视频也不方便。"),
        ],
        "steps": [
            ("安装蓝鲸", "到<a href=\"/bluewhale/\">蓝鲸下载页</a>下载安装包，页面上有 SHA-256 校验值可以核对。"),
            ("登录一次视频号", "打开软件，进入「平台授权」，点视频号。软件会打开一个独立的浏览器窗口，在里面完成登录。"),
            ("复制视频链接", "在微信里打开要保存的那条视频号视频，从分享菜单里选「复制链接」。不同微信版本里这个按钮的位置可能略有不同。"),
            ("粘贴并下载", "回到蓝鲸，把链接粘贴进输入框，添加下载任务。进度在下载列表里看，下完的文件保存在你的电脑上。"),
        ],
        "faq": [
            ("要一直登录吗？登录过期了怎么办？", "登录一次后可以连续使用。过期后到「平台授权」重新登录视频号即可。"),
            ("下载失败怎么办？", "先在下载列表里点「重试」，很多时候重试就能成功。还不行就到「平台授权」重新登录视频号再试。另外不要同时打开两个蓝鲸，否则下载会失败。"),
            ("收费吗？", "当前版本免费使用，没有内购。"),
            ("Mac 能用吗？手机呢？", "Mac 可以，需要 macOS 13 及以上、Intel 芯片。手机暂不支持。"),
            ("会把我的登录信息传到别处吗？", "平台授权信息保存在你自己的电脑上，本站不要求你上传任何授权文件。"),
        ],
    },
    {
        "slug": "douyin",
        "name": "抖音",
        "title": "抖音视频怎么保存到电脑？2026 实测方法与步骤",
        "h1": "抖音视频怎么保存到电脑",
        "desc": "抖音电脑网页版没有下载按钮，手机保存还要再传到电脑。这里整理了把抖音视频保存到电脑的几种办法，以及用免费的蓝鲸视频下载器（Windows / Mac）粘贴链接下载的具体步骤和常见问题。",
        "lede": "抖音电脑网页版没有直接的下载按钮；手机 App 里如果作者开放了下载，可以“分享 → 保存本地”，但还要再从手机传到电脑。想在电脑上直接存，下面先说有哪些办法，再给出最省事的一种的具体步骤。",
        "ways_sub": "按上手难度从低到高",
        "ways": [
            ("蓝鲸视频下载器（图形界面）", "免费的电脑软件，在软件里授权一次抖音，之后粘贴链接就能下载，有下载列表和失败重试。支持 Windows 10 / 11 和 Mac（Intel 芯片）。"),
            ("手机保存后传到电脑", "作者开放下载时，在 App 里点“分享 → 保存本地”，再用数据线或微信传到电脑。要多转一道。"),
            ("yt-dlp（命令行）", "开源免费，支持的网站非常多，但需要敲命令，对新手有门槛。"),
        ],
        "steps": [
            ("安装蓝鲸", "到<a href=\"/bluewhale/\">蓝鲸下载页</a>下载安装包，页面上有 SHA-256 校验值可以核对。"),
            ("授权一次抖音", "打开软件，进入「平台授权」，点抖音。软件会打开一个独立的浏览器窗口，在里面完成登录。"),
            ("复制视频链接", "手机 App 里点“分享 → 复制链接”；电脑上用浏览器打开抖音网页版，直接复制这条视频的网址也可以。"),
            ("粘贴并下载", "回到蓝鲸，把链接粘贴进输入框，添加下载任务。进度在下载列表里看，下完的文件保存在你的电脑上。"),
        ],
        "faq": [
            ("从抖音搜索结果页复制的网址能用吗？", "可以，搜索结果里点开视频后复制到的网址也能识别。"),
            ("下载失败怎么办？", "先在下载列表里点「重试」。还不行就到「平台授权」重新登录抖音，并在浏览器里确认这条视频能正常播放，再回软件重试。"),
            ("能一次下很多条吗？", "可以把多条链接陆续添加进下载列表，软件会排队下载。"),
            ("收费吗？", "当前版本免费使用，没有内购。"),
            ("Mac 能用吗？手机呢？", "Mac 可以，需要 macOS 13 及以上、Intel 芯片。手机暂不支持。"),
        ],
    },
]

HEAD = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · BruceTools</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><link rel="icon" type="image/x-icon" sizes="16x16 32x32 48x48" href="/assets/favicon.ico"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"><link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png"><link rel="stylesheet" href="/assets/guide.css"><link rel="stylesheet" href="/assets/brand.css"><script src="/assets/motion.js" defer></script><script src="/assets/la.js" defer></script><meta property="og:type" content="article"><meta property="og:site_name" content="BruceTools"><meta property="og:locale" content="zh_CN"><meta property="og:url" content="{url}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://brucetools.com/assets/og-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">{ld}</head><body class="download-page"><a class="skip" href="#main">跳到主要内容</a>

<nav class="wrap" aria-label="主导航" style="padding-block:1rem;display:flex;flex-wrap:wrap;gap:1.5rem"><a class="wordmark brand-header" href="/" aria-label="BruceTools 首页"><img src="/assets/logo-header.webp" alt="BruceTools · brucetools.com" width="337" height="84"></a><a href="/guide/">教程</a><a href="/bluewhale/">下载蓝鲸</a></nav>"""

FOOT = """<footer>
  <div class="wrap">
    <a class="wordmark footer-brand" href="/" aria-label="BruceTools 首页"><span class="mark"><img src="/assets/logo-mark.png" alt="BruceTools BT 标志" width="36" height="36"></span>Bruce<span class="soft">Tools</span></a>
    <p><a href="/guide/">全部教程</a> · <a href="/bluewhale/">蓝鲸视频下载器</a> · <a href="/radar/">蓝鲸选题雷达</a></p>
    <p style="margin-top:.6rem">{rights}</p>
  </div>
</footer>
</body></html>
"""


def ld(*objs):
    return "".join('<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False) for o in objs)


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def panel(icon, h2, sub, body):
    return ('    <section class="panel">\n      <div class="phead">\n        <span class="picon">%s</span>\n'
            '        <div>\n          <h2>%s</h2>\n          <p>%s</p>\n        </div>\n      </div>\n%s\n    </section>\n'
            % (ICON[icon], h2, sub, body))


def build_guide(g):
    url = "%s/guide/%s/" % (SITE, g["slug"])
    schema = ld(
        {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "inLanguage": "zh-CN",
         "description": g["desc"],
         "step": [{"@type": "HowToStep", "name": n, "text": strip_tags(t)} for n, t in g["steps"]]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in g["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "BruceTools", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "教程", "item": SITE + "/guide/"},
            {"@type": "ListItem", "position": 3, "name": g["h1"], "item": url}]},
    )
    out = [HEAD.format(title=html.escape(g["title"]), desc=html.escape(g["desc"]), url=url, ld=schema)]
    out.append('<header class="hero">\n  <div class="wrap">\n'
               '    <p class="crumb"><a href="/">BruceTools</a> › <a href="/guide/">教程</a> › %s</p>\n'
               '    <h1>%s</h1>\n    <p class="lede">%s</p>\n'
               '    <div class="get">\n      <a class="btn" href="/bluewhale/">%s\n        免费下载蓝鲸视频下载器\n      </a>\n'
               '      <span class="alt">Windows 10 / 11 · Mac（Intel）· 免费</span>\n    </div>\n  </div>\n</header>\n'
               % (g["name"], g["h1"], g["lede"], ICON_DL))
    out.append('\n<main id="main">\n  <div class="wrap">\n\n')
    out.append(panel("list", "%s视频存到电脑的几种办法" % g["name"], g["ways_sub"],
                     '      <ul class="ways">\n%s\n      </ul>' % "\n".join(
                         "        <li><b>%s</b>：%s</li>" % w for w in g["ways"])))
    out.append("\n")
    out.append(panel("play", "用蓝鲸下载%s视频的步骤" % g["name"], "四步，第二步只需要做一次",
                     '      <ol class="steps">\n%s\n      </ol>' % "\n".join(
                         "        <li><b>%s</b><br>%s</li>" % s for s in g["steps"])))
    out.append("\n")
    out.append(panel("faq", "常见问题", "关于%s下载，问得最多的几个" % g["name"],
                     '      <ul class="faq">\n%s\n      </ul>' % "\n".join(
                         "        <li>\n          <h3>%s</h3>\n          <p>%s</p>\n        </li>" % f for f in g["faq"])))
    out.append("\n")
    others = " ".join('<a href="/guide/%s/">%s</a>' % (o["slug"], o["h1"]) for o in GUIDES if o is not g)
    out.append(panel("link", "其他平台", "蓝鲸还支持 B站、小红书、YouTube、TikTok、X",
                     '      <p class="more">%s <a href="/bluewhale/">查看全部支持的平台</a></p>' % others))
    out.append("\n  </div>\n</main>\n\n")
    out.append(FOOT.format(rights=RIGHTS))
    p = ROOT / "guide" / g["slug"] / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(out), encoding="utf-8")
    return url


def build_index():
    url = SITE + "/guide/"
    title = "视频下载教程：视频号、抖音视频怎么保存到电脑"
    desc = "BruceTools 教程合集：视频号视频怎么下载到电脑、抖音视频怎么保存到电脑等，按平台给出办法、步骤和常见问题。"
    schema = ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "inLanguage": "zh-CN",
                 "description": desc, "url": url})
    out = [HEAD.format(title=html.escape(title), desc=html.escape(desc), url=url, ld=schema)]
    out.append('<header class="hero">\n  <div class="wrap">\n'
               '    <p class="crumb"><a href="/">BruceTools</a> › 教程</p>\n'
               '    <h1>视频下载教程</h1>\n'
               '    <p class="lede">按平台整理：有哪些办法、具体怎么做、出问题怎么办。</p>\n  </div>\n</header>\n')
    out.append('\n<main id="main">\n  <div class="wrap">\n\n')
    rows = "\n".join('        <li><b><a href="/guide/%s/">%s</a></b><br>%s</li>' % (g["slug"], g["h1"], g["desc"])
                     for g in GUIDES)
    out.append(panel("list", "按平台查看", "更多平台的教程会陆续补上", '      <ul class="ways">\n%s\n      </ul>' % rows))
    out.append("\n  </div>\n</main>\n\n")
    out.append(FOOT.format(rights=RIGHTS))
    (ROOT / "guide").mkdir(exist_ok=True)
    (ROOT / "guide" / "index.html").write_text("".join(out), encoding="utf-8")
    return url


if __name__ == "__main__":
    print(build_index())
    for g in GUIDES:
        print(build_guide(g))
