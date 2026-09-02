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
    const narrator = document.getElementById('narrator-card-content');

    feed.innerHTML = `
        <div class="loading-state">
            <i class="fa-solid fa-spinner fa-spin"></i>
            <p>Running real Google ADK + Grafana MCP analysis...</p>
        </div>
    `;

    narrator.innerHTML = `
        <div class="loading-state">
            <i class="fa-solid fa-spinner fa-spin"></i>
            <p>Querying live broadcast telemetry...</p>
        </div>
    `;

    try {
        const prompt =
            "Check the current broadcast health using Grafana MCP tools. " +
            "Do not invent telemetry. " +
            "Identify any significant regional degradation, retrieve supporting " +
            "metrics and logs, determine the evidence-supported likely cause, " +
            "and provide What happened, Root cause, Impact, and Recommended action.";

        const res = await fetch(
            `/api/adk/query?prompt=${encodeURIComponent(prompt)}`,
            { method: 'POST' }
        );

        if (!res.ok) {
            throw new Error(`ADK request failed: ${res.status}`);
        }

        const data = await res.json();
        const response = data.response || "No ADK response returned.";

        feed.innerHTML = `
            <div class="alert-item">
                <div class="alert-content">
                    <pre style="white-space: pre-wrap; margin: 0;">${escapeHtml(response)}</pre>
                </div>
            </div>
        `;

        narrator.innerHTML = `
            <div class="narrative-content">
                <pre style="white-space: pre-wrap; margin: 0;">${escapeHtml(response)}</pre>
            </div>
        `;

    } catch (e) {
        console.error("Real ADK analysis failed:", e);

        feed.innerHTML = `
            <div class="error-state">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <p>Real ADK analysis failed: ${escapeHtml(e.message)}</p>
            </div>
        `;

        narrator.innerHTML = `
            <div class="error-state">
                <p>${escapeHtml(e.message)}</p>
            </div>
        `;
    }
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
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
