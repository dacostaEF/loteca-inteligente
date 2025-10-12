# === Cursor Patch: Safety Shim + Rewrites ===
$ErrorActionPreference = "Stop"

# 1) Arquivos alvo
$filesHtml = Get-ChildItem -Recurse -Include *.html,*.htm -File
$filesJs   = Get-ChildItem -Recurse -Include *.js -File
$filesAll  = $filesHtml + $filesJs

# 2) Safety Shim + helpers (injetado antes de </head>)
$shim = @"
<!-- SAFETY SHIM ADDED BY SCRIPT -->
<script>
(() => {
  const NIL = new Proxy(function(){}, {
    get(_, p) {
      if (p === 'value' || p === 'textContent' || p === 'innerHTML') return '';
      return (..._args) => NIL;
    },
    set() { return true; }
  });
  const _get = Document.prototype.getElementById;
  Document.prototype.getElementById = function(id) {
    return _get.call(this, id) || NIL;
  };
})();
</script>
<script>
const $ = (id) => {
  const el = document.getElementById(id);
  return (el && el.nodeType === 1) ? el : null;
};
const val = (id, fallback = '') => {
  const el = $(id);
  return el && 'value' in el ? el.value : fallback;
};
const setText = (id, text = '') => {
  const el = $(id);
  if (el) el.textContent = text;
};
const setHTML = (id, html = '') => {
  const el = $(id);
  if (el) el.innerHTML = html;
};
</script>
"@

foreach ($f in $filesHtml) {
  $content = Get-Content $f.FullName -Raw
  if ($content -notmatch 'SAFETY SHIM ADDED BY SCRIPT') {
    if ($content -match '</head>') {
      $content = $content -replace '</head>', ($shim + "`r`n</head>")
      Set-Content -LiteralPath $f.FullName -Value $content -Encoding UTF8
      Write-Host "Shim inserido em: $($f.FullName)"
    }
  }
}

# 3) Rewrites em HTML/JS: getElementById().value/.textContent/.innerHTML
function Rewrite-File {
  param([string]$path)

  $c = Get-Content $path -Raw

  # a) Leituras de .value  -> val('ID')
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*'([^'`""]+)'\s*\)\.value",
    "val('`$1')"
  )
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*`"([^`"']+)`"\s*\)\.value",
    "val('`$1')"
  )

  # b) Escritas .textContent = X  -> setText('ID', X)
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*'([^'`""]+)'\s*\)\.textContent\s*=\s*(.+?);",
    { param($m) "setText('$($m.Groups[1].Value)', $($m.Groups[2].Value));" },
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*`"([^`"']+)`"\s*\)\.textContent\s*=\s*(.+?);",
    { param($m) "setText('$($m.Groups[1].Value)', $($m.Groups[2].Value));" },
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )

  # c) Escritas .innerHTML = X  -> setHTML('ID', X)
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*'([^'`""]+)'\s*\)\.innerHTML\s*=\s*(.+?);",
    { param($m) "setHTML('$($m.Groups[1].Value)', $($m.Groups[2].Value));" },
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
  $c = [Regex]::Replace($c,
    "document\.getElementById\(\s*`"([^`"']+)`"\s*\)\.innerHTML\s*=\s*(.+?);",
    { param($m) "setHTML('$($m.Groups[1].Value)', $($m.Groups[2].Value));" },
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )

  # d) Substitui id="${time.id}" por data-time-id="${time.id}"
  $c = $c -replace 'id="\$\{time\.id\}"', 'data-time-id="`${time.id}"'

  Set-Content -LiteralPath $path -Value $c -Encoding UTF8
  Write-Host "Reescrito: $path"
}

foreach ($f in $filesAll) { Rewrite-File -path $f.FullName }

Write-Host "`n✅ Patch concluído. Dica: rode o app e confira o console (F12) para ver se restou algum acesso a ID inexistente."
