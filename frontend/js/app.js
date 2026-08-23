document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    startTelemetryPolling();
    loadGrafanaTools();
    loadAuditLogs();
});

function setupTabNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitle = document.getElementById('page-title');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');

            if (pageTitle) {
                pageTitle.textContent = btn.textContent.trim();
            }
        });
    });
}

function startTelemetryPolling() {
    updateTelemetry();
    setInterval(updateTelemetry, 2500);
}

async function updateTelemetry() {
    try {
        const res = await fetch('/api/telemetry/stream');
        const data = await res.json();

        document.getElementById('val-cpu').textContent = data.ingest_cpu_pct + '%';
        document.getElementById('val-queue').textContent = data.transcode_queue_depth + ' frames';
        document.getElementById('val-cdn').textContent = data.cdn_egress_gbps + ' Gbps';
        document.getElementById('val-buffer').textContent = data.buffer_ratio_pct + '%';
        document.getElementById('val-desync').textContent = data.audio_video_desync_ms + ' ms';
        document.getElementById('val-viewers').textContent = data.active_viewers.toLocaleString();

        const cpuElem = document.getElementById('val-cpu');
        if (data.ingest_cpu_pct > 80.0) {
            cpuElem.style.color = '#ef4444';
        } else {
            cpuElem.style.color = '#38bdf8';
        }
    } catch (e) {
        console.log('Error fetching stream metrics:', e);
    }
}

async function runMCPAnalysis() {
    const feed = document.getElementById('alert-feed-box');
    feed.innerHTML = '<div class="placeholder-state"><i class="fa-solid fa-spinner fa-spin placeholder-icon"></i><p>Gemini ADK querying Grafana Cloud MCP Server (query_prometheus_metrics, query_loki_logs)...</p></div>';

    try {
        const res = await fetch('/api/mcp/analyze', { method: 'POST' });
        const data = await res.json();

        const severityClass = data.headline.includes('CRITICAL') ? 'critical' : (data.headline.includes('WARNING') ? 'warning' : 'stable');

        feed.innerHTML = `
            <div class="alert-card ${severityClass}">
                <div class="alert-headline">${data.headline}</div>
                <div class="alert-body">${data.plain_language_narrative}</div>
                <div style="margin-bottom:0.5rem; font-size:0.85rem;"><strong>Impact:</strong> ${data.impact_summary}</div>
                <div style="margin-bottom:0.75rem; font-size:0.85rem; color:#f97316;"><strong>Recommended Executive Action:</strong> ${data.recommended_action}</div>
                <div class="alert-meta">
                    <span>Grafana Incident: ${data.grafana_incident_id || 'N/A'}</span>
                    <span>Dashboard Annotation: Synced @ ${data.grafana_annotation_timestamp}</span>
                    <span>Time: ${data.timestamp}</span>
                </div>
            </div>
        `;

        document.getElementById('narrator-card-content').innerHTML = `
            <div style="padding:1rem; background:#0b0f19; border-radius:8px; border:1px solid #1f2937;">
                <h4 style="color:#f97316; margin-bottom:0.5rem;">${data.headline}</h4>
                <p style="font-size:0.95rem; line-height:1.6;">${data.plain_language_narrative}</p>
                <div style="margin-top:1rem; padding:0.75rem; background:#111827; border-radius:6px; border-left:3px solid #38bdf8;">
                    <strong>Root Cause Signal Correlation:</strong> Evaluated Grafana PromQL metrics and Loki LogQL streams via <code>grafana/mcp-grafana</code> tools.
                </div>
            </div>
        `;

        loadAuditLogs();
    } catch (e) {
        alert('Error analyzing broadcast health: ' + e);
    }
}

async function injectAnomaly(type) {
    try {
        await fetch(`/api/simulator/inject?anomaly_type=${type}`, { method: 'POST' });
        updateTelemetry();
        setTimeout(runMCPAnalysis, 800);
    } catch (e) {
        alert('Error injecting anomaly: ' + e);
    }
}

async function loadGrafanaTools() {
    try {
        const res = await fetch('/api/mcp/tools');
        const data = await res.json();
        const box = document.getElementById('mcp-tools-list');
        if (box) {
            box.innerHTML = data.tools.map(t => `
                <div class="tool-card">
                    <h4>${t.name}</h4>
                    <p style="font-size:0.8rem; color:#9ca3af;">${t.description}</p>
                </div>
            `).join('');
        }
    } catch (e) {
        console.log('Error loading Grafana MCP tools:', e);
    }
}

async function loadAuditLogs() {
    try {
        const res = await fetch('/api/mcp/audit');
        const data = await res.json();
        const box = document.getElementById('mcp-audit-box');
        if (box) {
            box.textContent = JSON.stringify(data, null, 2);
        }
    } catch (e) {
        console.log('Error loading MCP audit logs:', e);
    }
}
