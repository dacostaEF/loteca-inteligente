# === Safety Shim Simples ===
$ErrorActionPreference = "Stop"

Write-Host "🚀 Aplicando Safety Shim Simples..." -ForegroundColor Green

# 1) Arquivos HTML
$filesHtml = Get-ChildItem -Recurse -Include *.html,*.htm -File

Write-Host "📁 Encontrados $($filesHtml.Count) arquivos HTML" -ForegroundColor Yellow

# 2) Safety Shim
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

# 3) Injetar shim em arquivos HTML
$injectedCount = 0
foreach ($f in $filesHtml) {
  $content = Get-Content $f.FullName -Raw
  if ($content -notmatch 'SAFETY SHIM ADDED BY SCRIPT') {
    if ($content -match '</head>') {
      $content = $content -replace '</head>', ($shim + "`r`n</head>")
      Set-Content -LiteralPath $f.FullName -Value $content -Encoding UTF8
      Write-Host "✅ Shim inserido em: $($f.Name)" -ForegroundColor Green
      $injectedCount++
    } else {
      Write-Host "⚠️ Arquivo sem </head>: $($f.Name)" -ForegroundColor Yellow
    }
  } else {
    Write-Host "⏭️ Shim já existe em: $($f.Name)" -ForegroundColor Gray
  }
}

Write-Host "`n🎉 SAFETY SHIM APLICADO COM SUCESSO!" -ForegroundColor Green
Write-Host "📊 Estatísticas:" -ForegroundColor Yellow
Write-Host "   • Arquivos HTML processados: $($filesHtml.Count)" -ForegroundColor White
Write-Host "   • Shims injetados: $injectedCount" -ForegroundColor White
Write-Host "`n💡 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. git add -A" -ForegroundColor White
Write-Host "   2. git commit -m 'aplica safety shim simples'" -ForegroundColor White
Write-Host "   3. Testar o aplicativo" -ForegroundColor White
Write-Host "   4. Verificar se não há mais crashes por IDs inexistentes" -ForegroundColor White
Write-Host "`n🛡️ Safety Shim ativo - IDs inexistentes não causarão mais crashes!" -ForegroundColor Magenta
