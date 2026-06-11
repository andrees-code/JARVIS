# JARVIS


PLAN de como se ha planteado el proyecto (el plan esta hecho en formato html):
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS — Plan de construcción</title>
<style>
  :root {
    --bg:       #0a0c10;
    --bg2:      #0f1218;
    --bg3:      #141820;
    --border:   #1e2530;
    --border2:  #2a3340;
    --cyan:     #00d4ff;
    --cyan-dim: #00d4ff22;
    --cyan-mid: #00d4ff55;
    --text:     #c8d4e0;
    --text-dim: #6a7a8a;
    --text-hi:  #eaf2f8;
    --green:    #4ade80;
    --amber:    #fbbf24;
    --coral:    #f87171;
    --mono:     'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    --sans:     'Inter', 'Segoe UI', system-ui, sans-serif;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.7;
    min-height: 100vh;
  }

  /* ── NAV ── */
  nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    background: rgba(10,12,16,0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .nav-logo {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--cyan);
    letter-spacing: 0.1em;
    text-decoration: none;
  }
  .nav-links {
    display: flex;
    gap: 1.5rem;
    list-style: none;
  }
  .nav-links a {
    font-size: 12px;
    color: var(--text-dim);
    text-decoration: none;
    letter-spacing: 0.05em;
    transition: color 0.2s;
  }
  .nav-links a:hover { color: var(--cyan); }

  /* ── HERO ── */
  .hero {
    padding: 9rem 2rem 5rem;
    max-width: 860px;
    margin: 0 auto;
  }
  .hero-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--cyan);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .hero-eyebrow::before {
    content: '';
    display: block;
    width: 28px;
    height: 1px;
    background: var(--cyan);
  }
  .hero h1 {
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 700;
    color: var(--text-hi);
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
  }
  .hero h1 span {
    color: var(--cyan);
  }
  .typewriter-wrap {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--text-dim);
    margin-bottom: 2rem;
    min-height: 22px;
  }
  .typewriter-wrap span {
    color: var(--cyan);
    border-right: 2px solid var(--cyan);
    padding-right: 2px;
    animation: blink 1s step-end infinite;
  }
  @keyframes blink { 0%,100%{border-color:var(--cyan)} 50%{border-color:transparent} }

  .hero-desc {
    font-size: 16px;
    color: var(--text);
    max-width: 580px;
    margin-bottom: 2.5rem;
    line-height: 1.75;
  }

  .stat-row {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }
  .stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .stat-num {
    font-family: var(--mono);
    font-size: 22px;
    color: var(--text-hi);
    font-weight: 600;
  }
  .stat-label {
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── SECTION TITLES ── */
  section { max-width: 860px; margin: 0 auto; padding: 3rem 2rem; }
  .section-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2.5rem;
  }
  .section-head h2 {
    font-size: 13px;
    font-family: var(--mono);
    color: var(--cyan);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 400;
  }
  .section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ── ARCHITECTURE ── */
  .arch-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }
  .arch-cell {
    background: var(--bg2);
    padding: 1.25rem;
    transition: background 0.2s;
  }
  .arch-cell:hover { background: var(--bg3); }
  .arch-cell-icon {
    font-size: 22px;
    margin-bottom: 0.5rem;
  }
  .arch-cell-name {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--cyan);
    margin-bottom: 3px;
  }
  .arch-cell-lib {
    font-size: 12px;
    color: var(--text-dim);
  }

  .flow-row {
    display: flex;
    align-items: center;
    gap: 0;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow-x: auto;
    padding: 1.25rem 1.5rem;
  }
  .flow-step {
    display: flex;
    align-items: center;
    gap: 0;
    flex-shrink: 0;
  }
  .flow-box {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 6px;
    padding: 6px 14px;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text);
    white-space: nowrap;
  }
  .flow-box.hi {
    border-color: var(--cyan-mid);
    color: var(--cyan);
    background: var(--cyan-dim);
  }
  .flow-arrow {
    color: var(--text-dim);
    font-size: 16px;
    padding: 0 8px;
    flex-shrink: 0;
  }

  /* ── TIMELINE ── */
  .timeline { position: relative; padding-left: 2rem; }
  .timeline::before {
    content: '';
    position: absolute;
    left: 7px;
    top: 8px;
    bottom: 8px;
    width: 1px;
    background: linear-gradient(to bottom, var(--cyan), var(--border) 80%);
  }

  .week-item {
    position: relative;
    margin-bottom: 2.5rem;
  }
  .week-item:last-child { margin-bottom: 0; }

  .week-dot {
    position: absolute;
    left: -2rem;
    top: 10px;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: var(--bg);
    border: 2px solid var(--cyan);
    box-shadow: 0 0 8px var(--cyan-mid);
    transition: box-shadow 0.3s;
  }
  .week-item:hover .week-dot {
    box-shadow: 0 0 16px var(--cyan-mid), 0 0 4px var(--cyan);
  }

  .week-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s;
  }
  .week-card:hover { border-color: var(--border2); }

  .week-toggle {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.1rem 1.25rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    color: inherit;
  }
  .week-badge {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 4px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .badge-blue  { background: rgba(0,212,255,0.12); color: var(--cyan); border: 1px solid rgba(0,212,255,0.25); }
  .badge-green { background: rgba(74,222,128,0.10); color: var(--green); border: 1px solid rgba(74,222,128,0.25); }
  .badge-amber { background: rgba(251,191,36,0.10); color: var(--amber); border: 1px solid rgba(251,191,36,0.25); }
  .badge-coral { background: rgba(248,113,113,0.10); color: var(--coral); border: 1px solid rgba(248,113,113,0.25); }

  .week-titles { flex: 1; }
  .week-title { font-size: 15px; font-weight: 600; color: var(--text-hi); }
  .week-sub { font-size: 12px; color: var(--text-dim); margin-top: 1px; }
  .week-chevron {
    color: var(--text-dim);
    font-size: 18px;
    transition: transform 0.25s;
    flex-shrink: 0;
  }
  .week-item.open .week-chevron { transform: rotate(180deg); }

  .week-body {
    display: none;
    padding: 0 1.25rem 1.25rem;
    border-top: 1px solid var(--border);
  }
  .week-item.open .week-body { display: block; }

  .week-desc {
    font-size: 14px;
    color: var(--text);
    margin: 1rem 0 1.25rem;
    line-height: 1.75;
  }

  /* libs */
  .libs {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 1.25rem;
  }
  .lib-tag {
    font-family: var(--mono);
    font-size: 11px;
    background: var(--bg3);
    border: 1px solid var(--border2);
    color: var(--text-dim);
    padding: 3px 10px;
    border-radius: 4px;
  }

  /* tasks */
  .tasks { list-style: none; margin-bottom: 1.25rem; }
  .tasks li {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    font-size: 13px;
    color: var(--text);
    padding: 5px 0;
    border-bottom: 1px solid var(--border);
    line-height: 1.55;
  }
  .tasks li:last-child { border-bottom: none; }
  .task-check {
    font-size: 14px;
    color: var(--cyan);
    flex-shrink: 0;
    margin-top: 1px;
  }

  /* code */
  .code-block {
    background: #070a0e;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow-x: auto;
  }
  .code-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-bottom: 1px solid var(--border);
  }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-r { background: #ff5f56; }
  .dot-y { background: #ffbd2e; }
  .dot-g { background: #27c93f; }
  .code-filename {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
    margin-left: 4px;
  }
  .code-block pre {
    padding: 1rem 1.25rem;
    font-family: var(--mono);
    font-size: 12px;
    color: #a8b8c8;
    line-height: 1.75;
    white-space: pre;
  }
  .kw  { color: #c792ea; }
  .fn  { color: #82aaff; }
  .cm  { color: #4a5568; font-style: italic; }
  .st  { color: #c3e88d; }
  .nm  { color: #f78c6c; }
  .cy  { color: var(--cyan); }

  /* ── PLUGINS GRID ── */
  .plugins-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 10px;
  }
  .plugin-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    transition: border-color 0.2s, background 0.2s;
  }
  .plugin-card:hover { border-color: var(--border2); background: var(--bg3); }
  .plugin-icon { font-size: 20px; margin-bottom: 6px; }
  .plugin-name {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--cyan);
    margin-bottom: 3px;
  }
  .plugin-desc { font-size: 12px; color: var(--text-dim); }

  /* ── STACK TABLE ── */
  .stack-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  .stack-table th {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    text-align: left;
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    font-weight: 400;
  }
  .stack-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  .stack-table tr:last-child td { border-bottom: none; }
  .stack-table tr:hover td { background: var(--bg2); }
  .pkg-name {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--cyan);
  }

  /* ── INSTALL BLOCK ── */
  .install-block {
    background: #070a0e;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }
  .install-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
  }
  .install-label {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
  }
  .copy-btn {
    background: none;
    border: 1px solid var(--border2);
    color: var(--text-dim);
    font-size: 11px;
    font-family: var(--mono);
    padding: 3px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: color 0.2s, border-color 0.2s;
  }
  .copy-btn:hover { color: var(--cyan); border-color: var(--cyan-mid); }
  .install-block pre {
    padding: 1.2rem 1.5rem;
    font-family: var(--mono);
    font-size: 12.5px;
    color: #a8b8c8;
    line-height: 1.9;
    white-space: pre-wrap;
    overflow-x: auto;
  }
  .install-block .kw { color: var(--cyan); }

  /* ── FOOTER ── */
  footer {
    border-top: 1px solid var(--border);
    padding: 2rem;
    text-align: center;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.08em;
  }

  /* ── RESPONSIVE ── */
  @media (max-width: 600px) {
    nav { padding: 0 1rem; }
    .nav-links { display: none; }
    .hero { padding: 7rem 1.25rem 3rem; }
    section { padding: 2rem 1.25rem; }
    .stat-row { gap: 1.5rem; }
    .flow-row { padding: 1rem; }
    .hero h1 { font-size: 2rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .typewriter-wrap span { animation: none; border-color: var(--cyan); }
    * { transition-duration: 0ms !important; }
  }
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <a class="nav-logo" href="#">J.A.R.V.I.S</a>
  <ul class="nav-links">
    <li><a href="#arquitectura">Arquitectura</a></li>
    <li><a href="#plan">Plan semanal</a></li>
    <li><a href="#plugins">Plugins</a></li>
    <li><a href="#stack">Stack</a></li>
  </ul>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-eyebrow">Sistema de asistente personal</div>
  <h1>Construye tu propio<br><span>JARVIS</span></h1>
  <div class="typewriter-wrap" id="typewriter"><span id="tw-text"></span></div>
  <p class="hero-desc">
    Un asistente de voz modular para uso personal. Wake word local, LLM offline con Ollama,
    plugins independientes de ~30 líneas cada uno. Añadir nueva funcionalidad = 1 archivo, 15 minutos.
    La complejidad escala linealmente, no exponencialmente.
  </p>
  <div class="stat-row">
    <div class="stat"><span class="stat-num">6</span><span class="stat-label">Semanas al MVP</span></div>
    <div class="stat"><span class="stat-num">~80</span><span class="stat-label">Líneas del engine</span></div>
    <div class="stat"><span class="stat-num">~30</span><span class="stat-label">Líneas por plugin</span></div>
    <div class="stat"><span class="stat-num">100%</span><span class="stat-label">Local / offline</span></div>
  </div>
</div>

<!-- ARQUITECTURA -->
<section id="arquitectura">
  <div class="section-head"><h2>Arquitectura del engine</h2></div>

  <div class="arch-grid" style="margin-bottom:1.5rem">
    <div class="arch-cell">
      <div class="arch-cell-icon">🎙️</div>
      <div class="arch-cell-name">VoiceListener</div>
      <div class="arch-cell-lib">pvporcupine + whisper.cpp</div>
    </div>
    <div class="arch-cell">
      <div class="arch-cell-icon">🧠</div>
      <div class="arch-cell-name">Brain</div>
      <div class="arch-cell-lib">Ollama — qwen3:14b</div>
    </div>
    <div class="arch-cell">
      <div class="arch-cell-icon">🔀</div>
      <div class="arch-cell-name">PluginRegistry</div>
      <div class="arch-cell-lib">ChromaDB + auto_discover</div>
    </div>
    <div class="arch-cell">
      <div class="arch-cell-icon">🔊</div>
      <div class="arch-cell-name">Speaker</div>
      <div class="arch-cell-lib">pyttsx3 / coqui-tts</div>
    </div>
    <div class="arch-cell">
      <div class="arch-cell-icon">💾</div>
      <div class="arch-cell-name">Memory</div>
      <div class="arch-cell-lib">SQLite — últimas N turns</div>
    </div>
    <div class="arch-cell">
      <div class="arch-cell-icon">🖥️</div>
      <div class="arch-cell-name">Overlay UI</div>
      <div class="arch-cell-lib">customtkinter</div>
    </div>
  </div>

  <div class="flow-row">
    <div class="flow-step">
      <div class="flow-box hi">wake word</div>
      <div class="flow-arrow">→</div>
    </div>
    <div class="flow-step">
      <div class="flow-box">STT</div>
      <div class="flow-arrow">→</div>
    </div>
    <div class="flow-step">
      <div class="flow-box hi">LLM decide</div>
      <div class="flow-arrow">→</div>
    </div>
    <div class="flow-step">
      <div class="flow-box">plugin.execute()</div>
      <div class="flow-arrow">→</div>
    </div>
    <div class="flow-step">
      <div class="flow-box hi">respuesta</div>
      <div class="flow-arrow">→</div>
    </div>
    <div class="flow-step">
      <div class="flow-box">TTS</div>
    </div>
  </div>

  <div style="margin-top:1.5rem">
    <div class="code-block">
      <div class="code-header">
        <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
        <span class="code-filename">core/engine.py</span>
      </div>
      <pre><span class="kw">class</span> <span class="fn">Jarvis</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self):
        self.listener = <span class="fn">VoiceListener</span>(wake_word=<span class="st">"jarvis"</span>)
        self.speaker  = <span class="fn">Speaker</span>()
        self.brain    = <span class="fn">Brain</span>(model=<span class="st">"qwen3:14b"</span>)
        self.plugins  = <span class="fn">PluginRegistry</span>.auto_discover(<span class="st">"./plugins"</span>)

    <span class="kw">async def</span> <span class="fn">run</span>(self):
        <span class="kw">while</span> <span class="nm">True</span>:
            text      = <span class="kw">await</span> self.listener.<span class="fn">listen</span>()           <span class="cm"># 1. Escucha</span>
            tool_call = <span class="kw">await</span> self.brain.<span class="fn">decide</span>(               <span class="cm"># 2. Decide</span>
                            text, self.plugins.<span class="fn">relevant_for</span>(text))
            result    = <span class="kw">await</span> self.plugins.<span class="fn">execute</span>(tool_call)  <span class="cm"># 3. Ejecuta</span>
            response  = <span class="kw">await</span> self.brain.<span class="fn">respond</span>(result)      <span class="cm"># 4. Formula</span>
            <span class="kw">await</span> self.speaker.<span class="fn">say</span>(response)                  <span class="cm"># 5. Habla</span></pre>
    </div>
  </div>
</section>

<!-- PLAN SEMANAL -->
<section id="plan">
  <div class="section-head"><h2>Plan semanal</h2></div>

  <div class="timeline">

    <!-- SEMANA 1-2 -->
    <div class="week-item" id="w1">
      <div class="week-dot"></div>
      <div class="week-card">
        <button class="week-toggle" onclick="toggleWeek('w1')" aria-expanded="false">
          <span class="week-badge badge-blue">Semanas 1–2</span>
          <div class="week-titles">
            <div class="week-title">Core mínimo funcional</div>
            <div class="week-sub">Wake word → STT → Ollama → TTS</div>
          </div>
          <span class="week-chevron">⌄</span>
        </button>
        <div class="week-body">
          <p class="week-desc">El MVP: Jarvis escucha su nombre, transcribe lo que dices, consulta un LLM local y responde con voz. Sin herramientas aún. Solo conversación pura. ~80 líneas de Python.</p>
          <div class="libs">
            <span class="lib-tag">pvporcupine</span>
            <span class="lib-tag">whisper.cpp</span>
            <span class="lib-tag">ollama-python</span>
            <span class="lib-tag">pyttsx3</span>
            <span class="lib-tag">asyncio</span>
          </div>
          <ul class="tasks">
            <li><span class="task-check">○</span> Instalar Ollama con qwen3:14b o llama3.2:3b</li>
            <li><span class="task-check">○</span> Implementar VoiceListener con pvporcupine para "jarvis"</li>
            <li><span class="task-check">○</span> Conectar Whisper para transcripción offline</li>
            <li><span class="task-check">○</span> Loop principal async: escucha → transcribe → pregunta → responde</li>
            <li><span class="task-check">○</span> Test: conversación básica funciona en &lt;3s latencia</li>
          </ul>
          <div class="code-block">
            <div class="code-header">
              <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
              <span class="code-filename">core/engine.py — 80 líneas</span>
            </div>
            <pre><span class="kw">async def</span> <span class="fn">run</span>(self):
    <span class="kw">while</span> <span class="nm">True</span>:
        text  = <span class="kw">await</span> self.listener.<span class="fn">listen</span>()  <span class="cm"># wake word + STT</span>
        reply = <span class="kw">await</span> self.brain.<span class="fn">chat</span>(text)    <span class="cm"># Ollama local</span>
        <span class="kw">await</span> self.speaker.<span class="fn">say</span>(reply)          <span class="cm"># TTS</span></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- SEMANA 3 -->
    <div class="week-item" id="w2">
      <div class="week-dot"></div>
      <div class="week-card">
        <button class="week-toggle" onclick="toggleWeek('w2')" aria-expanded="false">
          <span class="week-badge badge-green">Semana 3</span>
          <div class="week-titles">
            <div class="week-title">Sistema de plugins + primeras tools</div>
            <div class="week-sub">3 plugins demo: sistema, archivos, navegador</div>
          </div>
          <span class="week-chevron">⌄</span>
        </button>
        <div class="week-body">
          <p class="week-desc">Añades el enrutador de herramientas: la IA lee los dicts TOOL y decide qué función ejecutar. Cada plugin es un archivo de ~30 líneas con un dict TOOL y una función execute().</p>
          <div class="libs">
            <span class="lib-tag">pyautogui</span>
            <span class="lib-tag">pathlib</span>
            <span class="lib-tag">playwright</span>
            <span class="lib-tag">screen-brightness-control</span>
          </div>
          <ul class="tasks">
            <li><span class="task-check">○</span> Crear PluginRegistry con auto_discover('./plugins')</li>
            <li><span class="task-check">○</span> system.py: abrir apps, ajustar volumen y brillo</li>
            <li><span class="task-check">○</span> files.py: leer, escribir y listar archivos</li>
            <li><span class="task-check">○</span> browser.py: buscar en Google con Playwright</li>
            <li><span class="task-check">○</span> Tool calling: pasar TOOL dicts a Ollama, parsear JSON response</li>
          </ul>
          <div class="code-block">
            <div class="code-header">
              <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
              <span class="code-filename">plugins/system.py — patrón estándar</span>
            </div>
            <pre>TOOL = {
    <span class="st">"name"</span>: <span class="st">"open_app"</span>,
    <span class="st">"description"</span>: <span class="st">"Abre una aplicación del sistema"</span>,
    <span class="st">"parameters"</span>: {<span class="st">"app"</span>: <span class="st">"string"</span>}
}

<span class="kw">async def</span> <span class="fn">execute</span>(app: <span class="nm">str</span>):
    <span class="kw">import</span> subprocess
    subprocess.<span class="fn">Popen</span>([app])
    <span class="kw">return</span> {<span class="st">"ok"</span>: <span class="nm">True</span>}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- SEMANA 4 -->
    <div class="week-item" id="w3">
      <div class="week-dot"></div>
      <div class="week-card">
        <button class="week-toggle" onclick="toggleWeek('w3')" aria-expanded="false">
          <span class="week-badge badge-amber">Semana 4</span>
          <div class="week-titles">
            <div class="week-title">Plugins específicos — YouTube & Drive</div>
            <div class="week-sub">Chromecast + Google Drive integrados</div>
          </div>
          <span class="week-chevron">⌄</span>
        </button>
        <div class="week-body">
          <p class="week-desc">Las herramientas que realmente importan. youtube.py busca, extrae la URL del primer resultado y hace cast a tu TV. cloud.py sube y descarga de Drive con la API de Google.</p>
          <div class="libs">
            <span class="lib-tag">playwright</span>
            <span class="lib-tag">pychromecast</span>
            <span class="lib-tag">google-api-python-client</span>
            <span class="lib-tag">oauth2client</span>
          </div>
          <ul class="tasks">
            <li><span class="task-check">○</span> youtube.py: buscar → extraer URL → pychromecast.get_chromecast()</li>
            <li><span class="task-check">○</span> Manejar edge cases: TV apagada, sin Wi-Fi, vídeo no encontrado</li>
            <li><span class="task-check">○</span> Configurar OAuth2 para Google Drive (service account recomendado)</li>
            <li><span class="task-check">○</span> cloud.py: subir archivo, listar recientes, descargar por nombre</li>
            <li><span class="task-check">○</span> Test end-to-end: "Jarvis, pon Daft Punk en la TV"</li>
          </ul>
          <div class="code-block">
            <div class="code-header">
              <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
              <span class="code-filename">plugins/youtube.py</span>
            </div>
            <pre><span class="kw">async def</span> <span class="fn">execute</span>(query: <span class="nm">str</span>):
    <span class="kw">async with</span> <span class="fn">async_playwright</span>() <span class="kw">as</span> p:
        page = <span class="kw">await</span> p.chromium.<span class="fn">launch</span>().<span class="fn">new_page</span>()
        <span class="kw">await</span> page.<span class="fn">goto</span>(<span class="st">f"youtube.com/results?q={query}"</span>)
        url = <span class="kw">await</span> page.<span class="fn">evaluate</span>(<span class="st">"""() =>
            document.querySelector('ytd-video-renderer a')?.href
        """</span>)
    cast = pychromecast.<span class="fn">get_chromecast</span>()
    cast.<span class="fn">play_media</span>(url, <span class="st">"video/mp4"</span>)
    <span class="kw">return</span> {<span class="st">"ok"</span>: <span class="nm">True</span>, <span class="st">"url"</span>: url}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- SEMANA 5 -->
    <div class="week-item" id="w4">
      <div class="week-dot"></div>
      <div class="week-card">
        <button class="week-toggle" onclick="toggleWeek('w4')" aria-expanded="false">
          <span class="week-badge badge-amber">Semana 5</span>
          <div class="week-titles">
            <div class="week-title">Enrutador semántico + más plugins</div>
            <div class="week-sub">ChromaDB para selección inteligente de herramientas</div>
          </div>
          <span class="week-chevron">⌄</span>
        </button>
        <div class="week-body">
          <p class="week-desc">Con 10+ plugins, pasar todos los TOOL dicts al LLM es ineficiente. ChromaDB embeddea las descripciones y solo envía al modelo las 3 más relevantes para el texto del usuario.</p>
          <div class="libs">
            <span class="lib-tag">chromadb</span>
            <span class="lib-tag">sentence-transformers</span>
            <span class="lib-tag">home-assistant-api</span>
            <span class="lib-tag">caldav</span>
          </div>
          <ul class="tasks">
            <li><span class="task-check">○</span> Indexar todos los TOOL['description'] en ChromaDB al arrancar</li>
            <li><span class="task-check">○</span> relevant_for(text): query semántico → top 3 herramientas</li>
            <li><span class="task-check">○</span> Añadir 3–5 plugins según tus necesidades (alarmas, Spotify, clima…)</li>
            <li><span class="task-check">○</span> Benchmark: medir latencia con router vs sin él</li>
            <li><span class="task-check">○</span> Logging básico: qué tool eligió y por qué</li>
          </ul>
          <div class="code-block">
            <div class="code-header">
              <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
              <span class="code-filename">core/plugin_registry.py</span>
            </div>
            <pre><span class="kw">class</span> <span class="fn">PluginRegistry</span>:
    <span class="kw">def</span> <span class="fn">relevant_for</span>(self, text: <span class="nm">str</span>, k: <span class="nm">int</span> = <span class="nm">3</span>):
        results = self.collection.<span class="fn">query</span>(
            query_texts=[text],
            n_results=k
        )
        <span class="kw">return</span> [self.plugins[name]
                <span class="kw">for</span> name <span class="kw">in</span> results[<span class="st">"ids"</span>][<span class="nm">0</span>]]</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- SEMANA 6 -->
    <div class="week-item" id="w5">
      <div class="week-dot"></div>
      <div class="week-card">
        <button class="week-toggle" onclick="toggleWeek('w5')" aria-expanded="false">
          <span class="week-badge badge-coral">Semana 6</span>
          <div class="week-titles">
            <div class="week-title">UI overlay + memoria persistente</div>
            <div class="week-sub">HUD flotante y contexto entre sesiones</div>
          </div>
          <span class="week-chevron">⌄</span>
        </button>
        <div class="week-body">
          <p class="week-desc">El toque final: un overlay siempre-encima que muestra estado, herramienta activa y la última respuesta. La memoria guarda las últimas conversaciones para que Jarvis recuerde contexto.</p>
          <div class="libs">
            <span class="lib-tag">customtkinter</span>
            <span class="lib-tag">SQLite</span>
            <span class="lib-tag">pynput</span>
          </div>
          <ul class="tasks">
            <li><span class="task-check">○</span> Overlay siempre-encima con estado: escuchando / pensando / hablando</li>
            <li><span class="task-check">○</span> Mostrar texto de la última respuesta y herramienta usada</li>
            <li><span class="task-check">○</span> Guardar últimas 20 conversaciones en SQLite</li>
            <li><span class="task-check">○</span> Inyectar resumen del historial en el system prompt de Ollama</li>
            <li><span class="task-check">○</span> Hotkey global Ctrl+J para activar sin wake word (opcional)</li>
          </ul>
          <div class="code-block">
            <div class="code-header">
              <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
              <span class="code-filename">core/memory.py</span>
            </div>
            <pre><span class="kw">class</span> <span class="fn">Memory</span>:
    <span class="kw">def</span> <span class="fn">get_context</span>(self, n: <span class="nm">int</span> = <span class="nm">5</span>) -> <span class="nm">str</span>:
        rows = self.db.<span class="fn">execute</span>(
            <span class="st">"SELECT role, content FROM history"</span>
            <span class="st">" ORDER BY ts DESC LIMIT ?"</span>, [n]
        ).<span class="fn">fetchall</span>()
        <span class="kw">return</span> <span class="st">"\n"</span>.<span class="fn">join</span>(<span class="st">f"{r}:{c}"</span> <span class="kw">for</span> r, c <span class="kw">in</span> rows[::<span class="nm">-1</span>])</pre>
          </div>
        </div>
      </div>
    </div>

  </div>
</section>

<!-- PLUGINS -->
<section id="plugins">
  <div class="section-head"><h2>Plugins iniciales</h2></div>
  <p style="font-size:14px;color:var(--text-dim);margin-bottom:1.5rem">Cada uno es un archivo Python independiente de ~30 líneas. La IA decide cuál usar. Añadir uno nuevo nunca toca el engine.</p>
  <div class="plugins-grid">
    <div class="plugin-card"><div class="plugin-icon">🖥️</div><div class="plugin-name">system.py</div><div class="plugin-desc">Abrir apps, volumen, brillo</div></div>
    <div class="plugin-card"><div class="plugin-icon">📁</div><div class="plugin-name">files.py</div><div class="plugin-desc">Leer, escribir, listar archivos</div></div>
    <div class="plugin-card"><div class="plugin-icon">🌐</div><div class="plugin-name">browser.py</div><div class="plugin-desc">Buscar en Google con Playwright</div></div>
    <div class="plugin-card"><div class="plugin-icon">▶️</div><div class="plugin-name">youtube.py</div><div class="plugin-desc">Buscar + reproducir en TV</div></div>
    <div class="plugin-card"><div class="plugin-icon">☁️</div><div class="plugin-name">cloud.py</div><div class="plugin-desc">Subir/descargar de Drive</div></div>
    <div class="plugin-card"><div class="plugin-icon">🏠</div><div class="plugin-name">home.py</div><div class="plugin-desc">Luces, persianas (HA API)</div></div>
    <div class="plugin-card"><div class="plugin-icon">📅</div><div class="plugin-name">calendar.py</div><div class="plugin-desc">Ver y crear eventos CalDAV</div></div>
    <div class="plugin-card"><div class="plugin-icon">🎵</div><div class="plugin-name">spotify.py</div><div class="plugin-desc">Reproducir música en local</div></div>
    <div class="plugin-card"><div class="plugin-icon">⏰</div><div class="plugin-name">timer.py</div><div class="plugin-desc">Alarmas y recordatorios</div></div>
    <div class="plugin-card"><div class="plugin-icon">🌤️</div><div class="plugin-name">weather.py</div><div class="plugin-desc">Tiempo con Open-Meteo (gratis)</div></div>
    <div class="plugin-card"><div class="plugin-icon">📝</div><div class="plugin-name">notes.py</div><div class="plugin-desc">Notas rápidas en Obsidian/txt</div></div>
    <div class="plugin-card"><div class="plugin-icon">➕</div><div class="plugin-name">tu_plugin.py</div><div class="plugin-desc">1 archivo · 15 minutos</div></div>
  </div>
</section>

<!-- STACK COMPLETO -->
<section id="stack">
  <div class="section-head"><h2>Stack completo</h2></div>

  <table class="stack-table" style="margin-bottom:2rem">
    <thead>
      <tr>
        <th>Paquete</th>
        <th>Para qué</th>
        <th>Semana</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><span class="pkg-name">pvporcupine</span></td><td style="color:var(--text-dim)">Wake word "jarvis" local, sin internet</td><td style="color:var(--text-dim)">1–2</td></tr>
      <tr><td><span class="pkg-name">openai-whisper</span></td><td style="color:var(--text-dim)">STT offline (modelo tiny/base/small)</td><td style="color:var(--text-dim)">1–2</td></tr>
      <tr><td><span class="pkg-name">ollama</span></td><td style="color:var(--text-dim)">LLM local: qwen3:14b o llama3.2:3b</td><td style="color:var(--text-dim)">1–2</td></tr>
      <tr><td><span class="pkg-name">pyttsx3</span></td><td style="color:var(--text-dim)">TTS básico offline</td><td style="color:var(--text-dim)">1–2</td></tr>
      <tr><td><span class="pkg-name">playwright</span></td><td style="color:var(--text-dim)">Automatización navegador (YouTube, búsquedas)</td><td style="color:var(--text-dim)">3</td></tr>
      <tr><td><span class="pkg-name">pychromecast</span></td><td style="color:var(--text-dim)">Enviar vídeo/audio a Chromecast por red local</td><td style="color:var(--text-dim)">4</td></tr>
      <tr><td><span class="pkg-name">google-api-python-client</span></td><td style="color:var(--text-dim)">Google Drive, Calendar, etc.</td><td style="color:var(--text-dim)">4</td></tr>
      <tr><td><span class="pkg-name">chromadb</span></td><td style="color:var(--text-dim)">Vector store para routing semántico de plugins</td><td style="color:var(--text-dim)">5</td></tr>
      <tr><td><span class="pkg-name">sentence-transformers</span></td><td style="color:var(--text-dim)">Embeddings locales para ChromaDB</td><td style="color:var(--text-dim)">5</td></tr>
      <tr><td><span class="pkg-name">customtkinter</span></td><td style="color:var(--text-dim)">Overlay HUD flotante siempre-encima</td><td style="color:var(--text-dim)">6</td></tr>
    </tbody>
  </table>

  <div class="install-block">
    <div class="install-header">
      <span class="install-label">$ pip install</span>
      <button class="copy-btn" onclick="copyInstall()" id="copy-btn">copiar</button>
    </div>
    <pre id="install-cmd"><span class="kw">pip install</span> pvporcupine openai-whisper ollama pyttsx3 \
            playwright pychromecast \
            google-api-python-client oauth2client \
            chromadb sentence-transformers \
            customtkinter screen-brightness-control \
            pyautogui pynput</pre>
  </div>
</section>

<footer>
  J.A.R.V.I.S — Just A Rather Very Intelligent System &nbsp;·&nbsp; Plan de construcción personal
</footer>

<script>
  /* ── TYPEWRITER ── */
  const lines = [
    "Initializing voice subsystem...",
    "Loading plugin registry...",
    "Connecting to Ollama — qwen3:14b...",
    "All systems operational. Jarvis ready.",
  ];
  let li = 0, ci = 0, deleting = false;
  const el = document.getElementById('tw-text');

  function type() {
    const line = lines[li];
    if (!deleting) {
      el.textContent = line.slice(0, ci + 1);
      ci++;
      if (ci === line.length) {
        deleting = true;
        setTimeout(type, li === lines.length - 1 ? 3000 : 1800);
        return;
      }
    } else {
      el.textContent = line.slice(0, ci - 1);
      ci--;
      if (ci === 0) {
        deleting = false;
        li = (li + 1) % lines.length;
        setTimeout(type, 400);
        return;
      }
    }
    setTimeout(type, deleting ? 28 : 55);
  }
  type();

  /* ── TOGGLE WEEKS ── */
  function toggleWeek(id) {
    const item = document.getElementById(id);
    const btn  = item.querySelector('.week-toggle');
    const isOpen = item.classList.contains('open');
    item.classList.toggle('open', !isOpen);
    btn.setAttribute('aria-expanded', String(!isOpen));
  }

  /* ── COPY INSTALL ── */
  function copyInstall() {
    const text = document.getElementById('install-cmd').innerText;
    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('copy-btn');
      btn.textContent = 'copiado ✓';
      setTimeout(() => btn.textContent = 'copiar', 2000);
    });
  }

  /* ── TASK CHECKBOXES ── */
  document.querySelectorAll('.task-check').forEach(span => {
    span.style.cursor = 'pointer';
    span.title = 'Marcar como hecho';
    span.addEventListener('click', () => {
      const done = span.textContent === '✓';
      span.textContent = done ? '○' : '✓';
      span.style.color = done ? 'var(--cyan)' : 'var(--green)';
      span.closest('li').style.opacity = done ? '1' : '0.5';
    });
  });
</script>
</body>
</html>
