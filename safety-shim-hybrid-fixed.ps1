# === SCRIPT HÍBRIDO: SAFETY SHIM + REWRITES + DIAGNÓSTICO ===
$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando Safety Shim Híbrido + Rewrites..." -ForegroundColor Green

# 1) Arquivos alvo
$filesHtml = Get-ChildItem -Recurse -Include *.html,*.htm -File
$filesJs   = Get-ChildItem -Recurse -Include *.js -File
$filesAll  = $filesHtml + $filesJs

Write-Host "📁 Encontrados $($filesHtml.Count) arquivos HTML e $($filesJs.Count) arquivos JS" -ForegroundColor Yellow

# 2) Safety Shim Híbrido com Modo Diagnóstico
$shim = @"
<!-- SAFETY SHIM HÍBRIDO ADDED BY SCRIPT -->
<script>
(() => {
  // === MODO DIAGNÓSTICO ===
  const DEBUG_MISSING_IDS = true; // coloque false em produção
  
  // === SAFETY SHIM ===
  const NIL = new Proxy(function(){}, {
    get(_, p) {
      if (p === 'value' || p === 'textContent' || p === 'innerHTML') return '';
      return (..._args) => NIL;
    },
    set() { return true; }
  });
  
  // === ESTADO GLOBAL ===
  window.ADMIN_STATE = {
    currentSection: null,
    formData: {},
    lastSaved: null,
    isDirty: false
  };
  
  // === GETELEMENTBYID COM DIAGNÓSTICO ===
  const _get = Document.prototype.getElementById;
  Document.prototype.getElementById = function(id) {
    const el = _get.call(this, id);
    if (!el && DEBUG_MISSING_IDS) {
      console.warn('[MISSING-ID] getElementById(' + id + ') → null', new Error().stack.split('\n')[2]?.trim() || '');
    }
    return el || NIL;
  };
  
  // === FUNÇÕES DE ESTADO ===
  window.saveState = (sectionId, data) => {
    window.ADMIN_STATE.currentSection = sectionId;
    window.ADMIN_STATE.formData[sectionId] = data;
    window.ADMIN_STATE.lastSaved = new Date().toISOString();
    window.ADMIN_STATE.isDirty = false;
  };
  
  window.loadState = (sectionId) => {
    return window.ADMIN_STATE.formData[sectionId] || {};
  };
  
  window.syncDOMToState = (sectionId) => {
    const data = {};
    const section = document.getElementById(sectionId);
    if (section) {
      const inputs = section.querySelectorAll('input, select, textarea');
      inputs.forEach(input => {
        if (input.id) {
          data[input.id] = input.value;
        }
      });
    }
    window.saveState(sectionId, data);
  };
  
  window.syncStateToDOM = (sectionId) => {
    const data = window.loadState(sectionId);
    const section = document.getElementById(sectionId);
    if (section) {
      Object.entries(data).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element && 'value' in element) {
          element.value = value;
        }
      });
    }
  };
})();
</script>
<script>
// === HELPERS SEGUROS ===
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

// === HELPERS POR SEÇÃO ===
const $section = (sectionId, fieldName) => {
  const section = $(sectionId);
  if (!section) return null;
  return section.querySelector('[data-field="' + fieldName + '"]');
};

const valSection = (sectionId, fieldName, fallback = '') => {
  const el = $section(sectionId, fieldName);
  return el && 'value' in el ? el.value : fallback;
};

// === REHOOK EVENTS ===
window.rehookEvents = (sectionId) => {
  console.log('[LISTENERS] Re-anexando event listeners da seção: ' + sectionId);
  
  const section = $(sectionId);
  if (!section) {
    console.warn('[LISTENERS] Seção ' + sectionId + ' não encontrada');
    return;
  }
  
  // Re-anexar listeners de cadeado para esta seção
  const camposComCadeado = ['elencoTotal', 'pctProvaveis', 'valorElenco', 'ratingMedio', 'chutesPorJogo', 'posseBola', 'passesCertos'];
  
  camposComCadeado.forEach(fieldId => {
    const field = $section(sectionId, fieldId) || $(fieldId);
    if (field) {
      // Remover listeners existentes para evitar duplicação
      field.removeEventListener('input', window.mostrarCadeadoSePreenchido);
      field.removeEventListener('blur', window.mostrarCadeadoSePreenchido);
      
      // Adicionar novos listeners
      field.addEventListener('input', () => window.mostrarCadeadoSePreenchido(fieldId));
      field.addEventListener('blur', () => window.mostrarCadeadoSePreenchido(fieldId));
      // Verificar no carregamento
      if (window.mostrarCadeadoSePreenchido) {
        window.mostrarCadeadoSePreenchido(fieldId);
      }
    }
  });
  
  console.log('[LISTENERS] Event listeners da seção ' + sectionId + ' re-anexados com sucesso');
};

console.log('🛡️ Safety Shim Híbrido carregado com sucesso!');
</script>
"@

# 3) Injetar shim em arquivos HTML
Write-Host "🔧 Injetando Safety Shim em arquivos HTML..." -ForegroundColor Cyan
foreach ($f in $filesHtml) {
  $content = Get-Content $f.FullName -Raw
  if ($content -notmatch 'SAFETY SHIM HÍBRIDO ADDED BY SCRIPT') {
    if ($content -match '</head>') {
      $content = $content -replace '</head>', ($shim + "`r`n</head>")
      Set-Content -LiteralPath $f.FullName -Value $content -Encoding UTF8
      Write-Host "✅ Shim inserido em: $($f.Name)" -ForegroundColor Green
    } else {
      Write-Host "⚠️ Arquivo sem </head>: $($f.Name)" -ForegroundColor Yellow
    }
  } else {
    Write-Host "⏭️ Shim já existe em: $($f.Name)" -ForegroundColor Gray
  }
}

# 4) Função de rewrite
function Rewrite-File {
  param([string]$path)
  
  $c = Get-Content $path -Raw
  $originalContent = $c
  
  # a) Leituras de .value -> val('ID')
  $c = $c -replace "document\.getElementById\(\s*'([^']+)'\s*\)\.value", "val('`$1')"
  $c = $c -replace 'document\.getElementById\(\s*"([^"]+)"\s*\)\.value', 'val("`$1")'
  
  # b) Escritas .textContent = X -> setText('ID', X)
  $c = $c -replace "document\.getElementById\(\s*'([^']+)'\s*\)\.textContent\s*=\s*([^;]+);", "setText('`$1', `$2);"
  $c = $c -replace 'document\.getElementById\(\s*"([^"]+)"\s*\)\.textContent\s*=\s*([^;]+);', 'setText("`$1", `$2);'
  
  # c) Escritas .innerHTML = X -> setHTML('ID', X)
  $c = $c -replace "document\.getElementById\(\s*'([^']+)'\s*\)\.innerHTML\s*=\s*([^;]+);", "setHTML('`$1', `$2);"
  $c = $c -replace 'document\.getElementById\(\s*"([^"]+)"\s*\)\.innerHTML\s*=\s*([^;]+);', 'setHTML("`$1", `$2);'
  
  # d) Substitui id="${time.id}" por data-time-id="${time.id}"
  $c = $c -replace 'id="\$\{time\.id\}"', 'data-time-id="`${time.id}"'
  
  # e) Substitui getElementById por $ (helper seguro)
  $c = $c -replace "document\.getElementById\(\s*'([^']+)'\s*\)", "`$('`$1')"
  $c = $c -replace 'document\.getElementById\(\s*"([^"]+)"\s*\)', '`$("`$1")'
  
  if ($c -ne $originalContent) {
    Set-Content -LiteralPath $path -Value $c -Encoding UTF8
    Write-Host "✅ Reescrito: $path" -ForegroundColor Green
    return $true
  } else {
    Write-Host "⏭️ Sem mudanças: $path" -ForegroundColor Gray
    return $false
  }
}

# 5) Aplicar rewrites
Write-Host "🔄 Aplicando rewrites em arquivos..." -ForegroundColor Cyan
$rewrittenCount = 0
foreach ($f in $filesAll) {
  if (Rewrite-File -path $f.FullName) {
    $rewrittenCount++
  }
}

Write-Host "`n🎉 PATCH HÍBRIDO CONCLUÍDO!" -ForegroundColor Green
Write-Host "📊 Estatísticas:" -ForegroundColor Yellow
Write-Host "   • Arquivos HTML processados: $($filesHtml.Count)" -ForegroundColor White
Write-Host "   • Arquivos JS processados: $($filesJs.Count)" -ForegroundColor White
Write-Host "   • Arquivos reescritos: $rewrittenCount" -ForegroundColor White
Write-Host "`n💡 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. git add -A" -ForegroundColor White
Write-Host "   2. git commit -m 'aplica safety shim híbrido + rewrites'" -ForegroundColor White
Write-Host "   3. Testar o aplicativo" -ForegroundColor White
Write-Host "   4. Verificar console (F12) para IDs faltando" -ForegroundColor White
Write-Host "`n🛡️ Modo diagnóstico ativo - IDs faltando serão logados no console!" -ForegroundColor Magenta
