const API_BASE = window.ARK_API_BASE || 'http://127.0.0.1:8081';

function pretty(value) {
  if (!value) return 'None recorded.';
  return JSON.stringify(value, null, 2);
}

async function refreshStatus() {
  const response = await fetch(`${API_BASE}/status`, { cache: 'no-store' });
  if (!response.ok) throw new Error(`status request failed: ${response.status}`);
  const status = await response.json();

  document.getElementById('authority-mode').textContent = status.authority.mode;
  document.getElementById('event-count').textContent = status.bus.event_count;
  document.getElementById('event-path').textContent = status.bus.path;
  document.getElementById('evidence-count').textContent = status.evidence.record_count;
  document.getElementById('evidence-path').textContent = status.evidence.path;
  document.getElementById('last-event').textContent = pretty(status.bus.last_event);
  document.getElementById('last-evidence').textContent = pretty(status.evidence.last_record);
}

async function safeRefresh() {
  try {
    await refreshStatus();
  } catch (error) {
    document.getElementById('authority-mode').textContent = 'offline';
    document.getElementById('last-event').textContent = String(error);
    document.getElementById('last-evidence').textContent = 'Start the local API with: python -m opt.ark.runtime.api.server';
  }
}

document.getElementById('refresh').addEventListener('click', safeRefresh);
safeRefresh();
