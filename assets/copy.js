
(function () {
  var btn = document.getElementById('copy');
  var sha = document.getElementById('sha');
  if (!btn || !sha) return;
  function select() {
    var range = document.createRange();
    range.selectNodeContents(sha);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    btn.textContent = '已选中，按 Ctrl+C 复制';
    setTimeout(function () { btn.textContent = '复制校验值'; }, 2600);
  }
  btn.addEventListener('click', function () {
    var text = sha.textContent.trim();
    try {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = '已复制';
        setTimeout(function () { btn.textContent = '复制校验值'; }, 1600);
      }, select);
    } catch (e) { select(); }
  });
})();
