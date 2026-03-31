#!/usr/bin/env python3
"""
Build script to add the complete Dashboard feature to index.html.
Inserts CSS, nav link, HTML page, and JavaScript in a single pass.
"""

import re

FILE = 'templates/index.html'

with open(FILE, 'r') as f:
    html = f.read()

# ─── 1. Add Dashboard CSS before </style> ─────────────────────────────
DASH_CSS = r"""
    /* ── Dashboard Page ───────────────────────────────────────── */
    .dash-hero{background:linear-gradient(135deg,#1e1b4b 0%,#4c1d95 50%,#7c3aed 100%);border-radius:var(--r);padding:2.5rem;color:#fff;margin-bottom:2rem;position:relative;overflow:hidden}
    .dash-hero::after{content:'';position:absolute;right:-50px;top:-50px;width:280px;height:280px;background:rgba(255,255,255,.06);border-radius:50%}
    .dash-hero-title{font-family:'Sora',sans-serif;font-size:1.8rem;font-weight:800;margin-bottom:.4rem;display:flex;align-items:center;gap:.6rem}
    .dash-hero-sub{font-size:.9rem;opacity:.88}
    .dash-hero-meta{display:flex;gap:1.5rem;margin-top:1rem;flex-wrap:wrap}
    .dash-meta-item{background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.2);border-radius:12px;padding:.5rem 1rem;display:flex;align-items:center;gap:.5rem;font-size:.8rem;font-weight:600}
    .dash-meta-num{font-family:'Sora',sans-serif;font-weight:800;font-size:1.1rem}
    .btn-export{padding:.6rem 1.2rem;border-radius:10px;border:1.5px solid rgba(255,255,255,.5);background:rgba(255,255,255,.12);backdrop-filter:blur(8px);color:#fff;font-size:.82rem;font-weight:700;cursor:pointer;transition:all .2s;white-space:nowrap;flex-shrink:0}
    .btn-export:hover{background:rgba(255,255,255,.22);border-color:#fff}
    .dash-stats-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:1.25rem;margin-bottom:1.75rem}
    .dash-stat-card{background:var(--card);border-radius:var(--r);border:1px solid var(--border);box-shadow:var(--sh-sm);padding:1.2rem;position:relative;overflow:hidden}
    .dash-stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:var(--r) var(--r) 0 0}
    .dash-stat-card:nth-child(1)::before{background:var(--p)}.dash-stat-card:nth-child(2)::before{background:var(--green)}.dash-stat-card:nth-child(3)::before{background:var(--violet)}.dash-stat-card:nth-child(4)::before{background:var(--amber)}.dash-stat-card:nth-child(5)::before{background:#0891B2}
    .dash-stat-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;margin-bottom:.6rem}
    .dash-stat-card:nth-child(1) .dash-stat-icon{background:rgba(108,60,225,.1)}.dash-stat-card:nth-child(2) .dash-stat-icon{background:rgba(16,185,129,.1)}.dash-stat-card:nth-child(3) .dash-stat-icon{background:rgba(167,139,250,.1)}.dash-stat-card:nth-child(4) .dash-stat-icon{background:rgba(245,158,11,.1)}.dash-stat-card:nth-child(5) .dash-stat-icon{background:rgba(8,145,178,.1)}
    .dash-stat-val{font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:800;line-height:1;margin-bottom:.3rem}
    .dash-stat-card:nth-child(1) .dash-stat-val{color:var(--p)}.dash-stat-card:nth-child(2) .dash-stat-val{color:var(--green)}.dash-stat-card:nth-child(3) .dash-stat-val{color:var(--violet)}.dash-stat-card:nth-child(4) .dash-stat-val{color:var(--amber)}.dash-stat-card:nth-child(5) .dash-stat-val{color:#0891B2}
    .dash-stat-lbl{font-size:.68rem;font-weight:700;color:var(--txt2);text-transform:uppercase;letter-spacing:.5px}
    .dash-sec-title{font-family:'Sora',sans-serif;font-size:1.15rem;font-weight:800;margin-bottom:1.2rem;display:flex;align-items:center;gap:.5rem}
    .dash-section{margin-bottom:1.75rem}
    .dash-charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.75rem;margin-bottom:1.75rem}
    .dash-chart-card{background:var(--card);border-radius:var(--r);border:1px solid var(--border);box-shadow:var(--sh-md);padding:1.5rem}
    .dash-chart-title{font-family:'Sora',sans-serif;font-size:.95rem;font-weight:800;margin-bottom:1rem;display:flex;align-items:center;gap:.5rem}
    .dash-chart-wrap{position:relative;height:220px}
    .dash-table-card{background:var(--card);border-radius:var(--r);border:1px solid var(--border);box-shadow:var(--sh-md);padding:1.5rem;margin-bottom:1.75rem}
    .dash-table-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.2rem}
    .dash-table-title{font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:800;display:flex;align-items:center;gap:.5rem}
    .btn-clear-history{padding:.45rem 1rem;border-radius:8px;border:1.5px solid var(--red);background:transparent;color:var(--red);font-size:.75rem;font-weight:700;cursor:pointer;transition:all .2s}
    .btn-clear-history:hover{background:rgba(239,68,68,.08)}
    .dash-table{width:100%;border-collapse:separate;border-spacing:0}
    .dash-table th{text-align:left;font-size:.68rem;font-weight:700;color:var(--txt2);text-transform:uppercase;letter-spacing:.6px;padding:.6rem .8rem;border-bottom:2px solid var(--border);background:#FAFBFE}
    .dash-table th:first-child{border-radius:10px 0 0 0}.dash-table th:last-child{border-radius:0 10px 0 0}
    .dash-table td{padding:.75rem .8rem;font-size:.82rem;border-bottom:1px solid var(--border);vertical-align:middle}
    .dash-table tr:last-child td{border-bottom:none}.dash-table tr:hover td{background:#F8F9FE}
    .risk-pill{display:inline-flex;align-items:center;gap:4px;padding:.25rem .65rem;border-radius:20px;font-size:.7rem;font-weight:700;white-space:nowrap}
    .risk-pill.low{background:rgba(16,185,129,.12);color:#065F46}.risk-pill.moderate{background:rgba(245,158,11,.12);color:#92400E}.risk-pill.high{background:rgba(239,68,68,.12);color:#991B1B}
    .dash-empty{background:var(--card);border:2px dashed var(--border);border-radius:var(--r);padding:3.5rem 2rem;text-align:center}
    .dash-empty-icon{font-size:4rem;margin-bottom:1rem}.dash-empty-title{font-family:'Sora',sans-serif;font-size:1.3rem;font-weight:800;margin-bottom:.5rem}.dash-empty-sub{font-size:.88rem;color:var(--txt2);line-height:1.6;margin-bottom:1.5rem;max-width:400px;margin-left:auto;margin-right:auto}
    .dash-trend-badge{font-size:.7rem;font-weight:700;padding:.2rem .55rem;border-radius:6px;display:inline-flex;align-items:center;gap:3px}
    .dash-trend-badge.up{background:rgba(239,68,68,.1);color:var(--red)}.dash-trend-badge.down{background:rgba(16,185,129,.1);color:var(--green)}.dash-trend-badge.stable{background:rgba(167,139,250,.1);color:var(--violet)}
    .risk-timeline{display:flex;gap:.75rem;flex-wrap:wrap;align-items:flex-start}
    .risk-tl-item{display:flex;flex-direction:column;align-items:center;gap:.3rem}
    .risk-tl-pill{padding:.35rem .8rem;border-radius:20px;font-size:.72rem;font-weight:700;white-space:nowrap}
    .risk-tl-pill.low{background:#D1FAE5;color:#065F46}.risk-tl-pill.moderate{background:#FEF3C7;color:#92400E}.risk-tl-pill.high{background:#FEE2E2;color:#991B1B}
    .risk-tl-date{font-size:.6rem;color:var(--txt2);font-weight:600}
    .timeline-note{font-size:.78rem;color:var(--txt2);margin-top:.8rem;font-style:italic}
    .comparison-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
    .compare-col{border-radius:14px;padding:1.2rem;border:1px solid var(--border)}
    .compare-col.best{background:linear-gradient(135deg,#F0FDF4,#fff);border-color:rgba(16,185,129,.3)}
    .compare-col.latest{background:linear-gradient(135deg,#F5F3FF,#fff);border-color:rgba(108,60,225,.3)}
    .compare-header{font-family:'Sora',sans-serif;font-size:.85rem;font-weight:800;padding:.35rem .8rem;border-radius:8px;display:inline-block;margin-bottom:.8rem}
    .compare-col.best .compare-header{background:rgba(16,185,129,.15);color:#065F46}
    .compare-col.latest .compare-header{background:rgba(108,60,225,.15);color:var(--p)}
    .compare-row{display:flex;justify-content:space-between;padding:.4rem 0;font-size:.82rem;border-bottom:1px solid var(--border)}
    .compare-row:last-child{border-bottom:none}.compare-lbl{color:var(--txt2);font-weight:600}.compare-val{font-weight:800}
    .insight-row{display:flex;align-items:flex-start;gap:.65rem;padding:.65rem 0;border-bottom:1px solid var(--border);font-size:.84rem;line-height:1.55}
    .insight-row:last-child{border-bottom:none}
    .insight-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:5px}
    .insight-crisis{background:#FFF5F5;border:1px solid #FEE2E2;border-radius:10px;padding:.8rem 1rem;margin-top:.6rem;font-size:.82rem;color:#991B1B;font-weight:600}
    .symptom-row{display:flex;align-items:center;gap:.8rem;padding:.6rem 0;border-bottom:1px solid var(--border)}
    .symptom-row:last-child{border-bottom:none}
    .symptom-icon{font-size:1.1rem;flex-shrink:0;width:28px;text-align:center}
    .symptom-label{font-size:.8rem;font-weight:700;min-width:130px;flex-shrink:0}
    .sparkline{display:flex;gap:3px;flex:1;align-items:center}
    .spark-sq{width:18px;height:18px;border-radius:4px;flex-shrink:0}
    .symptom-badge{font-size:.7rem;font-weight:700;padding:.2rem .5rem;border-radius:6px;white-space:nowrap;flex-shrink:0}
    .habit-improved{color:var(--green);font-weight:700}.habit-worsened{color:var(--red);font-weight:700}.habit-same{color:var(--txt2);font-weight:700}
"""

# Insert CSS before </style>
html = html.replace('  </style>', DASH_CSS + '  </style>', 1)

# ─── 2. Fix responsive media queries ──────────────────────────────────
# Add dashboard responsive rules to existing media queries
html = html.replace(
    """    .tips-sidebar {
        position: static
      }
    }""",
    """    .tips-sidebar {
        position: static
      }
      .dash-stats-grid{grid-template-columns:repeat(3,1fr)}
      .dash-charts-grid{grid-template-columns:1fr}
      .comparison-grid{grid-template-columns:1fr}
    }"""
)

html = html.replace(
    """      .welcome-title {
        font-size: 1.4rem
      }
    }""",
    """      .welcome-title {
        font-size: 1.4rem
      }
      .dash-stats-grid{grid-template-columns:1fr 1fr}
      .dash-hero{padding:1.5rem}
      .dash-hero-title{font-size:1.3rem}
      .btn-export{font-size:.72rem;padding:.5rem .8rem}
      .dash-table{font-size:.75rem}
      .dash-table th,.dash-table td{padding:.5rem}
      .symptom-label{min-width:90px;font-size:.72rem}
      .spark-sq{width:14px;height:14px}
      .nav-links{gap:.7rem;font-size:.8rem}
    }"""
)

# ─── 3. Add Dashboard nav link ────────────────────────────────────────
html = html.replace(
    """<span class="nav-link" onclick="showPage('tips',this)">💡 Recommendations</span>""",
    """<span class="nav-link" onclick="showPage('tips',this)">💡 Recommendations</span>
        <span class="nav-link" onclick="showPage('dashboard',this)">📊 Dashboard</span>"""
)

# ─── 4. Add Dashboard HTML page ───────────────────────────────────────
DASH_HTML = """
  <div class="page" id="page-dashboard">
    <div style="max-width:1100px;margin:0 auto">
      <div class="dash-hero">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:1">
          <div>
            <div class="dash-hero-title">📊 Your Journey Dashboard</div>
            <div class="dash-hero-sub">Track your mental wellness progress across all assessment sessions</div>
            <div class="dash-hero-meta" id="dash-hero-meta">
              <div class="dash-meta-item">📋 <span class="dash-meta-num" id="dash-total-sessions">0</span> Sessions</div>
              <div class="dash-meta-item">📅 Since <span class="dash-meta-num" id="dash-first-date">—</span></div>
            </div>
          </div>
          <button class="btn-export" onclick="exportReport()" title="Export as PDF">📄 Export My Report</button>
        </div>
      </div>
      <div id="dash-empty-state" class="dash-empty">
        <div class="dash-empty-icon">📊</div>
        <div class="dash-empty-title">No sessions yet</div>
        <div class="dash-empty-sub">Complete your first assessment to start tracking your mental wellness journey over time.</div>
        <button class="btn-go-assess" onclick="showPage('assess',document.querySelectorAll('.nav-link')[1])">Start Assessment →</button>
      </div>
      <div id="dash-main-content" style="display:none">
        <div class="dash-stats-grid">
          <div class="dash-stat-card"><div class="dash-stat-icon">📋</div><div class="dash-stat-val" id="ds-total">0</div><div class="dash-stat-lbl">Total Sessions</div></div>
          <div class="dash-stat-card"><div class="dash-stat-icon">🧠</div><div class="dash-stat-val" id="ds-avg-phq">—</div><div class="dash-stat-lbl">Avg PHQ-9</div></div>
          <div class="dash-stat-card"><div class="dash-stat-icon">💜</div><div class="dash-stat-val" id="ds-avg-wellness">—</div><div class="dash-stat-lbl">Avg Wellness</div></div>
          <div class="dash-stat-card"><div class="dash-stat-icon">📈</div><div class="dash-stat-val" id="ds-trend">—</div><div class="dash-stat-lbl">PHQ-9 Trend</div></div>
          <div class="dash-stat-card"><div class="dash-stat-icon">📅</div><div class="dash-stat-val" id="ds-days">—</div><div class="dash-stat-lbl">Days Tracked</div></div>
        </div>
        <div class="card dash-section" id="dash-risk-timeline-card">
          <h2 class="dash-sec-title">🎯 Risk Level History</h2>
          <div id="dash-risk-timeline" class="risk-timeline"></div>
          <div id="dash-risk-timeline-note" class="timeline-note" style="display:none"></div>
        </div>
        <div class="dash-charts-grid">
          <div class="dash-chart-card"><div class="dash-chart-title">🧠 PHQ-9 Score Over Time</div><div class="dash-chart-wrap"><canvas id="chart-phq-trend"></canvas></div></div>
          <div class="dash-chart-card"><div class="dash-chart-title">💜 Wellness Score Over Time</div><div class="dash-chart-wrap"><canvas id="chart-wellness-trend"></canvas></div></div>
        </div>
        <div class="card dash-section" id="dash-insights-card">
          <h2 class="dash-sec-title">💡 Your Personal Insights</h2>
          <div id="dash-insights-list"></div>
        </div>
        <div class="card dash-section" id="dash-comparison-card">
          <h2 class="dash-sec-title">📊 Best vs Latest Session</h2>
          <div class="comparison-grid" id="dash-comparison"></div>
        </div>
        <div class="dash-section">
          <h2 class="dash-sec-title" style="margin-bottom:1.5rem">📈 Your Lifestyle Patterns Over Time</h2>
          <div class="dash-charts-grid">
            <div class="dash-chart-card"><div class="dash-chart-title">🌙 Sleep Duration</div><div class="dash-chart-wrap"><canvas id="chart-sleep"></canvas></div></div>
            <div class="dash-chart-card"><div class="dash-chart-title">📱 Screen Time</div><div class="dash-chart-wrap"><canvas id="chart-screen"></canvas></div></div>
          </div>
          <div class="dash-charts-grid">
            <div class="dash-chart-card"><div class="dash-chart-title">😰 Stress Indicators</div><div class="dash-chart-wrap"><canvas id="chart-stress"></canvas></div></div>
            <div class="dash-chart-card"><div class="dash-chart-title">🤝 Social Support</div><div class="dash-chart-wrap"><canvas id="chart-support"></canvas></div></div>
          </div>
          <div class="dash-charts-grid">
            <div class="dash-chart-card"><div class="dash-chart-title">🔬 PHQ-9 Item Breakdown</div><div class="dash-chart-wrap" style="height:280px"><canvas id="chart-phq-items"></canvas></div><div id="phq-items-note" style="display:none;text-align:center;padding:1rem;color:var(--txt2);font-size:.85rem">Complete more assessments to see breakdown</div></div>
            <div class="dash-chart-card"><div class="dash-chart-title">🕸️ Wellness Radar</div><div class="dash-chart-wrap" style="height:280px"><canvas id="chart-radar"></canvas></div></div>
          </div>
        </div>
        <div class="card dash-section" id="dash-habit-card" style="display:none">
          <h2 class="dash-sec-title">📋 Habit Improvement Since First Session</h2>
          <div style="overflow-x:auto"><table class="dash-table"><thead><tr><th>Habit</th><th>First</th><th>Latest</th><th>Change</th><th>Status</th></tr></thead><tbody id="dash-habit-body"></tbody></table></div>
        </div>
        <div class="card dash-section" id="dash-symptom-card">
          <h2 class="dash-sec-title">⚡ Symptom Patterns</h2>
          <div id="dash-symptom-list"></div>
        </div>
        <div class="dash-table-card">
          <div class="dash-table-head"><div class="dash-table-title">📋 Session History</div><button class="btn-clear-history" onclick="clearHistory()">🗑 Clear History</button></div>
          <div style="overflow-x:auto"><table class="dash-table"><thead><tr><th>#</th><th>Date</th><th>Risk Level</th><th>PHQ-9</th><th>Wellness</th><th>GAD Est.</th></tr></thead><tbody id="dash-table-body"></tbody></table></div>
        </div>
      </div>
    </div>
  </div>
"""

# Insert the dashboard page before the modal overlay
html = html.replace(
    '  <div class="modal-overlay" id="modal">',
    DASH_HTML + '  <div class="modal-overlay" id="modal">'
)

# ─── 5. Modify showPage() to handle dashboard ────────────────────────
html = html.replace(
    "} else { document.getElementById('page-' + id).classList.add('active'); }",
    "} else if (id === 'dashboard') { document.getElementById('page-dashboard').classList.add('active'); loadDashboard(); } else { document.getElementById('page-' + id).classList.add('active'); }"
)

# ─── 6. Add saveSession() call in runAnalysis ─────────────────────────
html = html.replace(
    "document.getElementById('page-assess').classList.remove('active');\n        var res = document.getElementById('page-results');",
    "saveSession({ prediction: pred, probabilities: probs, phq_total: phqT, stability: stability, gad_estimate: gadSim });\n        document.getElementById('page-assess').classList.remove('active');\n        var res = document.getElementById('page-results');"
)

# ─── 7. Add all Dashboard JavaScript before DOMContentLoaded ──────────
DASH_JS = r"""
    // ── Session History & Dashboard (10 sections) ─────────────────
    function saveSession(data) {
      var sessions = JSON.parse(localStorage.getItem('ms_sessions') || '[]');
      var RL = ['Low Risk', 'Moderate Risk', 'High Risk'];
      sessions.push({
        date: new Date().toISOString(),
        riskLevel: data.prediction,
        riskLabel: RL[data.prediction],
        phqTotal: data.phq_total,
        wellness: data.stability,
        gadEstimate: data.gad_estimate,
        probabilities: data.probabilities,
        inputSnapshot: JSON.parse(JSON.stringify(inputs))
      });
      localStorage.setItem('ms_sessions', JSON.stringify(sessions));
    }

    function loadDashboard() {
      var sessions = JSON.parse(localStorage.getItem('ms_sessions') || '[]');
      var sleepMap = ['<5 hrs','5-6 hrs','6-7 hrs','7-8 hrs','>8 hrs'];
      var exerciseMap = ['Never','1-2×/wk','3-4×/wk','Daily'];
      var screenMap = ['<2 hrs','2-4 hrs','>4 hrs'];
      var supportMap = ['Never','Rarely','Sometimes','Often','Always'];
      var RISK_CLS = ['low','moderate','high'];
      var fmt = function(d){ return new Date(d).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'}) };
      var fmtShort = function(d){ return new Date(d).toLocaleDateString('en-IN',{day:'numeric',month:'short'}) };

      if (sessions.length === 0) {
        document.getElementById('dash-empty-state').style.display = 'block';
        document.getElementById('dash-main-content').style.display = 'none';
        document.getElementById('dash-total-sessions').textContent = '0';
        document.getElementById('dash-first-date').textContent = '—';
        return;
      }
      document.getElementById('dash-empty-state').style.display = 'none';
      document.getElementById('dash-main-content').style.display = 'block';

      var first = sessions[0], last = sessions[sessions.length - 1];
      document.getElementById('dash-total-sessions').textContent = sessions.length;
      document.getElementById('dash-first-date').textContent = fmtShort(first.date);

      // ── SECTION 1: Stat cards ──
      var avgP = (sessions.reduce(function(s,x){return s+x.phqTotal},0)/sessions.length).toFixed(1);
      var avgW = Math.round(sessions.reduce(function(s,x){return s+x.wellness},0)/sessions.length);
      document.getElementById('ds-total').textContent = sessions.length;
      document.getElementById('ds-avg-phq').textContent = avgP;
      document.getElementById('ds-avg-wellness').textContent = avgW + '%';

      // PHQ-9 trend: delta between latest and first
      var trendEl = document.getElementById('ds-trend');
      if (sessions.length >= 2) {
        var diff = last.phqTotal - first.phqTotal;
        if (diff > 0) trendEl.innerHTML = '<span class="dash-trend-badge up">↑ ' + diff.toFixed(1) + ' pts</span>';
        else if (diff < 0) trendEl.innerHTML = '<span class="dash-trend-badge down">↓ ' + Math.abs(diff).toFixed(1) + ' pts</span>';
        else trendEl.innerHTML = '<span class="dash-trend-badge stable">→ No change</span>';
      } else {
        trendEl.innerHTML = '<span class="dash-trend-badge stable">— First session</span>';
      }

      // Days tracked
      var daysEl = document.getElementById('ds-days');
      if (sessions.length >= 2) {
        var daysDiff = Math.max(1, Math.round((new Date(last.date) - new Date(first.date)) / 86400000));
        daysEl.textContent = daysDiff;
      } else {
        daysEl.textContent = '1st day';
      }

      // ── SECTION 3: Risk Timeline ──
      var tlContainer = document.getElementById('dash-risk-timeline');
      var tlNote = document.getElementById('dash-risk-timeline-note');
      var tlSessions = sessions.length > 8 ? sessions.slice(-8) : sessions;
      tlContainer.innerHTML = tlSessions.map(function(s){
        return '<div class="risk-tl-item"><span class="risk-tl-pill '+RISK_CLS[s.riskLevel]+'">'+s.riskLabel+'</span><span class="risk-tl-date">'+fmtShort(s.date)+'</span></div>';
      }).join('');
      if (sessions.length === 1) { tlNote.style.display = 'block'; tlNote.textContent = 'Complete more assessments to see your journey'; }
      else { tlNote.style.display = 'none'; }

      // ── SECTION 2: PHQ-9 & Wellness charts with reference lines ──
      var labels = sessions.map(function(s){ return fmtShort(s.date) });
      var phqData = sessions.map(function(s){ return s.phqTotal });
      var wellnessData = sessions.map(function(s){ return s.wellness });

      var refLinePlugin = {
        id: 'refLine',
        afterDraw: function(chart) {
          var meta = chart.options.plugins.refLine;
          if (!meta) return;
          var ctx = chart.ctx, yScale = chart.scales.y;
          var y = yScale.getPixelForValue(meta.value);
          ctx.save();
          ctx.beginPath();
          ctx.setLineDash([6,4]);
          ctx.strokeStyle = '#9CA3AF';
          ctx.lineWidth = 1.5;
          ctx.moveTo(chart.chartArea.left, y);
          ctx.lineTo(chart.chartArea.right, y);
          ctx.stroke();
          ctx.fillStyle = '#9CA3AF';
          ctx.font = "600 10px 'DM Sans'";
          ctx.fillText(meta.label, chart.chartArea.right - ctx.measureText(meta.label).width - 4, y - 5);
          ctx.restore();
        }
      };

      var baseOpts = {
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false}},
        scales:{ x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{family:"'DM Sans'",size:11}}}, y:{grid:{color:'rgba(0,0,0,.06)'},ticks:{font:{family:"'DM Sans'",size:11}}} },
        elements:{ point:{radius:5,hoverRadius:7,borderWidth:2,backgroundColor:'#fff'}, line:{tension:0.3,borderWidth:3} }
      };

      if (charts.phqTrend) charts.phqTrend.destroy();
      if (charts.wellnessTrend) charts.wellnessTrend.destroy();

      charts.phqTrend = new Chart(document.getElementById('chart-phq-trend'), {
        type:'line', plugins:[refLinePlugin],
        data:{ labels:labels, datasets:[{label:'PHQ-9',data:phqData,borderColor:'#EF4444',backgroundColor:'rgba(239,68,68,.08)',fill:true,pointBackgroundColor:'#fff',pointBorderColor:'#EF4444'}] },
        options:Object.assign({},baseOpts,{plugins:{legend:{display:false},refLine:{value:11.6,label:'Study avg (11.6)'}},scales:{x:baseOpts.scales.x,y:Object.assign({},baseOpts.scales.y,{min:0,max:27})}})
      });
      charts.wellnessTrend = new Chart(document.getElementById('chart-wellness-trend'), {
        type:'line', plugins:[refLinePlugin],
        data:{ labels:labels, datasets:[{label:'Wellness',data:wellnessData,borderColor:'#7C3AED',backgroundColor:'rgba(124,58,237,.08)',fill:true,pointBackgroundColor:'#fff',pointBorderColor:'#7C3AED'}] },
        options:Object.assign({},baseOpts,{plugins:{legend:{display:false},refLine:{value:52,label:'Study avg (52%)'}},scales:{x:baseOpts.scales.x,y:Object.assign({},baseOpts.scales.y,{min:0,max:100})}})
      });

      // ── SECTION 4: Personal Insights ──
      var insHtml = '';
      function addIns(color, text){ insHtml += '<div class="insight-row"><div class="insight-dot" style="background:'+color+'"></div><div>'+text+'</div></div>'; }

      if (sessions.length >= 2) {
        var phqDiff = last.phqTotal - first.phqTotal;
        if (phqDiff < 0) addIns('#10B981', 'Your PHQ-9 has improved by '+Math.abs(phqDiff)+' points since your first session ✓');
        else if (phqDiff > 0) addIns('#F59E0B', 'Your PHQ-9 has increased by '+phqDiff+' points — consider reaching out for support');
        else addIns('#A78BFA', 'Your PHQ-9 score has remained stable since your first session');
      }

      var bestWellness = sessions.reduce(function(b,s){ return s.wellness > b.wellness ? s : b }, sessions[0]);
      addIns('#7C3AED', 'Your best wellness score was '+bestWellness.wellness+'% on '+fmt(bestWellness.date));

      var mostCommonRisk = [0,0,0];
      sessions.forEach(function(s){ mostCommonRisk[s.riskLevel]++ });
      var topRisk = mostCommonRisk.indexOf(Math.max.apply(null,mostCommonRisk));
      var rlNames = ['Low','Moderate','High'];
      var pct = Math.round(mostCommonRisk[topRisk]/sessions.length*100);
      addIns(topRisk===0?'#10B981':topRisk===1?'#F59E0B':'#EF4444', 'You have been in '+rlNames[topRisk]+' Risk in '+mostCommonRisk[topRisk]+' out of '+sessions.length+' sessions ('+pct+'%)');

      var sleepCounts = [0,0,0,0,0];
      sessions.forEach(function(s){ if(s.inputSnapshot) sleepCounts[s.inputSnapshot.sleep]++ });
      var topSleep = sleepCounts.indexOf(Math.max.apply(null,sleepCounts));
      addIns('#6C3CE1', 'Your most common sleep duration is '+sleepMap[topSleep]);

      var totalStress = 0, stressCount = 0;
      sessions.forEach(function(s){ if(s.inputSnapshot){ totalStress += (s.inputSnapshot.workload+s.inputSnapshot.relax+s.inputSnapshot.overwhelm+s.inputSnapshot.exam)/4; stressCount++ }});
      if(stressCount) addIns('#EF4444', 'Your average stress level is '+(totalStress/stressCount).toFixed(1)+'/5');

      var hasHigh = sessions.some(function(s){ return s.riskLevel === 2 });
      if(hasHigh) insHtml += '<div class="insight-crisis">🆘 iCall: 9152987821 — free support available · Vandrevala Foundation: 1860-2662-345 (24/7)</div>';

      document.getElementById('dash-insights-list').innerHTML = insHtml;

      // ── SECTION 5: Best vs Latest comparison ──
      var compEl = document.getElementById('dash-comparison');
      var bestPHQ = sessions.reduce(function(b,s){ return s.phqTotal < b.phqTotal ? s : b }, sessions[0]);
      if (sessions.length === 1) {
        compEl.innerHTML = '<div class="compare-col best" style="display:flex;align-items:center;justify-content:center;color:var(--txt2);font-size:.88rem">No comparison yet — complete another assessment</div>' +
          '<div class="compare-col latest"><div class="compare-header">Latest Session</div><div class="compare-row"><span class="compare-lbl">Date</span><span class="compare-val">'+fmt(last.date)+'</span></div><div class="compare-row"><span class="compare-lbl">PHQ-9</span><span class="compare-val">'+last.phqTotal+'/27</span></div><div class="compare-row"><span class="compare-lbl">Wellness</span><span class="compare-val">'+last.wellness+'%</span></div><div class="compare-row"><span class="compare-lbl">Risk</span><span class="compare-val"><span class="risk-pill '+RISK_CLS[last.riskLevel]+'">'+last.riskLabel+'</span></span></div></div>';
      } else {
        compEl.innerHTML = '<div class="compare-col best"><div class="compare-header">🏆 Best Session</div><div class="compare-row"><span class="compare-lbl">Date</span><span class="compare-val">'+fmt(bestPHQ.date)+'</span></div><div class="compare-row"><span class="compare-lbl">PHQ-9</span><span class="compare-val">'+bestPHQ.phqTotal+'/27</span></div><div class="compare-row"><span class="compare-lbl">Wellness</span><span class="compare-val">'+bestPHQ.wellness+'%</span></div><div class="compare-row"><span class="compare-lbl">Risk</span><span class="compare-val"><span class="risk-pill '+RISK_CLS[bestPHQ.riskLevel]+'">'+bestPHQ.riskLabel+'</span></span></div></div>' +
          '<div class="compare-col latest"><div class="compare-header">Latest Session</div><div class="compare-row"><span class="compare-lbl">Date</span><span class="compare-val">'+fmt(last.date)+'</span></div><div class="compare-row"><span class="compare-lbl">PHQ-9</span><span class="compare-val">'+last.phqTotal+'/27</span></div><div class="compare-row"><span class="compare-lbl">Wellness</span><span class="compare-val">'+last.wellness+'%</span></div><div class="compare-row"><span class="compare-lbl">Risk</span><span class="compare-val"><span class="risk-pill '+RISK_CLS[last.riskLevel]+'">'+last.riskLabel+'</span></span></div></div>';
      }

      // ── SECTION 6: Lifestyle charts ──
      var lifestyleChartNames = ['chartSleep','chartScreen','chartStress','chartSupport','chartPhqItems','chartRadar'];
      lifestyleChartNames.forEach(function(k){ if(charts[k]) charts[k].destroy() });

      var lifeOpts = Object.assign({},baseOpts);

      // Sleep
      charts.chartSleep = new Chart(document.getElementById('chart-sleep'), {
        type:'line', plugins:[refLinePlugin],
        data:{ labels:labels, datasets:[{label:'Sleep',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.sleep:3}),borderColor:'#6C3CE1',backgroundColor:'rgba(108,60,225,.08)',fill:true,pointBackgroundColor:'#fff',pointBorderColor:'#6C3CE1'}] },
        options:Object.assign({},lifeOpts,{plugins:{legend:{display:false},refLine:{value:3,label:'Recommended'}},scales:{x:lifeOpts.scales.x,y:{min:0,max:4,grid:{color:'rgba(0,0,0,.06)'},ticks:{callback:function(v){return ['<5h','5-6h','6-7h','7-8h','>8h'][v]||''},font:{family:"'DM Sans'",size:10}}}}})
      });
      // Screen
      charts.chartScreen = new Chart(document.getElementById('chart-screen'), {
        type:'line', plugins:[refLinePlugin],
        data:{ labels:labels, datasets:[{label:'Screen',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.screen:1}),borderColor:'#F59E0B',backgroundColor:'rgba(245,158,11,.08)',fill:true,pointBackgroundColor:'#fff',pointBorderColor:'#F59E0B'}] },
        options:Object.assign({},lifeOpts,{plugins:{legend:{display:false},refLine:{value:1,label:'Moderate'}},scales:{x:lifeOpts.scales.x,y:{min:0,max:2,grid:{color:'rgba(0,0,0,.06)'},ticks:{callback:function(v){return ['<2h','2-4h','>4h'][v]||''},font:{family:"'DM Sans'",size:10}}}}})
      });
      // Stress (4 lines)
      charts.chartStress = new Chart(document.getElementById('chart-stress'), {
        type:'line',
        data:{ labels:labels, datasets:[
          {label:'Workload',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.workload:3}),borderColor:'#EF4444',backgroundColor:'transparent',pointRadius:3,borderWidth:2,tension:.3},
          {label:'Relaxing',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.relax:3}),borderColor:'#F59E0B',backgroundColor:'transparent',pointRadius:3,borderWidth:2,tension:.3},
          {label:'Overwhelm',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.overwhelm:3}),borderColor:'#FBBF24',backgroundColor:'transparent',pointRadius:3,borderWidth:2,tension:.3},
          {label:'Exam Anxiety',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.exam:3}),borderColor:'#EC4899',backgroundColor:'transparent',pointRadius:3,borderWidth:2,tension:.3}
        ]},
        options:Object.assign({},lifeOpts,{plugins:{legend:{display:true,labels:{boxWidth:10,font:{size:10,family:"'DM Sans'"}}}},scales:{x:lifeOpts.scales.x,y:{min:1,max:5,grid:{color:'rgba(0,0,0,.06)'},ticks:{font:{family:"'DM Sans'",size:10}}}}})
      });
      // Support
      charts.chartSupport = new Chart(document.getElementById('chart-support'), {
        type:'line',
        data:{ labels:labels, datasets:[{label:'Support',data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.support:3}),borderColor:'#0891B2',backgroundColor:'rgba(8,145,178,.08)',fill:true,pointBackgroundColor:'#fff',pointBorderColor:'#0891B2'}] },
        options:Object.assign({},lifeOpts,{plugins:{legend:{display:false}},scales:{x:lifeOpts.scales.x,y:{min:0,max:4,grid:{color:'rgba(0,0,0,.06)'},ticks:{callback:function(v){return ['Never','Rarely','Sometimes','Often','Always'][v]||''},font:{family:"'DM Sans'",size:10}}}}})
      });
      // PHQ-9 items (stacked bar)
      var phqNote = document.getElementById('phq-items-note');
      if (sessions.length < 2) {
        phqNote.style.display = 'block';
        document.getElementById('chart-phq-items').style.display = 'none';
      } else {
        phqNote.style.display = 'none';
        document.getElementById('chart-phq-items').style.display = 'block';
        var phqColors = ['#10B981','#34D399','#6EE7B7','#A7F3D0','#FDE68A','#FCD34D','#FBBF24','#F59E0B','#EF4444'];
        var phqLabels = ['Interest','Mood','Sleep','Energy','Appetite','Worth','Focus','Motor','Self-harm'];
        charts.chartPhqItems = new Chart(document.getElementById('chart-phq-items'), {
          type:'bar',
          data:{ labels:labels, datasets: phqLabels.map(function(lbl,i){
            return {label:lbl, data:sessions.map(function(s){return s.inputSnapshot?s.inputSnapshot.phq[i]:0}), backgroundColor:phqColors[i], borderRadius:2};
          })},
          options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true,labels:{boxWidth:8,font:{size:9,family:"'DM Sans'"}}}},scales:{x:{stacked:true,grid:{display:false},ticks:{font:{family:"'DM Sans'",size:10}}},y:{stacked:true,grid:{color:'rgba(0,0,0,.06)'},ticks:{font:{family:"'DM Sans'",size:10}}}}}
        });
      }
      // Radar
      var normalize = function(snap){
        if(!snap) return [50,50,50,50,50,50];
        return [
          Math.round(snap.sleep/4*100),
          Math.round(snap.exercise/3*100),
          Math.round((2-snap.screen)/2*100),
          Math.round(snap.support/4*100),
          Math.round((5-(snap.workload+snap.relax+snap.overwhelm+snap.exam)/4)/4*100),
          Math.round((27-sessions[sessions.length-1].phqTotal)/27*100)
        ];
      };
      var radarDS = [{label:'Latest',data:normalize(last.inputSnapshot),borderColor:'#6C3CE1',backgroundColor:'rgba(108,60,225,.15)',pointBackgroundColor:'#6C3CE1',borderWidth:2}];
      if(sessions.length>=2) radarDS.push({label:'First',data:normalize(first.inputSnapshot),borderColor:'#9CA3AF',backgroundColor:'rgba(156,163,175,.1)',pointBackgroundColor:'#9CA3AF',borderWidth:1.5,borderDash:[4,4]});
      charts.chartRadar = new Chart(document.getElementById('chart-radar'), {
        type:'radar',
        data:{ labels:['Sleep','Exercise','Low Screen','Support','Low Stress','Low PHQ-9'], datasets:radarDS },
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:sessions.length>=2,labels:{boxWidth:10,font:{size:10,family:"'DM Sans'"}}}},scales:{r:{min:0,max:100,ticks:{display:false},grid:{color:'rgba(0,0,0,.06)'},pointLabels:{font:{size:10,family:"'DM Sans'",weight:700}}}}}
      });

      // ── SECTION 7: Habit Improvement ──
      var habitCard = document.getElementById('dash-habit-card');
      if (sessions.length >= 2 && first.inputSnapshot && last.inputSnapshot) {
        habitCard.style.display = 'block';
        var habits = [
          {name:'🌙 Sleep',first:first.inputSnapshot.sleep,last:last.inputSnapshot.sleep,map:sleepMap,higherBetter:true},
          {name:'🏃 Exercise',first:first.inputSnapshot.exercise,last:last.inputSnapshot.exercise,map:exerciseMap,higherBetter:true},
          {name:'📱 Screen Time',first:first.inputSnapshot.screen,last:last.inputSnapshot.screen,map:screenMap,higherBetter:false},
          {name:'🤝 Support',first:first.inputSnapshot.support,last:last.inputSnapshot.support,map:supportMap,higherBetter:true},
          {name:'😰 Avg Stress',first:((first.inputSnapshot.workload+first.inputSnapshot.relax+first.inputSnapshot.overwhelm+first.inputSnapshot.exam)/4),last:((last.inputSnapshot.workload+last.inputSnapshot.relax+last.inputSnapshot.overwhelm+last.inputSnapshot.exam)/4),map:null,higherBetter:false}
        ];
        document.getElementById('dash-habit-body').innerHTML = habits.map(function(h){
          var fv = h.map ? h.map[h.first] : h.first.toFixed(1);
          var lv = h.map ? h.map[h.last] : h.last.toFixed(1);
          var diff = h.last - h.first;
          var improved = h.higherBetter ? diff > 0 : diff < 0;
          var worsened = h.higherBetter ? diff < 0 : diff > 0;
          var arrow = diff === 0 ? '→' : (improved ? '↑' : '↓');
          var cls = diff === 0 ? 'habit-same' : (improved ? 'habit-improved' : 'habit-worsened');
          var status = diff === 0 ? 'Same' : (improved ? 'Improved' : 'Worsened');
          return '<tr><td style="font-weight:700">'+h.name+'</td><td>'+fv+'</td><td>'+lv+'</td><td class="'+cls+'">'+arrow+'</td><td class="'+cls+'">'+status+'</td></tr>';
        }).join('');
      } else { habitCard.style.display = 'none'; }

      // ── SECTION 8: Symptom Sparklines ──
      var sparkColors = function(val,max3){
        if(max3){return val===0?'#D1FAE5':val===1?'#FEF3C7':val===2?'#FED7AA':'#FEE2E2'}
        return val<=1?'#D1FAE5':val<=2?'#FEF3C7':val<=3?'#FED7AA':val===4?'#FEE2E2':'#FCA5A5';
      };
      var sparkTextColors = function(val,max3){
        if(max3){return val===0?'#065F46':val===1?'#92400E':val===2?'#9A3412':'#991B1B'}
        return val<=1?'#065F46':val<=2?'#92400E':val<=3?'#9A3412':val===4?'#991B1B':'#7F1D1D';
      };
      var symptoms = [
        {icon:'⚡',label:'Low Energy',key:function(s){return s.inputSnapshot?s.inputSnapshot.phq[3]:0},max3:true},
        {icon:'🛌',label:'Sleep Trouble',key:function(s){return s.inputSnapshot?s.inputSnapshot.phq[2]:0},max3:true},
        {icon:'🎯',label:'Concentration',key:function(s){return s.inputSnapshot?s.inputSnapshot.phq[6]:0},max3:true},
        {icon:'😰',label:'Overwhelmed',key:function(s){return s.inputSnapshot?s.inputSnapshot.overwhelm:3},max3:false},
        {icon:'🧘',label:'Difficulty Relaxing',key:function(s){return s.inputSnapshot?s.inputSnapshot.relax:3},max3:false}
      ];
      document.getElementById('dash-symptom-list').innerHTML = symptoms.map(function(sym){
        var vals = sessions.map(sym.key);
        var current = vals[vals.length-1];
        var squares = vals.map(function(v){ return '<div class="spark-sq" style="background:'+sparkColors(v,sym.max3)+'" title="'+v+'"></div>' }).join('');
        var badgeBg = sparkColors(current,sym.max3);
        var badgeColor = sparkTextColors(current,sym.max3);
        return '<div class="symptom-row"><div class="symptom-icon">'+sym.icon+'</div><div class="symptom-label">'+sym.label+'</div><div class="sparkline">'+squares+'</div><span class="symptom-badge" style="background:'+badgeBg+';color:'+badgeColor+'">'+current+(sym.max3?'/3':'/5')+'</span></div>';
      }).join('');

      // ── SECTION 9: Session History Table ──
      var tbody = document.getElementById('dash-table-body');
      tbody.innerHTML = '';
      sessions.slice().reverse().forEach(function(s,idx){
        var d = new Date(s.date);
        var dateStr = fmt(s.date) + ' ' + d.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'});
        var row = document.createElement('tr');
        row.innerHTML = '<td style="font-weight:700;color:var(--txt2)">'+(sessions.length-idx)+'</td><td>'+dateStr+'</td><td><span class="risk-pill '+RISK_CLS[s.riskLevel]+'">'+s.riskLabel+'</span></td><td style="font-weight:700">'+s.phqTotal+'<span style="color:var(--txt2);font-weight:400"> /27</span></td><td style="font-weight:700;color:var(--p)">'+s.wellness+'%</td><td style="font-weight:700;color:var(--txt2)">'+s.gadEstimate+'<span style="font-weight:400"> /21</span></td>';
        tbody.appendChild(row);
      });
    }

    function clearHistory() {
      if (!confirm('Clear all session history? This cannot be undone.')) return;
      localStorage.removeItem('ms_sessions');
      loadDashboard();
      showToast('Session history cleared');
    }

    // ── SECTION 10: Export Report ──
    function exportReport() {
      var sessions = JSON.parse(localStorage.getItem('ms_sessions') || '[]');
      var profile = JSON.parse(localStorage.getItem('ms_profile') || '{}');
      var name = profile.name || 'User';
      if (sessions.length === 0) { showToast('No sessions to export'); return; }
      var avgP = (sessions.reduce(function(s,x){return s+x.phqTotal},0)/sessions.length).toFixed(1);
      var avgW = Math.round(sessions.reduce(function(s,x){return s+x.wellness},0)/sessions.length);
      var rows = sessions.map(function(s,i){
        var d = new Date(s.date);
        return '<tr><td>'+(i+1)+'</td><td>'+d.toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})+' '+d.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'})+'</td><td>'+s.riskLabel+'</td><td>'+s.phqTotal+'/27</td><td>'+s.wellness+'%</td><td>'+s.gadEstimate+'/21</td></tr>';
      }).join('');
      var html = '<!DOCTYPE html><html><head><title>MindScan Report - '+name+'</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui,sans-serif;padding:2rem;color:#111}h1{font-size:1.5rem;margin-bottom:.5rem}h2{font-size:1.1rem;margin:1.5rem 0 .5rem;color:#6C3CE1}.meta{color:#666;margin-bottom:1.5rem;font-size:.9rem}table{width:100%;border-collapse:collapse;margin:1rem 0}th,td{border:1px solid #ddd;padding:.5rem .7rem;text-align:left;font-size:.85rem}th{background:#f5f5f5;font-weight:700}.summary{background:#F5F3FF;border-radius:8px;padding:1rem;margin:1rem 0}.summary span{font-weight:700;color:#6C3CE1}@media print{body{padding:1rem}}</style></head><body><h1>🧠 MindScan Report</h1><p class="meta">Generated for <strong>'+name+'</strong> on '+new Date().toLocaleDateString('en-IN',{day:'numeric',month:'long',year:'numeric'})+'</p><div class="summary">Average PHQ-9: <span>'+avgP+'/27</span> · Average Wellness: <span>'+avgW+'%</span> · Total Sessions: <span>'+sessions.length+'</span></div><h2>Session History</h2><table><thead><tr><th>#</th><th>Date</th><th>Risk Level</th><th>PHQ-9</th><th>Wellness</th><th>GAD Est.</th></tr></thead><tbody>'+rows+'</tbody></table><p style="margin-top:2rem;font-size:.75rem;color:#999">This report is generated from MindScan, an AI-powered mental health assessment tool. It is not a clinical diagnosis. If you are in crisis, please contact iCall: 9152987821 or Vandrevala Foundation: 1860-2662-345.</p></body></html>';
      var w = window.open('','_blank');
      w.document.write(html);
      w.document.close();
      setTimeout(function(){ w.print() }, 500);
    }
"""

html = html.replace(
    "    document.addEventListener('DOMContentLoaded'",
    DASH_JS + "\n    document.addEventListener('DOMContentLoaded'"
)

# ─── Write result ─────────────────────────────────────────────────────
with open(FILE, 'w') as f:
    f.write(html)

print(f"✓ Dashboard built successfully! File now has {html.count(chr(10))+1} lines")
print(f"  - CSS: inserted before </style>")
print(f"  - Nav: added Dashboard tab")
print(f"  - HTML: added page-dashboard section")
print(f"  - JS: added saveSession, loadDashboard, clearHistory, exportReport")
print(f"  - Modified: showPage() and runAnalysis()")
