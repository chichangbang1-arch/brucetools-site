/* 51.LA 访问统计（应用：Brucetools.com，统计 ID 3RpVutj4LBZ4Hr1V）。
   官方代码是一个外部脚本加一段内联 LA.init()；本站 CSP 不允许内联脚本，
   所以改成在这里加载 SDK、加载完成后再初始化。统计失败不影响页面。 */
(function () {
  var ID = "3RpVutj4LBZ4Hr1V";
  if (document.getElementById("LA_COLLECT")) return;
  var s = document.createElement("script");
  s.id = "LA_COLLECT";
  s.charset = "UTF-8";
  s.async = true;
  s.src = "https://sdk.51.la/js-sdk-pro.min.js";
  s.onload = function () {
    try { if (window.LA && LA.init) LA.init({ id: ID, ck: ID }); } catch (e) { /* 忽略 */ }
  };
  document.head.appendChild(s);
})();
