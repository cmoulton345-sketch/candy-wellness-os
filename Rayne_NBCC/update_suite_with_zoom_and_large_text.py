import os
import json

base_dir = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC"

# 1. LOAD PREVIOUS MODULES DATA
with open(os.path.join(base_dir, "build_master_study_suite.py"), "r", encoding="utf-8") as f:
    orig_code = f.read()

start_idx = orig_code.find("modules_data = [")
end_idx = orig_code.find("\n# -------------------------------------------------------------\n# STEP 1:")
modules_data_str = orig_code[start_idx + len("modules_data = "):end_idx].strip()
modules_data = json.loads(modules_data_str)

# 2. LOAD ATLAS DATA FROM update_suite_with_atlas.py
with open(os.path.join(base_dir, "update_suite_with_atlas.py"), "r", encoding="utf-8") as f:
    atlas_code = f.read()

a_start = atlas_code.find("atlas_data = [")
a_end = atlas_code.find("\n# -------------------------------------------------------------\n# 3. BUILD INTERACTIVE")
atlas_data_str = atlas_code[a_start + len("atlas_data = "):a_end].strip()
namespace = {}
exec("atlas_data = " + atlas_data_str, namespace)
atlas_data = namespace["atlas_data"]

print(f"Loaded {len(modules_data)} modules and {len(atlas_data)} atlas plates.")

# ==============================================================================
# 3. GENERATE ENHANCED PRINTABLE BLUEPRINTS & ATLAS (WITH ZOOM & GIANT WORDS)
# ==============================================================================
printable_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rayne's Printable Anatomical Atlas & Blueprints Pack (Modules 1–8)</title>
  <style>
    @page {
      size: letter portrait;
      margin: 0.35in;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0b1120;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent-cyan: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.25);
      --font-scale: 1;
    }

    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 20px;
      line-height: 1.6;
      transition: font-size 0.2s ease;
    }

    /* Font Scale Modifier Classes */
    body.scale-normal { --font-scale: 1; }
    body.scale-large  { --font-scale: 1.25; }
    body.scale-xlarge { --font-scale: 1.5; }
    body.scale-giant  { --font-scale: 1.8; }

    /* Interactive Top Control Bar */
    .no-print-bar {
      background: #1e293b;
      border: 2px solid var(--accent-cyan);
      color: #ffffff;
      padding: 18px 24px;
      border-radius: 12px;
      margin-bottom: 28px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }

    .bar-title h2 {
      font-size: 1.4rem;
      font-weight: 800;
      color: #38bdf8;
      margin-bottom: 4px;
    }

    .bar-title p {
      color: #cbd5e1;
      font-size: 0.95rem;
    }

    .bar-actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
    }

    .btn-group {
      display: flex;
      background: #0f172a;
      border-radius: 8px;
      padding: 4px;
      border: 1px solid #334155;
      gap: 4px;
    }

    .ctrl-btn {
      background: transparent;
      border: none;
      color: #cbd5e1;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .ctrl-btn:hover {
      background: #334155;
      color: #38bdf8;
    }

    .ctrl-btn.active {
      background: #38bdf8;
      color: #0f172a;
      box-shadow: 0 2px 8px rgba(56, 189, 248, 0.35);
    }

    .print-btn {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: white;
      border: none;
      padding: 10px 22px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
      transition: transform 0.2s ease;
    }

    .print-btn:hover {
      transform: translateY(-2px);
      background: linear-gradient(135deg, #38bdf8, #0284c7);
      color: #0f172a;
    }

    .help-banner {
      width: 100%;
      background: rgba(56, 189, 248, 0.1);
      border-left: 4px solid var(--accent-cyan);
      padding: 10px 14px;
      border-radius: 6px;
      margin-top: 6px;
      font-size: 0.92rem;
      color: #e0f2fe;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Page Blueprint & Atlas Card */
    .bp-page {
      background: #1e293b;
      border: 2px solid #334155;
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 38px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
      page-break-after: always;
      break-after: page;
    }

    .bp-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--accent-cyan);
      padding-bottom: 12px;
      margin-bottom: 18px;
    }

    .bp-title {
      font-size: calc(1.4rem * var(--font-scale));
      font-weight: 800;
      color: var(--accent-cyan);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .bp-badge {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid var(--accent-cyan);
      color: var(--accent-cyan);
      padding: 6px 16px;
      border-radius: 20px;
      font-size: calc(0.9rem * var(--font-scale));
      font-weight: 700;
    }

    /* Diagram Display Container */
    .bp-diagram-box {
      background: #ffffff;
      padding: 16px;
      border-radius: 10px;
      margin-bottom: 18px;
      text-align: center;
      position: relative;
      cursor: zoom-in;
      border: 2px solid #e2e8f0;
      transition: box-shadow 0.25s ease, transform 0.2s ease;
    }

    .bp-diagram-box:hover {
      box-shadow: 0 8px 24px rgba(56, 189, 248, 0.3);
      border-color: #38bdf8;
    }

    .bp-diagram-box img {
      max-width: 100%;
      height: auto;
      max-height: 560px;
      border-radius: 6px;
      display: block;
      margin: 0 auto;
      transition: all 0.3s ease;
    }

    /* Diagram Sizing Classes */
    body.diag-giant .bp-diagram-box img {
      max-height: 850px;
    }

    .zoom-hint-badge {
      position: absolute;
      bottom: 12px;
      right: 14px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(4px);
      color: #38bdf8;
      border: 1px solid #38bdf8;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 700;
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Study Cards (Parts Grid) */
    .parts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-top: 14px;
    }

    @media (max-width: 800px) {
      .parts-grid { grid-template-columns: 1fr; }
    }

    .part-pill {
      background: #0f172a;
      border: 1.5px solid #334155;
      border-left: 5px solid var(--accent-cyan);
      padding: 14px 18px;
      border-radius: 8px;
      font-size: calc(1.05rem * var(--font-scale));
      line-height: 1.6;
      cursor: pointer;
      position: relative;
      transition: all 0.22s ease;
    }

    .part-pill:hover {
      background: #1e293b;
      border-color: var(--accent-cyan);
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(56, 189, 248, 0.2);
    }

    .part-pill strong {
      color: #67e8f9;
      display: block;
      font-size: calc(1.22rem * var(--font-scale));
      margin-bottom: 4px;
      letter-spacing: 0.2px;
    }

    .part-pill .card-click-hint {
      position: absolute;
      top: 10px;
      right: 12px;
      font-size: 0.75rem;
      color: #94a3b8;
      opacity: 0.7;
    }

    .part-pill:hover .card-click-hint {
      color: #38bdf8;
      opacity: 1;
    }

    /* Modal 1: Image Zoom Lightbox */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(11, 17, 32, 0.94);
      backdrop-filter: blur(8px);
      z-index: 99999;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-header-bar {
      width: 100%;
      max-width: 1200px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e293b;
      padding: 12px 24px;
      border-radius: 12px;
      border: 1px solid #334155;
      color: white;
      gap: 16px;
      flex-wrap: wrap;
    }

    .modal-title-text {
      font-size: 1.2rem;
      font-weight: 800;
      color: #38bdf8;
    }

    .modal-zoom-controls {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .modal-ctrl-btn {
      background: #0f172a;
      border: 1px solid #38bdf8;
      color: #38bdf8;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .modal-ctrl-btn:hover {
      background: #38bdf8;
      color: #0f172a;
    }

    .modal-close-btn {
      background: #ef4444;
      border: none;
      color: white;
      padding: 6px 16px;
      border-radius: 6px;
      font-size: 1.1rem;
      font-weight: 800;
      cursor: pointer;
    }

    .modal-close-btn:hover { background: #dc2626; }

    .modal-img-viewport {
      flex: 1;
      width: 100%;
      max-width: 1200px;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
      cursor: grab;
    }

    .modal-img-viewport:active { cursor: grabbing; }

    .modal-img-viewport img {
      transition: transform 0.2s ease-out;
      transform-origin: center center;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
      background: white;
    }

    /* Modal 2: Giant Word / Study Card Lightbox */
    .word-modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(11, 17, 32, 0.88);
      backdrop-filter: blur(8px);
      z-index: 99999;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }

    .word-modal-overlay.active {
      display: flex;
    }

    .word-card-popup {
      background: #1e293b;
      border: 3px solid #38bdf8;
      border-radius: 18px;
      padding: 36px 40px;
      max-width: 820px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
      position: relative;
      animation: popIn 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    @keyframes popIn {
      from { transform: scale(0.85); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .word-modal-badge {
      display: inline-block;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 0.95rem;
      font-weight: 700;
      margin-bottom: 16px;
    }

    .word-modal-title {
      font-size: 2.3rem;
      font-weight: 800;
      color: #67e8f9;
      line-height: 1.2;
      margin-bottom: 18px;
      border-bottom: 2px solid #334155;
      padding-bottom: 12px;
    }

    .word-modal-body {
      font-size: 1.45rem;
      line-height: 1.7;
      color: #f1f5f9;
      margin-bottom: 28px;
    }

    .word-modal-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }

    .word-nav-btn {
      background: #0f172a;
      border: 2px solid #38bdf8;
      color: #38bdf8;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .word-nav-btn:hover {
      background: #38bdf8;
      color: #0f172a;
    }

    .word-counter {
      color: #94a3b8;
      font-size: 1rem;
      font-weight: 600;
    }

    /* Print Formatting Rules */
    @media print {
      body {
        background: white !important;
        color: black !important;
        padding: 0 !important;
      }

      .no-print-bar, .modal-overlay, .word-modal-overlay, .zoom-hint-badge, .card-click-hint {
        display: none !important;
      }

      .bp-page {
        background: white !important;
        color: black !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
        padding: 16px !important;
        page-break-after: always !important;
        break-after: page !important;
      }

      .bp-title-row {
        border-bottom: 2px solid #000 !important;
      }

      .bp-title {
        color: #000 !important;
        font-size: 16pt !important;
      }

      .bp-badge {
        color: #000 !important;
        border: 1.5px solid #000 !important;
        background: #f1f5f9 !important;
        font-size: 10pt !important;
      }

      .bp-diagram-box {
        background: white !important;
        border: 1.5px solid #000 !important;
        padding: 8px !important;
        margin-bottom: 12px !important;
      }

      .bp-diagram-box img {
        max-height: 600px !important;
      }

      .parts-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
      }

      .part-pill {
        background: #ffffff !important;
        color: #000 !important;
        border: 1.5px solid #000 !important;
        border-left: 5px solid #000 !important;
        padding: 10px 12px !important;
        font-size: 11pt !important;
        line-height: 1.45 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }

      .part-pill strong {
        color: #000 !important;
        font-size: 12.5pt !important;
        margin-bottom: 2px !important;
      }
    }
  </style>
</head>
<body class="scale-normal">

  <!-- Interactive Control Bar -->
  <div class="no-print-bar">
    <div class="bar-title">
      <h2>Rayne's Anatomical Atlas & Blueprint Study Pack</h2>
      <p>NBCC Practical Nursing (Modules 1–8) • Master Visual Reference for Oct 13 Exam</p>
    </div>

    <div class="bar-actions">
      <!-- Font Size Toggle -->
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="font-size:0.88rem; color:#94a3b8; font-weight:700;">TEXT SIZE:</span>
        <div class="btn-group">
          <button class="ctrl-btn active" id="btn-scale-normal" onclick="setFontScale('normal')">Aa 100%</button>
          <button class="ctrl-btn" id="btn-scale-large" onclick="setFontScale('large')">Aa+ 125%</button>
          <button class="ctrl-btn" id="btn-scale-xlarge" onclick="setFontScale('xlarge')">Aa++ 150%</button>
          <button class="ctrl-btn" id="btn-scale-giant" onclick="setFontScale('giant')">Aa+++ Giant</button>
        </div>
      </div>

      <!-- Diagram Fit Toggle -->
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="font-size:0.88rem; color:#94a3b8; font-weight:700;">PICTURES:</span>
        <div class="btn-group">
          <button class="ctrl-btn active" id="btn-diag-standard" onclick="setDiagramSize('standard')">Standard</button>
          <button class="ctrl-btn" id="btn-diag-giant" onclick="setDiagramSize('giant')">🔍 Full Expand</button>
        </div>
      </div>

      <!-- Print Button -->
      <button class="print-btn" onclick="window.print()">🖨️ Print / Save to PDF</button>
    </div>

    <div class="help-banner">
      <span>💡 <strong>Interactive Learning:</strong> Click <strong>ANY picture</strong> to zoom in full-screen (+ / - / pan labels). Click <strong>ANY study box</strong> to open it in Giant Flashcard focus!</span>
    </div>
  </div>
"""

# Append Atlas Plates
for atlas_idx, item in enumerate(atlas_data):
    p_html = ""
    for part_idx, p in enumerate(item["parts"]):
        p_html += f"""
        <div class="part-pill" onclick="openWordModal({atlas_idx}, {part_idx})">
          <span class="card-click-hint">🔍 Enlarge</span>
          <strong>{p['name']}</strong>
          {p['role']}
        </div>
        """

    secondary_img = ""
    if item["img_secondary"]:
        secondary_img = f"""
        <div class="bp-diagram-box" style="margin-top:14px;" onclick="openImageModal('{item['img_secondary']}?t=3', '{item['title']} (Secondary View)')">
          <img src="{item['img_secondary']}?t=3" alt="{item['title']} Secondary View">
          <div class="zoom-hint-badge">🔍 Click to Zoom In Full-Screen</div>
        </div>
        """

    printable_html += f"""
  <div class="bp-page" id="plate-{item['id']}">
    <div class="bp-title-row">
      <div class="bp-title">ATLAS: {item['title']}</div>
      <div class="bp-badge">{item['system']}</div>
    </div>
    
    <div class="bp-diagram-box" onclick="openImageModal('{item['img']}?t=3', '{item['title']}')">
      <img src="{item['img']}?t=3" alt="{item['title']}">
      <div class="zoom-hint-badge">🔍 Click to Zoom In Full-Screen</div>
    </div>
    
    {secondary_img}

    <div class="parts-grid">
      {p_html}
    </div>
  </div>
"""

# Append Concept Blueprints
for mod in modules_data:
    printable_html += f"""
  <div class="bp-page" id="blueprint-mod-{mod['mod_num']}">
    <div class="bp-title-row">
      <div class="bp-title">BLUEPRINT: {mod['title']}</div>
      <div class="bp-badge">{mod['chapter']}</div>
    </div>
    <div class="bp-diagram-box" onclick="openImageModal('{mod['diagram']}?t=3', '{mod['title']}')">
      <img src="{mod['diagram']}?t=3" alt="{mod['title']}">
      <div class="zoom-hint-badge">🔍 Click to Zoom In Full-Screen</div>
    </div>
    <div class="part-pill" style="cursor:default; border-left:5px solid var(--accent-cyan); font-size:calc(1.1rem * var(--font-scale));">
      <strong>Core Nursing Focus:</strong> {mod['summary']}
    </div>
  </div>
"""

# Modals & Client-side Script
printable_html += f"""
  <!-- Modal 1: Image Zoom Lightbox -->
  <div class="modal-overlay" id="imageModal" onclick="closeImageModalOnBackdrop(event)">
    <div class="modal-header-bar">
      <span class="modal-title-text" id="modalImageTitle">Anatomical Diagram Zoom</span>
      <div class="modal-zoom-controls">
        <button class="modal-ctrl-btn" onclick="zoomImage(-0.25)">➖ Zoom Out</button>
        <button class="modal-ctrl-btn" onclick="resetImageZoom()">↺ 100%</button>
        <button class="modal-ctrl-btn" onclick="zoomImage(0.25)">➕ Zoom In</button>
        <button class="modal-ctrl-btn" onclick="toggleFitScreen()">↔ Fit Screen</button>
        <button class="modal-close-btn" onclick="closeImageModal()">✕ Close</button>
      </div>
    </div>
    <div class="modal-img-viewport" id="modalViewport">
      <img src="" id="modalImg" alt="Enlarged Diagram">
    </div>
  </div>

  <!-- Modal 2: Giant Word / Flashcard Modal -->
  <div class="word-modal-overlay" id="wordModal" onclick="closeWordModalOnBackdrop(event)">
    <div class="word-card-popup" onclick="event.stopPropagation()">
      <div class="word-modal-badge" id="wmBadge">System Badge</div>
      <div class="word-modal-title" id="wmTitle">Anatomical Structure</div>
      <div class="word-modal-body" id="wmBody">Physiological role and nursing exam rationale...</div>
      <div class="word-modal-nav">
        <button class="word-nav-btn" onclick="prevWord()">◀ Previous</button>
        <span class="word-counter" id="wmCounter">Part 1 of 12</span>
        <button class="word-nav-btn" onclick="nextWord()">Next ▶</button>
        <button class="modal-close-btn" style="padding:10px 20px;" onclick="closeWordModal()">✕ Close</button>
      </div>
    </div>
  </div>

  <script>
    // Atlas Data Injection for Interactive Flashcards
    const atlasData = {json.dumps(atlas_data)};

    let currentScale = 'normal';
    function setFontScale(scale) {{
      currentScale = scale;
      document.body.className = document.body.className.replace(/scale-\\w+/g, '') + ' scale-' + scale;
      
      document.querySelectorAll('[id^="btn-scale-"]').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('btn-scale-' + scale);
      if (activeBtn) activeBtn.classList.add('active');
    }}

    function setDiagramSize(size) {{
      if (size === 'giant') {{
        document.body.classList.add('diag-giant');
        document.getElementById('btn-diag-giant').classList.add('active');
        document.getElementById('btn-diag-standard').classList.remove('active');
      }} else {{
        document.body.classList.remove('diag-giant');
        document.getElementById('btn-diag-giant').classList.remove('active');
        document.getElementById('btn-diag-standard').classList.add('active');
      }}
    }}

    // 1. IMAGE LIGHTBOX MODAL
    let currentImgZoom = 1;
    function openImageModal(imgSrc, title) {{
      const modal = document.getElementById('imageModal');
      const modalImg = document.getElementById('modalImg');
      const titleEl = document.getElementById('modalImageTitle');

      modalImg.src = imgSrc;
      titleEl.innerText = title;
      currentImgZoom = 1;
      modalImg.style.transform = `scale(${{currentImgZoom}})`;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeImageModal() {{
      const modal = document.getElementById('imageModal');
      modal.classList.remove('active');
      document.body.style.overflow = 'auto';
    }}

    function closeImageModalOnBackdrop(e) {{
      if (e.target.id === 'imageModal' || e.target.id === 'modalViewport') {{
        closeImageModal();
      }}
    }}

    function zoomImage(delta) {{
      currentImgZoom = Math.max(0.5, Math.min(3.5, currentImgZoom + delta));
      document.getElementById('modalImg').style.transform = `scale(${{currentImgZoom}})`;
    }}

    function resetImageZoom() {{
      currentImgZoom = 1;
      document.getElementById('modalImg').style.transform = `scale(1)`;
    }}

    function toggleFitScreen() {{
      const img = document.getElementById('modalImg');
      if (currentImgZoom !== 1) {{
        currentImgZoom = 1;
      }} else {{
        currentImgZoom = 1.4;
      }}
      img.style.transform = `scale(${{currentImgZoom}})`;
    }}

    // Mouse wheel zoom inside modal
    document.getElementById('modalViewport').addEventListener('wheel', function(e) {{
      e.preventDefault();
      if (e.deltaY < 0) {{
        zoomImage(0.15);
      }} else {{
        zoomImage(-0.15);
      }}
    }}, {{ passive: false }});

    // 2. GIANT WORD / CARD MODAL
    let activeAtlasIdx = 0;
    let activePartIdx = 0;

    function openWordModal(atlasIdx, partIdx) {{
      activeAtlasIdx = atlasIdx;
      activePartIdx = partIdx;
      renderWordModal();
      document.getElementById('wordModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function renderWordModal() {{
      const item = atlasData[activeAtlasIdx];
      const part = item.parts[activePartIdx];
      
      document.getElementById('wmBadge').innerText = `${{item.system}} • Plate ${{activeAtlasIdx + 1}}`;
      document.getElementById('wmTitle').innerText = part.name;
      document.getElementById('wmBody').innerText = part.role;
      document.getElementById('wmCounter').innerText = `Structure ${{activePartIdx + 1}} of ${{item.parts.length}}`;
    }}

    function closeWordModal() {{
      document.getElementById('wordModal').classList.remove('active');
      document.body.style.overflow = 'auto';
    }}

    function closeWordModalOnBackdrop(e) {{
      if (e.target.id === 'wordModal') {{
        closeWordModal();
      }}
    }}

    function nextWord() {{
      const item = atlasData[activeAtlasIdx];
      if (activePartIdx < item.parts.length - 1) {{
        activePartIdx++;
      }} else {{
        activePartIdx = 0; // loop
      }}
      renderWordModal();
    }}

    function prevWord() {{
      const item = atlasData[activeAtlasIdx];
      if (activePartIdx > 0) {{
        activePartIdx--;
      }} else {{
        activePartIdx = item.parts.length - 1; // loop
      }}
      renderWordModal();
    }}

    // Keyboard support
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') {{
        closeImageModal();
        closeWordModal();
      }} else if (document.getElementById('wordModal').classList.contains('active')) {{
        if (e.key === 'ArrowRight') nextWord();
        if (e.key === 'ArrowLeft') prevWord();
      }}
    }});
  </script>
</body>
</html>
"""

# Write to printable HTML
with open(os.path.join(base_dir, "Rayne_AP_Master_Blueprints_Printable_Modules_1_8.html"), "w", encoding="utf-8") as f:
    f.write(printable_html)

print("Generated enhanced Rayne_AP_Master_Blueprints_Printable_Modules_1_8.html with Interactive Zoom & Giant Words!")

# ==============================================================================
# 4. ALSO ENHANCE RAYNE_AP_MASTER_STUDY_HUB_MODULES_1_8.HTML WITH SAME ZOOM & MODALS
# ==============================================================================
# Read existing Study Hub
with open(os.path.join(base_dir, "Rayne_AP_Master_Study_Hub_Modules_1_8.html"), "r", encoding="utf-8") as f:
    hub_content = f.read()

# Enhance CSS with font scales and lightbox modals if not present
if "imageModal" not in hub_content:
    # Inject modals into Study Hub before </body>
    hub_modal_injection = f"""
  <!-- Modal 1: Image Zoom Lightbox -->
  <div class="modal-overlay" id="imageModal" onclick="closeImageModalOnBackdrop(event)">
    <div class="modal-header-bar">
      <span class="modal-title-text" id="modalImageTitle">Anatomical Diagram Zoom</span>
      <div class="modal-zoom-controls">
        <button class="modal-ctrl-btn" onclick="zoomImage(-0.25)">➖ Zoom Out</button>
        <button class="modal-ctrl-btn" onclick="resetImageZoom()">↺ 100%</button>
        <button class="modal-ctrl-btn" onclick="zoomImage(0.25)">➕ Zoom In</button>
        <button class="modal-ctrl-btn" onclick="toggleFitScreen()">↔ Fit Screen</button>
        <button class="modal-close-btn" onclick="closeImageModal()">✕ Close</button>
      </div>
    </div>
    <div class="modal-img-viewport" id="modalViewport">
      <img src="" id="modalImg" alt="Enlarged Diagram">
    </div>
  </div>

  <!-- Modal 2: Giant Word / Flashcard Modal -->
  <div class="word-modal-overlay" id="wordModal" onclick="closeWordModalOnBackdrop(event)">
    <div class="word-card-popup" onclick="event.stopPropagation()">
      <div class="word-modal-badge" id="wmBadge">System Badge</div>
      <div class="word-modal-title" id="wmTitle">Anatomical Structure</div>
      <div class="word-modal-body" id="wmBody">Physiological role and nursing exam rationale...</div>
      <div class="word-modal-nav">
        <button class="word-nav-btn" onclick="prevWord()">◀ Previous</button>
        <span class="word-counter" id="wmCounter">Part 1 of 12</span>
        <button class="word-nav-btn" onclick="nextWord()">Next ▶</button>
        <button class="modal-close-btn" style="padding:10px 20px;" onclick="closeWordModal()">✕ Close</button>
      </div>
    </div>
  </div>

  <style>
    /* Modal 1: Image Zoom Lightbox */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(11, 17, 32, 0.94);
      backdrop-filter: blur(8px);
      z-index: 99999;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
    }}
    .modal-overlay.active {{ display: flex; }}
    .modal-header-bar {{
      width: 100%;
      max-width: 1200px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e293b;
      padding: 12px 24px;
      border-radius: 12px;
      border: 1px solid #334155;
      color: white;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .modal-title-text {{
      font-size: 1.2rem;
      font-weight: 800;
      color: #38bdf8;
    }}
    .modal-zoom-controls {{ display: flex; gap: 8px; align-items: center; }}
    .modal-ctrl-btn {{
      background: #0f172a;
      border: 1px solid #38bdf8;
      color: #38bdf8;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .modal-ctrl-btn:hover {{ background: #38bdf8; color: #0f172a; }}
    .modal-close-btn {{
      background: #ef4444;
      border: none;
      color: white;
      padding: 6px 16px;
      border-radius: 6px;
      font-size: 1.1rem;
      font-weight: 800;
      cursor: pointer;
    }}
    .modal-close-btn:hover {{ background: #dc2626; }}
    .modal-img-viewport {{
      flex: 1;
      width: 100%;
      max-width: 1200px;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
      cursor: grab;
    }}
    .modal-img-viewport:active {{ cursor: grabbing; }}
    .modal-img-viewport img {{
      transition: transform 0.2s ease-out;
      transform-origin: center center;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
      background: white;
    }}

    /* Modal 2: Giant Word / Study Card Lightbox */
    .word-modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(11, 17, 32, 0.88);
      backdrop-filter: blur(8px);
      z-index: 99999;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }}
    .word-modal-overlay.active {{ display: flex; }}
    .word-card-popup {{
      background: #1e293b;
      border: 3px solid #38bdf8;
      border-radius: 18px;
      padding: 36px 40px;
      max-width: 820px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
      position: relative;
    }}
    .word-modal-badge {{
      display: inline-block;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 0.95rem;
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .word-modal-title {{
      font-size: 2.3rem;
      font-weight: 800;
      color: #67e8f9;
      line-height: 1.2;
      margin-bottom: 18px;
      border-bottom: 2px solid #334155;
      padding-bottom: 12px;
    }}
    .word-modal-body {{
      font-size: 1.45rem;
      line-height: 1.7;
      color: #f1f5f9;
      margin-bottom: 28px;
    }}
    .word-modal-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }}
    .word-nav-btn {{
      background: #0f172a;
      border: 2px solid #38bdf8;
      color: #38bdf8;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .word-nav-btn:hover {{ background: #38bdf8; color: #0f172a; }}
    .word-counter {{ color: #94a3b8; font-size: 1rem; font-weight: 600; }}

    /* Atlas Image Hover */
    .atlas-img-box, .bp-img-box {{
      position: relative;
      cursor: zoom-in;
    }}
    .parts-table tr {{
      cursor: pointer;
      transition: background 0.15s ease;
    }}
    .parts-table tr:hover {{
      background: #253349 !important;
    }}
  </style>

  <script>
    // Lightbox and Word Zoom Scripts
    let currentImgZoom = 1;
    function openImageModal(imgSrc, title) {{
      const modal = document.getElementById('imageModal');
      const modalImg = document.getElementById('modalImg');
      const titleEl = document.getElementById('modalImageTitle');
      modalImg.src = imgSrc;
      titleEl.innerText = title;
      currentImgZoom = 1;
      modalImg.style.transform = `scale(${{currentImgZoom}})`;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeImageModal() {{
      const modal = document.getElementById('imageModal');
      modal.classList.remove('active');
      document.body.style.overflow = 'auto';
    }}

    function closeImageModalOnBackdrop(e) {{
      if (e.target.id === 'imageModal' || e.target.id === 'modalViewport') {{
        closeImageModal();
      }}
    }}

    function zoomImage(delta) {{
      currentImgZoom = Math.max(0.5, Math.min(3.5, currentImgZoom + delta));
      document.getElementById('modalImg').style.transform = `scale(${{currentImgZoom}})`;
    }}

    function resetImageZoom() {{
      currentImgZoom = 1;
      document.getElementById('modalImg').style.transform = `scale(1)`;
    }}

    function toggleFitScreen() {{
      currentImgZoom = (currentImgZoom !== 1) ? 1 : 1.4;
      document.getElementById('modalImg').style.transform = `scale(${{currentImgZoom}})`;
    }}

    // Giant Word Modal
    let activeAtlasIdx = 0;
    let activePartIdx = 0;
    function openWordModal(atlasIdx, partIdx) {{
      activeAtlasIdx = atlasIdx;
      activePartIdx = partIdx;
      renderWordModal();
      document.getElementById('wordModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function renderWordModal() {{
      const item = atlasData[activeAtlasIdx];
      const part = item.parts[activePartIdx];
      document.getElementById('wmBadge').innerText = `${{item.system}} • Plate ${{activeAtlasIdx + 1}}`;
      document.getElementById('wmTitle').innerText = part.name;
      document.getElementById('wmBody').innerText = part.role;
      document.getElementById('wmCounter').innerText = `Structure ${{activePartIdx + 1}} of ${{item.parts.length}}`;
    }}

    function closeWordModal() {{
      document.getElementById('wordModal').classList.remove('active');
      document.body.style.overflow = 'auto';
    }}

    function closeWordModalOnBackdrop(e) {{
      if (e.target.id === 'wordModal') {{
        closeWordModal();
      }}
    }}

    function nextWord() {{
      const item = atlasData[activeAtlasIdx];
      activePartIdx = (activePartIdx < item.parts.length - 1) ? activePartIdx + 1 : 0;
      renderWordModal();
    }}

    function prevWord() {{
      const item = atlasData[activeAtlasIdx];
      activePartIdx = (activePartIdx > 0) ? activePartIdx - 1 : item.parts.length - 1;
      renderWordModal();
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') {{
        closeImageModal();
        closeWordModal();
      }} else if (document.getElementById('wordModal').classList.contains('active')) {{
        if (e.key === 'ArrowRight') nextWord();
        if (e.key === 'ArrowLeft') prevWord();
      }}
    }});
  </script>
</body>
"""
    hub_content = hub_content.replace("</body>", hub_modal_injection)

# Also ensure renderAtlas wires openImageModal and openWordModal in Study Hub
old_render_atlas = """        card.innerHTML = `
          <div class="atlas-header">
            <span class="atlas-title">${item.title}</span>
            <span class="atlas-badge">${item.system}</span>
          </div>
          <div class="atlas-img-box">
            <img src="${item.img}?t=3" alt="${item.title}">
            ${secondaryImgHtml}
          </div>
          <div class="atlas-body">
            <p><strong>Description:</strong> ${item.description}</p>
            <h4 style="color:#38bdf8; margin-top:14px; margin-bottom:6px; font-size:1rem;">📌 Key Labeled Structures & Functions to Memorize:</h4>
            <table class="parts-table">
              <thead>
                <tr>
                  <th>Anatomical Structure</th>
                  <th>Function & Exam Key</th>
                </tr>
              </thead>
              <tbody>
                ${rows}
              </tbody>
            </table>
          </div>
        `;"""

new_render_atlas = """        card.innerHTML = `
          <div class="atlas-header">
            <span class="atlas-title">${item.title}</span>
            <span class="atlas-badge">${item.system}</span>
          </div>
          <div class="atlas-img-box" onclick="openImageModal('${item.img}?t=3', '${item.title}')">
            <img src="${item.img}?t=3" alt="${item.title}">
            <div style="font-size:0.82rem; color:#0284c7; margin-top:6px; font-weight:700;">🔍 Click picture to zoom in full-screen</div>
            ${secondaryImgHtml}
          </div>
          <div class="atlas-body">
            <p><strong>Description:</strong> ${item.description}</p>
            <h4 style="color:#38bdf8; margin-top:14px; margin-bottom:6px; font-size:1rem;">📌 Key Labeled Structures & Functions to Memorize (Click row to enlarge):</h4>
            <table class="parts-table">
              <thead>
                <tr>
                  <th>Anatomical Structure</th>
                  <th>Function & Exam Key</th>
                </tr>
              </thead>
              <tbody>
                ${rows}
              </tbody>
            </table>
          </div>
        `;"""

if old_render_atlas in hub_content:
    hub_content = hub_content.replace(old_render_atlas, new_render_atlas)

with open(os.path.join(base_dir, "Rayne_AP_Master_Study_Hub_Modules_1_8.html"), "w", encoding="utf-8") as f:
    f.write(hub_content)

print("Updated Rayne_AP_Master_Study_Hub_Modules_1_8.html with Lightbox Zoom & Word modals!")
