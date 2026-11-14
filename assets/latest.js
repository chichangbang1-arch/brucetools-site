/* 首页版本号 / 安装包大小：以各产品的 latest.json 为准。
   HTML 里写着的数字只是兜底（无脚本、爬虫、请求失败时显示）。
   发新版时只要覆盖 bluewhale/latest.json、radar/latest.json，首页会自动跟上。 */
(function () {
  var SOURCES = { bluewhale: "/bluewhale/latest.json", radar: "/radar/latest.json" };

  function fmtBytes(n) {
    return Math.round(n / 1048576) + " MB（" + n.toLocaleString("en-US") + " 字节）";
  }

  function apply(name, data) {
    if (!data || !/^\d+\.\d+\.\d+$/.test(String(data.version))) return;
    var size = Number(data.installer_size);
    var nodes = document.querySelectorAll('[data-latest="' + name + '"]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.getAttribute("data-field") === "tag") {
        el.textContent = "v" + data.version;
      } else if (el.getAttribute("data-field") === "meta" && size > 0) {
        el.textContent = "v" + data.version + " · 约 " + fmtBytes(size);
      }
    }
  }

  Object.keys(SOURCES).forEach(function (name) {
    if (!document.querySelector('[data-latest="' + name + '"]')) return;
    fetch(SOURCES[name], { cache: "no-cache" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { apply(name, data); })
      .catch(function () { /* 保留 HTML 里的兜底数字 */ });
  });
})();
