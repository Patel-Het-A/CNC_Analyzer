const API_BASE = "http://localhost:8000";

const SAMPLE_GCODE = `G21
G90
G00 Z10

G00 X0 Y0
G01 Z-2 F300
G01 X40 Y0
G01 X40 Y20
G01 X0 Y20
G01 X0 Y0
G00 Z10

G00 X50 Y0
G01 Z-2
G01 X90 Y0
G01 X90 Y20
G01 X50 Y20
G01 X50 Y0
G00 Z10

G00 X0 Y30
G01 Z-2
G01 X40 Y30
G01 X0 Y35
G01 X40 Y35
G01 X0 Y40
G01 X40 Y40
G00 Z10

G00 X70 Y40
G01 Z-2
G01 X75 Y45
G01 X80 Y50
G01 X85 Y45
G01 X90 Y40
G01 X85 Y35
G01 X80 Y30
G01 X75 Y35
G01 X70 Y40
G00 Z10

G00 X10 Y60
G01 Z-2
G01 X20 Y70
G00 Z10

G00 X80 Y70
G01 Z-2
G01 X60 Y60
G00 Z10

G00 X20 Y80
G01 Z-2
G01 X30 Y80
G01 X30 Y90
G01 X20 Y90
G01 X20 Y80
G00 Z10

G00 X60 Y80
G01 Z-2
G01 X70 Y80
G01 X70 Y90
G01 X60 Y90
G01 X60 Y80
G00 Z10

G00 X0 Y100
G01 Z-2
G01 X100 Y100
G00 Z10

M30`;

const FAULTY_GCODE = `G21
G90
G00 Z15
G00 X10 Y10
G01 Z-1 F250

G01 X30 Y10
G01 X30 Y30
G01 X10 Y30
G00 X10 Y10 Z-1
G00 Z15

G00 X40 Y10
G01 Z-2
G01 X60 Y10
G01 X60 Y30 F7000
G01 X40 Y30

G01 X40 Y10
G00 Z15
G00 X10 Y40
G01 Z-2
G01 X30 Y40

G01 X10 Y45
G01 X30 Y45
G01 Y50
G01 X10 Y50
G00 Z15

G00 X50 Y50
G01 Z-2
G01 X70 Y50
G01 X70 Y70
G00 X50 Y70 Z-2

G01 X50 Y50
G00 Z15
G00 X20 Y75
G01 Z-2
G01 X35 Y90

G00 Z15
G00 X80 Y80
G01 Z-2
G00 X60 Y60 Z-2
G01 X75 Y75

G00 Z15
G00 X0 Y110
G01 Z-2
G01 X90 Y110
G00 Z-8
G00 Z15

M30`;

let currentResult = null;
let currentView = "top";
let currentToolpath = [];
let currentOptimized = [];
let currentIssueLines = new Set();

const editor = document.getElementById("gcode-editor");
const lineNums = document.getElementById("line-numbers");
const lineCount = document.getElementById("line-count");
const runBtn = document.getElementById("run-btn");
const emptyState = document.getElementById("empty-state");
const loadingState = document.getElementById("loading-state");
const resultsContent = document.getElementById("results-content");

document.addEventListener("DOMContentLoaded", () => {
  updateLineNumbers();
  bindEvents();
});

function bindEvents() {
  editor.addEventListener("input", updateLineNumbers);
  editor.addEventListener("scroll", syncScroll);
  document.getElementById("btn-load-sample").addEventListener("click", () => loadCode(SAMPLE_GCODE));
  document.getElementById("btn-load-faulty").addEventListener("click", () => loadCode(FAULTY_GCODE));
  document.getElementById("btn-clear").addEventListener("click", () => loadCode(""));
  runBtn.addEventListener("click", runAnalysis);

  document.querySelectorAll(".viz-tab").forEach(t =>
    t.addEventListener("click", () => {
      document.querySelectorAll(".viz-tab").forEach(x => x.classList.remove("active"));
      t.classList.add("active");
      currentView = t.dataset.view;
      if (currentToolpath.length) drawToolpath(currentToolpath, currentOptimized, currentIssueLines);
    })
  );

  document.querySelector('[data-section="docs"]').addEventListener("click", e => {
    e.preventDefault();
    document.getElementById("docs-overlay").style.display = "flex";
  });
  document.getElementById("docs-close").addEventListener("click", () => {
    document.getElementById("docs-overlay").style.display = "none";
  });
  document.getElementById("docs-overlay").addEventListener("click", e => {
    if (e.target === e.currentTarget) e.currentTarget.style.display = "none";
  });

  document.getElementById("toggle-commands").addEventListener("click", () => {
    const wrap = document.getElementById("commands-wrap");
    const btn = document.getElementById("toggle-commands");
    const hidden = wrap.style.display === "none";
    wrap.style.display = hidden ? "block" : "none";
    btn.textContent = hidden ? "Hide" : "Show";
  });

  editor.addEventListener("keydown", e => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runAnalysis();
  });
}

function updateLineNumbers() {
  const lines = editor.value.split("\n");
  lineNums.innerHTML = lines.map((_, i) => `<div>${i + 1}</div>`).join("");
  lineCount.textContent = `${lines.length} line${lines.length !== 1 ? "s" : ""}`;
}

function syncScroll() {
  lineNums.scrollTop = editor.scrollTop;
}

function loadCode(code) {
  editor.value = code;
  updateLineNumbers();
}

async function runAnalysis() {
  const raw = editor.value.trim();
  if (!raw) { flashEditor(); return; }

  const gcode = raw.split("\n");

  showLoading();
  animateLoaderSteps();

  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ gcode })
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || "Server error");
    }

    const data = await response.json();
    currentResult = data;
    renderResults(data, gcode);

  } catch (err) {
    showError(err.message);
  }
}

function showLoading() {
  emptyState.style.display = "none";
  loadingState.style.display = "flex";
  resultsContent.style.display = "none";
  runBtn.classList.add("loading");
  runBtn.querySelector("span").textContent = "Analyzing...";
}

function animateLoaderSteps() {
  const steps = document.querySelectorAll(".loader-step");
  steps.forEach(s => { s.classList.remove("active", "done"); });
  let i = 0;
  const interval = setInterval(() => {
    if (i > 0) { steps[i - 1].classList.remove("active"); steps[i - 1].classList.add("done"); }
    if (i < steps.length) { steps[i].classList.add("active"); i++; }
    else clearInterval(interval);
  }, 600);
}

function showResults() {
  loadingState.style.display = "none";
  resultsContent.style.display = "block";
  runBtn.classList.remove("loading");
  runBtn.querySelector("span").textContent = "Run Analysis";
}

function showError(message) {
  loadingState.style.display = "none";
  resultsContent.style.display = "none";
  runBtn.classList.remove("loading");
  runBtn.querySelector("span").textContent = "Run Analysis";

  emptyState.style.display = "flex";
  emptyState.innerHTML = `
    <div class="empty-icon" style="color:var(--error)">
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="1.5"/>
        <path d="M24 14v14M24 32v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    <p class="empty-title" style="color:var(--error)">API Error</p>
    <p class="empty-sub">${escHtml(message)}</p>
    <p class="empty-sub" style="font-family:var(--font-mono);font-size:11px;margin-top:8px;color:var(--text-muted);">
      Run: uvicorn api.app:app --reload --port 8000
    </p>
  `;
}

function renderResults(data, gcode) {
  setTimeout(() => {
    showResults();
    renderMetrics(data.metrics);
    renderIssues(data.issues || []);
    buildToolpathFromGCode(gcode, data.issues || []);
    renderAI(data.ai);
    renderCommands(gcode, data.issues || []);
  }, 600);
}

function renderMetrics(metrics) {
  const orig = metrics.original || {};
  const opt = metrics.optimized || {};
  const impr = metrics.improvemnt ?? metrics.improvement ?? 0;

  document.getElementById("m-original").textContent =
    orig.total !== undefined ? `${orig.total} mm` : "—";
  document.getElementById("m-optimized").textContent =
    opt.total !== undefined ? `${opt.total} mm` : "—";
  document.getElementById("m-improvement").textContent =
    impr !== undefined ? `${impr}%` : "—";
  document.getElementById("m-efficiency").textContent =
    orig["efficiency_%"] !== undefined ? `${orig["efficiency_%"]}%` : "—";

  const effOrig = orig["efficiency_%"] || 0;
  const effOpt = opt["efficiency_%"] || 0;
  const bars = document.getElementById("efficiency-bars");
  bars.innerHTML = `
    <div class="bar-group">
      <div class="bar-label">
        <span class="bar-name">Original Efficiency</span>
        <span class="bar-pct">${effOrig}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill original" id="bar-orig" style="width:0%"></div>
      </div>
    </div>
    <div class="bar-group">
      <div class="bar-label">
        <span class="bar-name">Optimized Efficiency</span>
        <span class="bar-pct">${effOpt}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill optimized" id="bar-opt" style="width:0%"></div>
      </div>
    </div>
  `;
  requestAnimationFrame(() => {
    setTimeout(() => {
      document.getElementById("bar-orig").style.width = effOrig + "%";
      document.getElementById("bar-opt").style.width = effOpt + "%";
    }, 100);
  });
}

function renderIssues(issues) {
  const list = document.getElementById("issues-list");
  const count = document.getElementById("issues-count");
  count.textContent = issues.length;

  if (!issues.length) {
    list.innerHTML = `<div class="no-issues">✓ No issues detected — G-code looks clean</div>`;
    return;
  }

  list.innerHTML = issues.map((issue, i) => {
    let line = "?", msg = "", sev = "WARNING", type = "";
    if (typeof issue === "string") {
      const lineM = issue.match(/line=(\d+)/);
      const msgM = issue.match(/msg='([^']+)'/);
      const sevM = issue.match(/severity=(\w+)/);
      const typeM = issue.match(/type=(\w+)/);
      line = lineM ? lineM[1] : "?";
      msg = msgM ? msgM[1] : issue;
      sev = sevM ? sevM[1] : "WARNING";
      type = typeM ? typeM[1] : "";
    } else {
      line = issue.line_number || "?";
      msg = issue.message || "";
      sev = issue.severity || "WARNING";
      type = issue.issue_type || "";
    }
    return `
      <div class="issue-item ${sev}" style="animation-delay:${i * 0.06}s">
        <span class="issue-sev ${sev}">${sev}</span>
        <div class="issue-body">
          <div class="issue-line">Line ${line}</div>
          <div class="issue-msg">${escHtml(msg)}</div>
          ${type ? `<div class="issue-type">Type: ${type}</div>` : ""}
        </div>
      </div>
    `;
  }).join("");
}

function renderAI(ai) {
  const section = document.getElementById("ai-section");
  if (!ai) { section.style.display = "none"; return; }
  section.style.display = "block";

  const expEl = document.getElementById("ai-explanation");
  const expText = ai.explanation || "";
  if (expText) {
    const lines = expText.split("\n").filter(l => l.trim());
    expEl.innerHTML = lines.map(line => {
      const dashIdx = line.indexOf("-");
      if (dashIdx > -1 && dashIdx < 6) {
        return `<div class="ai-line">
          <span class="ai-line-num">${escHtml(line.substring(0, dashIdx).trim())}</span>
          <span class="ai-line-text">${escHtml(line.substring(dashIdx + 1).trim())}</span>
        </div>`;
      }
      return `<div class="ai-line"><span class="ai-line-text">${escHtml(line)}</span></div>`;
    }).join("");
  } else {
    expEl.textContent = "No explanation available.";
  }

  const sugEl = document.getElementById("ai-suggestions");
  const sugText = ai.suggestion || "";
  if (sugText) {
    const lines = sugText.split("\n").filter(l => l.trim());
    sugEl.innerHTML = lines.map(line => {
      const dashIdx = line.indexOf("-");
      if (dashIdx > -1 && dashIdx < 10) {
        return `<div class="ai-sug-line">
          <span class="ai-sug-num">${escHtml(line.substring(0, dashIdx).trim())}</span>
          <span class="ai-sug-text">${escHtml(line.substring(dashIdx + 1).trim())}</span>
        </div>`;
      }
      return `<div class="ai-sug-line"><span class="ai-sug-text">${escHtml(line)}</span></div>`;
    }).join("");
  } else {
    sugEl.textContent = "No suggestions.";
  }
}

function renderCommands(gcode, issues) {
  const issueLines = new Set(
    issues.map(i => {
      if (typeof i === "string") {
        const m = i.match(/line=(\d+)/);
        return m ? parseInt(m[1]) : null;
      }
      return i.line_number;
    }).filter(Boolean)
  );

  const tbody = document.getElementById("commands-body");
  const rows = gcode.map((line, idx) => {
    const clean = line.replace(/[;(].*/, "").trim().toUpperCase();
    if (!clean) return null;
    const g = clean.match(/G(\d+)/)?.[0];
    const m = clean.match(/M(\d+)/)?.[0];
    const x = clean.match(/X([-\d.]+)/)?.[1];
    const y = clean.match(/Y([-\d.]+)/)?.[1];
    const z = clean.match(/Z([-\d.]+)/)?.[1];
    const f = clean.match(/F([\d.]+)/)?.[1];
    const s = clean.match(/S([\d.]+)/)?.[1];
    return { line: idx + 1, g, m, x, y, z, f, s };
  }).filter(Boolean);

  tbody.innerHTML = rows.map(cmd => {
    const isIssue = issueLines.has(cmd.line);
    const rowStyle = isIssue ? 'style="background:rgba(255,92,92,0.05)"' : "";
    return `<tr ${rowStyle}>
      <td>${cmd.line}${isIssue ? ' <span style="color:var(--error)">⚠</span>' : ""}</td>
      <td class="cmd-gcode">${cmd.g || "—"}</td>
      <td class="cmd-mcode">${cmd.m || "—"}</td>
      <td class="cmd-coord">${cmd.x || "—"}</td>
      <td class="cmd-coord">${cmd.y || "—"}</td>
      <td class="cmd-coord">${cmd.z || "—"}</td>
      <td>${cmd.f || "—"}</td>
      <td>${cmd.s || "—"}</td>
    </tr>`;
  }).join("");
}

function buildToolpathFromGCode(gcode, issues) {
  const issueLines = new Set(
    issues.map(i => {
      if (typeof i === "string") {
        const m = i.match(/line=(\d+)/);
        return m ? parseInt(m[1]) : null;
      }
      return i.line_number;
    }).filter(Boolean)
  );

  let x = 0, y = 0, z = 0;
  const segments = [];

  gcode.forEach((line, idx) => {
    const lineNum = idx + 1;
    const clean = line.replace(/[;(].*/, "").trim().toUpperCase();
    if (!clean) return;

    const g = clean.match(/G(\d+)/)?.[1];
    const nx = clean.match(/X([-\d.]+)/)?.[1];
    const ny = clean.match(/Y([-\d.]+)/)?.[1];
    const nz = clean.match(/Z([-\d.]+)/)?.[1];

    if (g === "00" || g === "01") {
      const ex = nx !== undefined ? parseFloat(nx) : x;
      const ey = ny !== undefined ? parseFloat(ny) : y;
      const ez = nz !== undefined ? parseFloat(nz) : z;
      segments.push({ sx: x, sy: y, sz: z, ex, ey, ez, type: g === "00" ? "G00" : "G01", lineNum, issue: issueLines.has(lineNum) });
      x = ex; y = ey; z = ez;
    }
  });

  currentToolpath = segments;
  currentOptimized = segments;
  currentIssueLines = issueLines;
  drawToolpath(segments, segments, issueLines);
}

function drawToolpath(segments, optimized, issueLines) {
  const canvas = document.getElementById("toolpath-canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = "#0E0E14";
  ctx.fillRect(0, 0, W, H);

  ctx.strokeStyle = "rgba(255,255,255,0.04)";
  ctx.lineWidth = 1;
  for (let gx = 0; gx <= W; gx += 40) { ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke(); }
  for (let gy = 0; gy <= H; gy += 40) { ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke(); }

  if (!segments.length) return;

  const getAxes = (view) => {
    if (view === "top") return { ax: "x", ay: "y", lx: "X", ly: "Y" };
    if (view === "side") return { ax: "x", ay: "z", lx: "X", ly: "Z" };
    return { ax: "y", ay: "z", lx: "Y", ly: "Z" };
  };
  const { ax, ay, lx, ly } = getAxes(currentView);

  const allX = segments.flatMap(s => [s[`s${ax}`], s[`e${ax}`]]);
  const allY = segments.flatMap(s => [s[`s${ay}`], s[`e${ay}`]]);
  const minX = Math.min(...allX), maxX = Math.max(...allX);
  const minY = Math.min(...allY), maxY = Math.max(...allY);
  const pad = 48;
  const rangeX = maxX - minX || 1;
  const rangeY = maxY - minY || 1;
  const scale = Math.min((W - pad * 2) / rangeX, (H - pad * 2) / rangeY) * 0.85;
  const offX = (W - rangeX * scale) / 2 - minX * scale;
  const offY = (H + rangeY * scale) / 2 + minY * scale;

  const px = v => v * scale + offX;
  const py = v => -v * scale + offY;

  ctx.fillStyle = "rgba(255,255,255,0.2)";
  ctx.font = "11px 'Space Mono', monospace";
  ctx.fillText(lx, W - 24, H / 2);
  ctx.fillText(ly, W / 2, 16);

  segments.forEach(seg => {
    const sx = px(seg[`s${ax}`]), sy = py(seg[`s${ay}`]);
    const ex = px(seg[`e${ax}`]), ey = py(seg[`e${ay}`]);
    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey);
    if (seg.issue) {
      ctx.strokeStyle = "#FF5C5C"; ctx.lineWidth = 2; ctx.setLineDash(seg.type === "G00" ? [5, 3] : []);
    } else if (seg.type === "G00") {
      ctx.strokeStyle = "#FFB347"; ctx.lineWidth = 1; ctx.setLineDash([4, 3]);
    } else {
      ctx.strokeStyle = "#60A5FA"; ctx.lineWidth = 1.5; ctx.setLineDash([]);
    }
    ctx.stroke(); ctx.setLineDash([]);
  });

  const first = segments[0];
  ctx.beginPath(); ctx.arc(px(first[`s${ax}`]), py(first[`s${ay}`]), 5, 0, Math.PI * 2);
  ctx.fillStyle = "#3EFFA0"; ctx.fill();
  ctx.fillStyle = "rgba(62,255,160,0.8)"; ctx.font = "10px 'Space Mono', monospace";
  ctx.fillText("START", px(first[`s${ax}`]) + 8, py(first[`s${ay}`]) - 6);

  const last = segments[segments.length - 1];
  ctx.beginPath(); ctx.arc(px(last[`e${ax}`]), py(last[`e${ay}`]), 5, 0, Math.PI * 2);
  ctx.fillStyle = "#FF5C5C"; ctx.fill();
  ctx.fillStyle = "rgba(255,92,92,0.8)";
  ctx.fillText("END", px(last[`e${ax}`]) + 8, py(last[`e${ay}`]) - 6);
}

function flashEditor() {
  editor.style.boxShadow = "inset 0 0 0 1px var(--error)";
  setTimeout(() => { editor.style.boxShadow = ""; }, 800);
}

function escHtml(str) {
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

window.addEventListener("resize", () => {
  if (currentToolpath.length) drawToolpath(currentToolpath, currentOptimized, currentIssueLines);
});