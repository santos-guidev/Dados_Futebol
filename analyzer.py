"""
Betting Analyzer - Servidor local (Versão Final Estabilizada)
Execute: python analyzer.py
Acesse:  http://localhost:8080
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs

PORT = 8080
# Base URL apontando para a raiz do repositório
BASE = "https://raw.githubusercontent.com/santos-guidev/Dados_Futebol/main/WebScraping_FlashScore/"

# ── Lista completa de arquivos históricos (Caminhos relativos a BASE) ─────────────────────────
HIST_FILES = [
    # Argentina
    "jogos_passados/argentina_2021.json","jogos_passados/argentina_2022.json","jogos_passados/argentina_2023.json",
    "jogos_passados/argentina_2024.json","jogos_passados/argentina_2025.json","jogos_passados/argentina_2026.json",
    # Australia
    "jogos_passados/australia_2021-2022.json","jogos_passados/australia_2022-2023.json","jogos_passados/australia_2023-2024.json",
    "jogos_passados/australia_2024-2025.json","jogos_passados/australia_2025-2026.json",
    # Austria
    "jogos_passados/austria_2021-2022.json","jogos_passados/austria_2022-2023.json","jogos_passados/austria_2023-2024.json",
    "jogos_passados/austria_2024-2025.json","jogos_passados/austria_2025-2026.json",
    # Belgium
    "jogos_passados/belgium_2021-2022.json","jogos_passados/belgium_2022-2023.json","jogos_passados/belgium_2023-2024.json",
    "jogos_passados/belgium_2024-2025.json","jogos_passados/belgium_2025-2026.json",
    # Bolivia
    "jogos_passados/bolivia_2021.json","jogos_passados/bolivia_2022.json","jogos_passados/bolivia_2023.json",
    "jogos_passados/bolivia_2024.json","jogos_passados/bolivia_2025.json","jogos_passados/bolivia_2026.json",
    # Bosnia
    "jogos_passados/bosnia-and-herzegovina_2021-2022.json","jogos_passados/bosnia-and-herzegovina_2022-2023.json",
    "jogos_passados/bosnia-and-herzegovina_2023-2024.json","jogos_passados/bosnia-and-herzegovina_2024-2025.json",
    "jogos_passados/bosnia-and-herzegovina_2025-2026.json",
    # Brazil
    "jogos_passados/brazil_2021.json","jogos_passados/brazil_2022.json","jogos_passados/brazil_2023.json",
    "jogos_passados/brazil_2024.json","jogos_passados/brazil_2025.json","jogos_passados/brazil_2026.json",
    # Bulgaria
    "jogos_passados/bulgaria_2021-2022.json","jogos_passados/bulgaria_2022-2023.json","jogos_passados/bulgaria_2023-2024.json",
    "jogos_passados/bulgaria_2024-2025.json","jogos_passados/bulgaria_2025-2026.json",
    # Chile
    "jogos_passados/chile_2021.json","jogos_passados/chile_2022.json","jogos_passados/chile_2023.json",
    "jogos_passados/chile_2024.json","jogos_passados/chile_2025.json","jogos_passados/chile_2026.json",
    # China
    "jogos_passados/china_2021.json","jogos_passados/china_2022.json","jogos_passados/china_2023.json",
    "jogos_passados/china_2024.json","jogos_passados/china_2025.json","jogos_passados/china_2026.json",
    # Colombia
    "jogos_passados/colombia_2021.json","jogos_passados/colombia_2022.json","jogos_passados/colombia_2023.json",
    "jogos_passados/colombia_2024.json","jogos_passados/colombia_2025.json","jogos_passados/colombia_2026.json",
    # Croatia
    "jogos_passados/croatia_2021-2022.json","jogos_passados/croatia_2022-2023.json","jogos_passados/croatia_2023-2024.json",
    "jogos_passados/croatia_2024-2025.json","jogos_passados/croatia_2025-2026.json",
    # Cyprus
    "jogos_passados/cyprus_2021-2022.json","jogos_passados/cyprus_2022-2023.json","jogos_passados/cyprus_2023-2024.json",
    "jogos_passados/cyprus_2024-2025.json","jogos_passados/cyprus_2025-2026.json",
    # Czech Republic
    "jogos_passados/czech-republic_2021-2022.json","jogos_passados/czech-republic_2022-2023.json",
    "jogos_passados/czech-republic_2023-2024.json","jogos_passados/czech-republic_2024-2025.json",
    "jogos_passados/czech-republic_2025-2026.json",
    # Denmark
    "jogos_passados/denmark_2021-2022.json","jogos_passados/denmark_2022-2023.json","jogos_passados/denmark_2023-2024.json",
    "jogos_passados/denmark_2024-2025.json","jogos_passados/denmark_2025-2026.json",
    # Ecuador
    "jogos_passados/ecuador_2021.json","jogos_passados/ecuador_2022.json","jogos_passados/ecuador_2023.json",
    "jogos_passados/ecuador_2024.json","jogos_passados/ecuador_2025.json","jogos_passados/ecuador_2026.json",
    # Egypt
    "jogos_passados/egypt_2021-2022.json","jogos_passados/egypt_2022-2023.json","jogos_passados/egypt_2023-2024.json",
    "jogos_passados/egypt_2024-2025.json","jogos_passados/egypt_2025-2026.json",
    # England
    "jogos_passados/england_2021-2022.json","jogos_passados/england_2022-2023.json","jogos_passados/england_2023-2024.json",
    "jogos_passados/england_2024-2025.json","jogos_passados/england_2025-2026.json",
    # Estonia
    "jogos_passados/estonia_2021.json","jogos_passados/estonia_2022.json","jogos_passados/estonia_2023.json",
    "jogos_passados/estonia_2024.json","jogos_passados/estonia_2025.json","jogos_passados/estonia_2026.json",
    # Europe
    "jogos_passados/europe_2021-2022.json","jogos_passados/europe_2022-2023.json","jogos_passados/europe_2023-2024.json",
    "jogos_passados/europe_2024-2025.json","jogos_passados/europe_2025-2026.json",
    # Finland
    "jogos_passados/finland_2021.json","jogos_passados/finland_2022.json","jogos_passados/finland_2023.json",
    "jogos_passados/finland_2024.json","jogos_passados/finland_2025.json","jogos_passados/finland_2026.json",
    # France
    "jogos_passados/france_2021-2022.json","jogos_passados/france_2022-2023.json","jogos_passados/france_2023-2024.json",
    "jogos_passados/france_2024-2025.json","jogos_passados/france_2025-2026.json",
    # Germany
    "jogos_passados/germany_2021-2022.json","jogos_passados/germany_2022-2023.json","jogos_passados/germany_2023-2024.json",
    "jogos_passados/germany_2024-2025.json","jogos_passados/germany_2025-2026.json",
    # Greece
    "jogos_passados/greece_2021-2022.json","jogos_passados/greece_2022-2023.json","jogos_passados/greece_2023-2024.json",
    "jogos_passados/greece_2024-2025.json","jogos_passados/greece_2025-2026.json",
    # Iceland
    "jogos_passados/iceland_2021.json","jogos_passados/iceland_2022.json","jogos_passados/iceland_2023.json",
    "jogos_passados/iceland_2024.json","jogos_passados/iceland_2025.json","jogos_passados/iceland_2026.json",
    # Ireland
    "jogos_passados/ireland_2021.json","jogos_passados/ireland_2022.json","jogos_passados/ireland_2023.json",
    "jogos_passados/ireland_2024.json","jogos_passados/ireland_2025.json","jogos_passados/ireland_2026.json",
    # Israel
    "jogos_passados/israel_2021-2022.json","jogos_passados/israel_2022-2023.json","jogos_passados/israel_2023-2024.json",
    "jogos_passados/israel_2024-2025.json","jogos_passados/israel_2025-2026.json",
    # Italy
    "jogos_passados/italy_2021-2022.json","jogos_passados/italy_2022-2023.json","jogos_passados/italy_2023-2024.json",
    "jogos_passados/italy_2024-2025.json","jogos_passados/italy_2025-2026.json",
    # Japan
    "jogos_passados/japan_2021.json","jogos_passados/japan_2022.json","jogos_passados/japan_2023.json",
    "jogos_passados/japan_2024.json","jogos_passados/japan_2025.json","jogos_passados/japan_2026.json",
    # Mexico
    "jogos_passados/mexico_2021-2022.json","jogos_passados/mexico_2022-2023.json","jogos_passados/mexico_2023-2024.json",
    "jogos_passados/mexico_2024-2025.json","jogos_passados/mexico_2025-2026.json",
    # Netherlands
    "jogos_passados/netherlands_2021-2022.json","jogos_passados/netherlands_2022-2023.json","jogos_passados/netherlands_2023-2024.json",
    "jogos_passados/netherlands_2024-2025.json","jogos_passados/netherlands_2025-2026.json",
    # Northern Ireland
    "jogos_passados/northern-ireland_2021-2022.json","jogos_passados/northern-ireland_2022-2023.json",
    "jogos_passados/northern-ireland_2023-2024.json","jogos_passados/northern-ireland_2024-2025.json",
    "jogos_passados/northern-ireland_2025-2026.json",
    # Norway
    "jogos_passados/norway_2021.json","jogos_passados/norway_2022.json","jogos_passados/norway_2023.json",
    "jogos_passados/norway_2024.json","jogos_passados/norway_2025.json","jogos_passados/norway_2026.json",
    # Paraguay
    "jogos_passados/paraguay_2021.json","jogos_passados/paraguay_2022.json","jogos_passados/paraguay_2023.json",
    "jogos_passados/paraguay_2024.json","jogos_passados/paraguay_2025.json","jogos_passados/paraguay_2026.json",
    # Peru
    "jogos_passados/peru_2021.json","jogos_passados/peru_2022.json","jogos_passados/peru_2023.json",
    "jogos_passados/peru_2024.json","jogos_passados/peru_2025.json","jogos_passados/peru_2026.json",
    # Poland
    "jogos_passados/poland_2021-2022.json","jogos_passados/poland_2022-2023.json","jogos_passados/poland_2023-2024.json",
    "jogos_passados/poland_2024-2025.json","jogos_passados/poland_2025-2026.json",
    # Portugal
    "jogos_passados/portugal_2021-2022.json","jogos_passados/portugal_2022-2023.json","jogos_passados/portugal_2023-2024.json",
    "jogos_passados/portugal_2024-2025.json","jogos_passados/portugal_2025-2026.json",
    # Romania
    "jogos_passados/romania_2021-2022.json","jogos_passados/romania_2022-2023.json","jogos_passados/romania_2023-2024.json",
    "jogos_passados/romania_2024-2025.json","jogos_passados/romania_2025-2026.json",
    # Saudi Arabia
    "jogos_passados/saudi-arabia_2021-2022.json","jogos_passados/saudi-arabia_2022-2023.json","jogos_passados/saudi-arabia_2023-2024.json",
    "jogos_passados/saudi-arabia_2024-2025.json","jogos_passados/saudi-arabia_2025-2026.json",
    # Scotland
    "jogos_passados/scotland_2021-2022.json","jogos_passados/scotland_2022-2023.json","jogos_passados/scotland_2023-2024.json",
    "jogos_passados/scotland_2024-2025.json","jogos_passados/scotland_2025-2026.json",
    # Serbia
    "jogos_passados/serbia_2021-2022.json","jogos_passados/serbia_2022-2023.json","jogos_passados/serbia_2023-2024.json",
    "jogos_passados/serbia_2024-2025.json","jogos_passados/serbia_2025-2026.json",
    # Slovakia
    "jogos_passados/slovakia_2021-2022.json","jogos_passados/slovakia_2022-2023.json","jogos_passados/slovakia_2023-2024.json",
    "jogos_passados/slovakia_2024-2025.json","jogos_passados/slovakia_2025-2026.json",
    # Slovenia
    "jogos_passados/slovenia_2021-2022.json","jogos_passados/slovenia_2022-2023.json","jogos_passados/slovenia_2023-2024.json",
    "jogos_passados/slovenia_2024-2025.json","jogos_passados/slovenia_2025-2026.json",
    # South Africa
    "jogos_passados/south-africa_2021-2022.json","jogos_passados/south-africa_2022-2023.json","jogos_passados/south-africa_2023-2024.json",
    "jogos_passados/south-africa_2024-2025.json","jogos_passados/south-africa_2025-2026.json",
    # South America
    "jogos_passados/south-america_2021.json","jogos_passados/south-america_2022.json","jogos_passados/south-america_2023.json",
    "jogos_passados/south-america_2024.json","jogos_passados/south-america_2025.json","jogos_passados/south-america_2026.json",
    # South Korea
    "jogos_passados/south-korea_2021.json","jogos_passados/south-korea_2022.json","jogos_passados/south-korea_2023.json",
    "jogos_passados/south-korea_2024.json","jogos_passados/south-korea_2025.json","jogos_passados/south-korea_2026.json",
    # Spain
    "jogos_passados/spain_2021-2022.json","jogos_passados/spain_2022-2023.json","jogos_passados/spain_2023-2024.json",
    "jogos_passados/spain_2024-2025.json","jogos_passados/spain_2025-2026.json",
    # Sweden
    "jogos_passados/sweden_2021.json","jogos_passados/sweden_2022.json","jogos_passados/sweden_2023.json",
    "jogos_passados/sweden_2024.json","jogos_passados/sweden_2025.json","jogos_passados/sweden_2026.json",
    # Switzerland
    "jogos_passados/switzerland_2021-2022.json","jogos_passados/switzerland_2022-2023.json","jogos_passados/switzerland_2023-2024.json",
    "jogos_passados/switzerland_2024-2025.json","jogos_passados/switzerland_2025-2026.json",
    # Turkey
    "jogos_passados/turkey_2021-2022.json","jogos_passados/turkey_2022-2023.json","jogos_passados/turkey_2023-2024.json",
    "jogos_passados/turkey_2024-2025.json","jogos_passados/turkey_2025-2026.json",
    # Ukraine
    "jogos_passados/ukraine_2021-2022.json","jogos_passados/ukraine_2022-2023.json","jogos_passados/ukraine_2023-2024.json",
    "jogos_passados/ukraine_2024-2025.json","jogos_passados/ukraine_2025-2026.json",
    # Uruguay
    "jogos_passados/uruguay_2021.json","jogos_passados/uruguay_2022.json","jogos_passados/uruguay_2023.json",
    "jogos_passados/uruguay_2024.json","jogos_passados/uruguay_2025.json","jogos_passados/uruguay_2026.json",
    # USA
    "jogos_passados/usa_2021.json","jogos_passados/usa_2022.json","jogos_passados/usa_2023.json",
    "jogos_passados/usa_2024.json","jogos_passados/usa_2025.json","jogos_passados/usa_2026.json",
    # Venezuela
    "jogos_passados/venezuela_2021.json","jogos_passados/venezuela_2022.json","jogos_passados/venezuela_2023.json",
    "jogos_passados/venezuela_2024.json","jogos_passados/venezuela_2025.json","jogos_passados/venezuela_2026.json",
    # Wales
    "jogos_passados/wales_2021-2022.json","jogos_passados/wales_2022-2023.json","jogos_passados/wales_2023-2024.json",
    "jogos_passados/wales_2024-2025.json","jogos_passados/wales_2025-2026.json",
]

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Betting Analyzer</title>
<style>
:root {
  --bg:#0f1117;--bg2:#181c27;--bg3:#1e2436;
  --border:rgba(255,255,255,0.08);--border2:rgba(255,255,255,0.15);
  --text:#e8eaf0;--text2:#8b92a8;--text3:#555d72;
  --green:#22c55e;--green-bg:rgba(34,197,94,.1);--green-bd:rgba(34,197,94,.3);
  --yellow:#f59e0b;--yellow-bg:rgba(245,158,11,.1);--yellow-bd:rgba(245,158,11,.3);
  --red:#ef4444;--red-bg:rgba(239,68,68,.1);--red-bd:rgba(239,68,68,.3);
  --blue:#3b82f6;--blue-bg:rgba(59,130,246,.1);--blue-bd:rgba(59,130,246,.3);
  --mono:'Courier New',monospace;--r:8px;--rl:12px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px}
.wrap{max-width:1400px;margin:0 auto;padding:1.5rem}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;flex-wrap:wrap;gap:10px}
.title{font-size:13px;font-weight:500;color:var(--text2);letter-spacing:.08em;text-transform:uppercase}
.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
input[type=date]{background:var(--bg2);border:1px solid var(--border2);color:var(--text);padding:7px 12px;border-radius:var(--r);font-size:13px;font-family:var(--mono);cursor:pointer}
input[type=date]::-webkit-calendar-picker-indicator{filter:invert(.7);cursor:pointer}
button{padding:7px 16px;font-size:12px;border:1px solid var(--border2);border-radius:var(--r);background:transparent;color:var(--text);cursor:pointer;font-family:inherit;transition:background .15s}
button:hover{background:var(--bg3)}
button.primary{border-color:var(--blue-bd);color:var(--blue)}
button.primary:hover{background:var(--blue-bg)}
button:disabled{opacity:.4;cursor:not-allowed}
.hist-prog{display:none;width:100%;background:var(--bg2);border:1px solid var(--border);border-radius:var(--r);padding:10px;margin-bottom:1rem}
.prog-bar{height:4px;background:var(--bg3);border-radius:2px;overflow:hidden;margin-bottom:6px}
.prog-fill{height:100%;background:var(--blue);width:0%;transition:width .3s}
.prog-lbl{font-size:11px;color:var(--text3);font-family:var(--mono)}
.stats-bar{display:flex;gap:15px;margin-bottom:1rem;background:var(--bg2);padding:12px;border-radius:var(--r);border:1px solid var(--border)}
.stat-item{display:flex;flex-direction:column;gap:2px}
.stat-val{font-size:16px;font-weight:700;font-family:var(--mono)}
.stat-lbl{font-size:10px;color:var(--text3);text-transform:uppercase}
.main-grid{display:grid;grid-template-columns:1fr 380px;gap:1.5rem;align-items:start}
@media(max-width:1000px){.main-grid{grid-template-columns:1fr}}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden}
.table-area{min-height:400px}
table{width:100%;border-collapse:collapse;text-align:left}
th{background:var(--bg3);padding:12px 16px;font-size:11px;text-transform:uppercase;color:var(--text3);letter-spacing:.05em;border-bottom:1px solid var(--border)}
td{padding:12px 16px;border-bottom:1px solid var(--border);vertical-align:middle}
tr:hover td{background:rgba(255,255,255,0.02);cursor:pointer}
tr.sel td{background:var(--blue-bg)}
.tm{font-weight:600;font-size:14px;margin-bottom:2px}
.sub{font-size:11px;color:var(--text3)}
.mono{font-family:var(--mono);font-size:12px}
.badge{display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.02em}
.bg{background:var(--green-bg);color:var(--green);border:1px solid var(--green-bd)}
.bw{background:var(--yellow-bg);color:var(--yellow);border:1px solid var(--yellow-bd)}
.bn{background:var(--bg3);color:var(--text3);border:1px solid var(--border2)}
.pbar{display:flex;align-items:center;gap:8px;margin-bottom:4px}
.ptrack{flex:1;height:4px;background:var(--bg3);border-radius:2px;overflow:hidden}
.pfill{height:100%;border-radius:2px}
.pfill.g{background:var(--green)}
.pfill.y{background:var(--yellow)}
.pfill.r{background:var(--red)}
.pnum{font-family:var(--mono);font-size:11px;min-width:30px;text-align:right}
.detail{padding:1.5rem}
.dh{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem}
.dt{font-size:18px;font-weight:700;margin-bottom:4px}
.ds{font-size:12px;color:var(--text2)}
.strat-grid{display:grid;gap:12px;margin-bottom:1.5rem}
.sbox{padding:12px;border-radius:var(--r);border:1px solid var(--border2);background:var(--bg3)}
.sbox.ok{border-color:var(--green-bd);background:var(--green-bg)}
.sbox.med{border-color:var(--yellow-bd);background:var(--yellow-bg)}
.sbox.bad{opacity:.7}
.sn{font-size:11px;text-transform:uppercase;color:var(--text3);font-weight:700;margin-bottom:8px}
.sp{font-size:20px;font-weight:700;font-family:var(--mono);margin-bottom:2px}
.sf{font-size:12px;color:var(--text2);margin-bottom:8px}
.sev{font-family:var(--mono);font-size:13px;font-weight:700}
.snote{font-size:10px;color:var(--text3);margin-top:2px}
.slbl{font-size:11px;font-weight:700;text-transform:uppercase;color:var(--text3);margin:1.5rem 0 .75rem;display:flex;align-items:center;gap:8px}
.slbl::after{content:'';flex:1;height:1px;background:var(--border)}
.bk-grid{display:grid;grid-template-columns:1fr;gap:4px}
.bk-row{display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;padding:6px 8px;background:var(--bg3);border-radius:4px}
.bk-name{color:var(--text2)}
.hist-row{display:flex;flex-wrap:wrap;gap:6px}
.hchip{padding:4px 8px;background:var(--bg3);border:1px solid var(--border2);border-radius:4px;font-size:11px;color:var(--text2)}
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;height:300px;color:var(--text3)}
.loading{padding:40px;text-align:center;color:var(--text2);font-style:italic}
.err{color:var(--red);font-family:var(--mono);font-size:12px;margin-top:10px;max-width:300px;text-align:center}
.pills{display:flex;gap:6px;margin-bottom:1rem}
.pill{padding:6px 12px;border-radius:20px;background:var(--bg2);border:1px solid var(--border2);font-size:11px;color:var(--text2);cursor:pointer;transition:all .2s}
.pill:hover{background:var(--bg3)}
.pill.on{background:var(--blue-bg);color:var(--blue);border-color:var(--blue-bd)}
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div class="title">Betting Analyzer <span id="status" style="margin-left:15px;text-transform:none;font-weight:400;color:var(--text3)"></span></div>
    <div class="controls">
      <input type="date" id="dateInput">
      <button class="primary" onclick="loadJogos()">Carregar Jogos</button>
      <button id="btnHist" onclick="loadHistorico()">Carregar Historico</button>
    </div>
  </div>

  <div id="histProgress" class="hist-prog">
    <div class="prog-bar"><div id="progFill" class="prog-fill"></div></div>
    <div id="progLbl" class="prog-lbl">Iniciando...</div>
  </div>

  <div class="stats-bar">
    <div class="stat-item"><span class="stat-lbl">Jogos</span><span class="stat-val" id="sTotal">0</span></div>
    <div class="stat-item"><span class="stat-lbl">Over 0.5</span><span class="stat-val" id="sOver" style="color:var(--green)">0</span></div>
    <div class="stat-item"><span class="stat-lbl">Back Favorito</span><span class="stat-val" id="sBack" style="color:var(--blue)">0</span></div>
    <div class="stat-item"><span class="stat-lbl">Scalpe Under</span><span class="stat-val" id="sScalpe" style="color:var(--yellow)">0</span></div>
  </div>

  <div class="pills">
    <div class="pill on" onclick="setPill(this,'all')">Todos</div>
    <div class="pill" onclick="setPill(this,'over05')">Over 0.5 FT</div>
    <div class="pill" onclick="setPill(this,'back')">Back favorito</div>
    <div class="pill" onclick="setPill(this,'scalpe')">Scalpe under</div>
    <div class="pill" onclick="setPill(this,'multi')">Multi-sinal</div>
  </div>

  <div class="main-grid">
    <div class="card table-area" id="tableArea">
      <div class="empty">Clique em "Carregar historico" primeiro, depois "Carregar jogos"</div>
    </div>
    <div class="card" id="detailArea">
      <div class="empty">Clique em um jogo para detalhes</div>
    </div>
  </div>
</div>

<script>
let allMatches = [];
let histStats = {};
let selectedIdx = -1;
let activeFilter = 'all';

function status(m){ document.getElementById('status').textContent=m; }

// ── UTILS ──────────────────────────────────────────────────────────
function getBest(m){
  const a=m.Odds_1X2_FT||[];
  if(!a.length) return {o1:m.Best_Odd_1_FT||2,oX:m.Best_Odd_X_FT||3,o2:m.Best_Odd_2_FT||2,bk1:'—'};
  let b={o1:0,oX:0,o2:0,bk1:'',bkX:'',bk2:''};
  a.forEach(x=>{
    if(x.Odd_1>b.o1){b.o1=x.Odd_1;b.bk1=x.Bookmaker}
    if(x.Odd_X>b.oX){b.oX=x.Odd_X;b.bkX=x.Bookmaker}
    if(x.Odd_2>b.o2){b.o2=x.Odd_2;b.bk2=x.Bookmaker}
  });
  return b;
}
function getAvg(m){
  const a=m.Odds_1X2_FT||[];
  if(!a.length) return getBest(m);
  let s1=0,sX=0,s2=0;
  a.forEach(x=>{s1+=x.Odd_1||0;sX+=x.Odd_X||0;s2+=x.Odd_2||0});
  return {o1:s1/a.length,oX:sX/a.length,o2:s2/a.length};
}
function getBestOU(m,line){
  const ou=m.Odds_OU_FT;
  if(!ou||!ou[line]||!ou[line].length) return null;
  let b={over:0,under:0,bk:''};
  ou[line].forEach(x=>{
    if(x.Over>b.over){b.over=x.Over;b.bk=x.Bookmaker}
    if(x.Under>b.under) b.under=x.Under;
  });
  return b.over>0?b:null;
}

// ── ESTRATÉGIAS ────────────────────────────────────────────────────
function calc(m, hH, hA){
  const avg=getAvg(m), best=getBest(m);
  const ou05=getBestOU(m,'OU_0.5');

  const tot=1/avg.o1+1/avg.oX+1/avg.o2;
  const pH=(1/avg.o1)/tot, pX=(1/avg.oX)/tot, pA=(1/avg.o2)/tot;
  const margin=(tot-1)*100;

  const [pFav,oddFav,favName] = pH>=pA ? [pH,best.o1,m.Home] : [pA,best.o2,m.Away];
  const backRange = oddFav>=1.50 && oddFav<=2.00;
  const edge      = pFav - 1/oddFav;
  const backOk    = backRange && edge>0;
  const evFav     = (oddFav-1)*pFav-(1-pFav);

  let pMkt=null;
  if(ou05){ const t=1/ou05.over+1/ou05.under; pMkt=(1/ou05.over)/t; }
  const hRate_H = hH?.over05Rate??null, hRate_A = hA?.over05Rate??null;
  const pHist   = (hRate_H!==null&&hRate_A!==null) ? (hRate_H+hRate_A)/2 : null;
  let pOver;
  if(pMkt!==null&&pHist!==null)   pOver=pMkt*0.55+pHist*0.45;
  else if(pMkt!==null)             pOver=pMkt;
  else if(pHist!==null)            pOver=Math.min(.97,pHist);
  else                             pOver=Math.min(.90,.58+pFav*.4);
  const overOk = pOver>=0.72;
  const evOver = ou05?(ou05.over-1)*pOver-(1-pOver):null;

  let uLine=null;
  for(const l of['OU_2.5','OU_2.0','OU_1.5']){
    const x=getBestOU(m,l); if(x){uLine={...x,line:l};break;}
  }
  const pU = uLine?1/uLine.under:null;

  const gsH=hH?.avgGoalsScored??null, gcH=hH?.avgGoalsConceded??null;
  const gsA=hA?.avgGoalsScored??null, gcA=hA?.avgGoalsConceded??null;
  const expH=(gsH!==null&&gcA!==null)?(gsH+gcA)/2:null;
  const expA=(gsA!==null&&gcH!==null)?(gsA+gcH)/2:null;
  const expTot=(expH!==null&&expA!==null)?expH+expA:null;
  const lowSco=expTot!==null?expTot<2.5:null;

  const scalpeOk=!!(pU&&pU<0.45&&lowSco&&uLine.under>=1.80);
  const evUnder=uLine?(uLine.under-1)*(pU||0.3)-(1-(pU||0.3)):null;

  const signals=(overOk?1:0)+(backOk?1:0)+(scalpeOk?1:0);
  return {margin,pH,pX,pA,pFav,oddFav,favName,backRange,edge,backOk,evFav,
          pOver,pMkt,pHist,overOk,evOver,ou05,
          uLine,pU,expTot,lowSco,scalpeOk,evUnder,
          signals,avg,best,hH,hA};
}

// ── HISTÓRICO ──────────────────────────────────────────────────────
function buildHist(data){
  const s={};
  const leagues = data.leagues || (data.matches ? [{matches: data.matches}] : []);
  leagues.forEach(lg=>{
    (lg.matches||[]).forEach(m=>{
      if(m.Home_Score==null) return;
      const tot=(parseInt(m.Home_Score)||0)+(parseInt(m.Away_Score)||0);
      [[m.Home,parseInt(m.Home_Score),parseInt(m.Away_Score)],[m.Away,parseInt(m.Away_Score),parseInt(m.Home_Score)]].forEach(([t,gs,gc])=>{
        if(!t) return;
        const k=t.toLowerCase().trim();
        if(!s[k]) s[k]={gs:0,gc:0,n:0,o05:0};
        s[k].n++; s[k].gs+=gs||0; s[k].gc+=gc||0;
        if(tot>0) s[k].o05++;
      });
    });
  });
  Object.keys(s).forEach(k=>{
    const x=s[k];
    x.avgGoalsScored   = x.n?+(x.gs/x.n).toFixed(2):null;
    x.avgGoalsConceded = x.n?+(x.gc/x.n).toFixed(2):null;
    x.over05Rate       = x.n?+(x.o05/x.n):null;
  });
  return s;
}

function fuzzy(name){
  if(!name) return null;
  const k=name.toLowerCase().trim();
  if(histStats[k]) return histStats[k];
  // Normalização para busca aproximada (remove acentos e abreviações comuns)
  const norm = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\./g, "").replace(/-/g, " ");
  const nk = norm(k);
  for(const key of Object.keys(histStats)){
    const nkey = norm(key);
    if(nkey.includes(nk)||nk.includes(nkey)) return histStats[key];
  }
  return null;
}

// ── PROCESS & RENDER ──────────────────────────────────────────────
function pct(v){ return v!=null?(v*100).toFixed(1)+'%':'—'; }
function evStr(v){ if(v==null)return'—'; return(v>=0?'+':'')+v.toFixed(2); }

function processMatches(data){
  const matches = data.matches || data;
  if(!Array.isArray(matches)) return;
  allMatches=matches.map(m=>({...m,strats:calc(m,fuzzy(m.Home),fuzzy(m.Away))}));
  
  document.getElementById('sTotal').textContent=allMatches.length;
  document.getElementById('sOver').textContent=allMatches.filter(m=>m.strats.overOk).length;
  document.getElementById('sBack').textContent=allMatches.filter(m=>m.strats.backOk).length;
  document.getElementById('sScalpe').textContent=allMatches.filter(m=>m.strats.scalpeOk).length;
  applyFilter();
}

function applyFilter(){
  if(!allMatches.length) return;
  let f=allMatches;
  if(activeFilter==='over05') f=f.filter(m=>m.strats.overOk);
  if(activeFilter==='back')   f=f.filter(m=>m.strats.backOk);
  if(activeFilter==='scalpe') f=f.filter(m=>m.strats.scalpeOk);
  if(activeFilter==='multi')  f=f.filter(m=>m.strats.signals>=2);
  renderTable(f);
}
function setPill(el,f){
  document.querySelectorAll('.pill').forEach(p=>p.classList.remove('on'));
  el.classList.add('on'); activeFilter=f; applyFilter();
}

function renderTable(matches){
  if(!matches.length){
    document.getElementById('tableArea').innerHTML='<div class="empty">Nenhum jogo para este filtro.</div>'; return;
  }
  let h=`<table><thead><tr>
    <th style="width:22%">Partida</th><th style="width:7%">Hora</th>
    <th style="width:20%">Over 0.5 FT</th>
    <th style="width:20%">Back favorito</th>
    <th style="width:20%">Scalpe under</th>
    <th style="width:11%">Sinais</th>
  </tr></thead><tbody>`;

  matches.forEach(m=>{
    const gi=allMatches.indexOf(m), s=m.strats;
    const op=(s.pOver*100).toFixed(0);
    const oc=s.pOver>=.80?'g':s.pOver>=.72?'y':'r';
    const ob=s.overOk?(s.pOver>=.80?'bg':'bw'):'bn';
    const bb=s.backOk?'bg':s.backRange?'bw':'bn';
    const sb=s.scalpeOk?'bg':'bn';
    const sigC=s.signals===3?'bg':s.signals===2?'bw':'bn';

    h+=`<tr class="${selectedIdx===gi?'sel':''}" onclick="showDetail(${gi})">
      <td><div class="tm">${m.Home} v ${m.Away}</div><div class="sub">${m.League||'—'}</div></td>
      <td class="mono">${m.Time||'—'}</td>
      <td>
        <div class="pbar"><div class="ptrack"><div class="pfill ${oc}" style="width:${op}%"></div></div><span class="pnum">${op}%</span></div>
        <span class="badge ${ob}">${s.overOk?'sinal':'baixo'}</span>
        ${s.pHist!=null?`<div class="sub" style="margin-top:2px">hist ${pct(s.pHist)}</div>`:'<div class="sub" style="margin-top:2px;color:#854f0b">sem hist</div>'}
      </td>
      <td>
        <div class="mono" style="margin-bottom:3px">${s.favName} @ ${s.oddFav.toFixed(2)}</div>
        <span class="badge ${bb}">${s.backOk?'sinal':s.backRange?'sem edge':'fora faixa'}</span>
        ${s.backRange?`<div class="sub" style="margin-top:2px">edge ${s.edge>=0?'+':''}${(s.edge*100).toFixed(1)}%</div>`:''}
      </td>
      <td>
        <span class="badge ${sb}">${s.scalpeOk?'sinal':'—'}</span>
        ${s.uLine?`<div class="sub" style="margin-top:2px">${s.uLine.line} u ${s.uLine.under.toFixed(2)}</div>`:''}
        ${s.expTot!=null?`<div class="sub">exp ${s.expTot.toFixed(1)} gols</div>`:'<div class="sub" style="color:#854f0b">sem hist</div>'}
      </td>
      <td><span class="badge ${sigC}" style="font-size:11px">${s.signals}/3</span></td>
    </tr>`;
  });
  h+='</tbody></table>';
  document.getElementById('tableArea').innerHTML=h;
}

function showDetail(idx){
  selectedIdx=idx; applyFilter();
  const m=allMatches[idx], s=m.strats;
  const oc=s.pOver>=.80?'ok':s.pOver>=.72?'med':'bad';
  const bc=s.backOk?'ok':s.backRange?'med':'bad';
  const sc2=s.scalpeOk?'ok':'bad';

  const bkRows=(m.Odds_1X2_FT||[]).slice(0,14).map(b=>
    `<div class="bk-row"><span class="bk-name">${b.Bookmaker}</span><span>${b.Odd_1.toFixed(2)} / ${b.Odd_X.toFixed(2)} / ${b.Odd_2.toFixed(2)}</span></div>`
  ).join('');

  let ou05Rows='';
  if(m.Odds_OU_FT?.['OU_0.5']){
    ou05Rows=m.Odds_OU_FT['OU_0.5'].slice(0,10).map(b=>
      `<div class="bk-row"><span class="bk-name">${b.Bookmaker}</span><span>O ${b.Over} / U ${b.Under}</span></div>`
    ).join('');
  }

  let hist='';
  if(s.hH||s.hA){
    hist=`<div class="slbl">Historico dos times</div><div class="hist-row">`;
    if(s.hH) hist+=`<span class="hchip">${m.Home}: ${s.hH.n}j | marc. ${s.hH.avgGoalsScored} | sofr. ${s.hH.avgGoalsConceded} | over05 ${(s.hH.over05Rate*100).toFixed(0)}%</span>`;
    if(s.hA) hist+=`<span class="hchip">${m.Away}: ${s.hA.n}j | marc. ${s.hA.avgGoalsScored} | sofr. ${s.hA.avgGoalsConceded} | over05 ${(s.hA.over05Rate*100).toFixed(0)}%</span>`;
    hist+='</div>';
  }

  document.getElementById('detailArea').innerHTML=`<div class="detail">
    <div class="dh">
      <div><div class="dt">${m.Home} vs ${m.Away}</div><div class="ds">${m.League||''} · ${m.Date||''} ${m.Time||''}</div></div>
      <button onclick="document.getElementById('detailArea').innerHTML='';selectedIdx=-1;applyFilter()">fechar</button>
    </div>
    <div class="strat-grid">
      <div class="sbox ${oc}">
        <div class="sn">Over 0.5 FT</div><div class="sp">${pct(s.pOver)}</div>
        <div class="sf">fair: ${(1/s.pOver).toFixed(2)}${s.ou05?' · mkt over '+s.ou05.over.toFixed(2):''}</div>
        <div class="sev" style="color:${(s.evOver||0)>=0?'var(--green)':'var(--red)'}">${evStr(s.evOver)}</div>
        <div class="snote">mkt: ${pct(s.pMkt)} · hist: ${pct(s.pHist)}</div>
        <div class="snote" style="margin-top:3px;font-weight:500;color:${s.overOk?'var(--green)':'var(--text3)'}">${s.overOk?'SINAL':'sem sinal'}</div>
      </div>
      <div class="sbox ${bc}">
        <div class="sn">Back favorito</div><div class="sp">${pct(s.pFav)}</div>
        <div class="sf">${s.favName} @ ${s.oddFav.toFixed(2)} · fair ${(1/s.pFav).toFixed(2)}</div>
        <div class="sev" style="color:${s.evFav>=0?'var(--green)':'var(--red)'}">${evStr(s.evFav)}</div>
        <div class="snote">edge: ${s.edge>=0?'+':''}${(s.edge*100).toFixed(1)}% · faixa 1.50-2.00</div>
        <div class="snote" style="margin-top:3px;font-weight:500;color:${s.backOk?'var(--green)':'var(--text3)'}">${s.backOk?'SINAL':s.backRange?'odd ok sem edge':'fora da faixa'}</div>
      </div>
      <div class="sbox ${sc2}">
        <div class="sn">Scalpe under</div><div class="sp">${s.uLine?pct(s.pU):'—'}</div>
        <div class="sf">${s.uLine?s.uLine.line+' u @ '+s.uLine.under.toFixed(2)+' ('+s.uLine.bk+')':'—'}</div>
        <div class="sev" style="color:${(s.evUnder||0)>=0?'var(--green)':'var(--red)'}">${evStr(s.evUnder)}</div>
        <div class="snote">exp: ${s.expTot!=null?s.expTot.toFixed(2):'—'} gols · low-sco: ${s.lowSco?'sim':'não'}</div>
        <div class="snote" style="margin-top:3px;font-weight:500;color:${s.scalpeOk?'var(--green)':'var(--text3)'}">${s.scalpeOk?'SINAL':'sem sinal'}</div>
      </div>
    </div>
    ${hist}${bkRows?`<div class="slbl">Odds 1X2</div><div class="bk-grid">${bkRows}</div>`:''}
  </div>`;
  document.getElementById('detailArea').scrollIntoView({behavior:'smooth',block:'nearest'});
}

// ── FETCH ──────────────────────────────────────────────────────────
async function loadJogos(){
  const d=document.getElementById('dateInput').value;
  if(!d){alert('Selecione uma data');return;}
  document.getElementById('tableArea').innerHTML=`<div class="loading">Carregando jogos para ${d}...</div>`;
  document.getElementById('detailArea').innerHTML='';
  status('');
  try{
    const r=await fetch(`/proxy?url=jogos_futuros/jogos_flashscore_${d}.json`);
    const j=await r.json();
    if(j.error) throw new Error(j.error);
    processMatches(j);
    const htxt=Object.keys(histStats).length>0?` · ${Object.keys(histStats).length} times no historico`:'';
    status(`${allMatches.length} jogos carregados · ${d}${htxt}`);
  }catch(e){
    document.getElementById('tableArea').innerHTML=`<div class="empty"><div class="err">${e.message}</div></div>`;
  }
}

const HIST_FILES_JS = HIST_FILES_PLACEHOLDER;

async function loadHistorico(){
  const btn=document.getElementById('btnHist');
  const prog=document.getElementById('histProgress');
  const fill=document.getElementById('progFill');
  const lbl=document.getElementById('progLbl');

  btn.disabled=true;
  prog.style.display='block';
  histStats={};

  let loaded=0, total=HIST_FILES_JS.length;

  for(let i=0;i<HIST_FILES_JS.length;i++){
    const f=HIST_FILES_JS[i];
    fill.style.width=((i/total)*100).toFixed(0)+'%';
    lbl.textContent=`${i+1}/${total} · ${f}`;
    try{
      const r=await fetch(`/proxy?url=${f}`);
      const data=await r.json();
      if(data.error) continue;
      const s=buildHist(data);
      Object.assign(histStats,s);
      loaded++;
    }catch(e){}
  }

  fill.style.width='100%';
  lbl.textContent=`Concluido: ${Object.keys(histStats).length} times carregados`;
  btn.disabled=false;
  btn.textContent=`Hist: ${Object.keys(histStats).length} times`;
  status(`Historico carregado: ${Object.keys(histStats).length} times de ${loaded}/${total} arquivos`);

  setTimeout(()=>{ prog.style.display='none'; },3000);
  if(allMatches.length) processMatches({matches:allMatches});
}
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        try:
            status = str(args[1]) if len(args) > 1 else "???"
            request = str(args[0]) if len(args) > 0 else ""
            color = "\033[92m" if status == "200" else "\033[91m"
            print(f"  {color}{status}\033[0m {request}")
        except:
            pass

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/':
            html = HTML.replace('HIST_FILES_PLACEHOLDER', json.dumps(HIST_FILES))
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif parsed.path == '/proxy':
            qs  = parse_qs(parsed.query)
            rel = qs.get('url', [''])[0]
            if not rel:
                self._err('url param missing', 400); return

            full_url = BASE + rel
            try:
                req = urllib.request.Request(full_url, headers={'User-Agent': 'BettingAnalyzer/1.0'})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except urllib.error.HTTPError as e:
                self._err(f'GitHub {e.code}: {rel}')
            except Exception as e:
                self._err(str(e))
        else:
            self.send_response(404); self.end_headers()

    def _err(self, msg, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': msg}).encode())


if __name__ == '__main__':
    try:
        # Tenta matar processos na porta 8080 antes de iniciar
        import os
        try: os.system("fuser -k 8080/tcp > /dev/null 2>&1")
        except: pass
        
        with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
            print(f"\n  \033[94mBetting Analyzer\033[0m rodando em \033[92mhttp://localhost:{PORT}\033[0m")
            print(f"  {len(HIST_FILES)} arquivos historicos configurados")
            print(f"  Ctrl+C para parar\n")
            httpd.serve_forever()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
    except KeyboardInterrupt:
        print('\n  Servidor encerrado.')