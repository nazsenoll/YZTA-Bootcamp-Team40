const state = {
  connected: false,
};

const els = {
  disconnectedView: document.getElementById("disconnected-view"),
  connectedView: document.getElementById("connected-view"),
  btnConnect: document.getElementById("btn-connect"),
  btnDisconnect: document.getElementById("btn-disconnect"),
  connectError: document.getElementById("connect-error"),
  statusServer: document.getElementById("status-server"),
  statusDb: document.getElementById("status-db"),
  roleBadge: document.getElementById("role-badge"),
  thread: document.getElementById("thread"),
  emptyState: document.getElementById("empty-state"),
  composer: document.getElementById("composer"),
  inQuestion: document.getElementById("in-question"),
  btnAsk: document.getElementById("btn-ask"),
};

// ---------- Baglanti ----------

els.btnConnect.addEventListener("click", async () => {
  const payload = {
    server: document.getElementById("in-server").value,
    database: document.getElementById("in-database").value,
    username: document.getElementById("in-username").value,
    password: document.getElementById("in-password").value,
  };

  els.connectError.textContent = "";
  els.btnConnect.disabled = true;
  els.btnConnect.textContent = "Bağlanıyor...";

  try {
    const res = await fetch("/api/connect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!data.ok) {
      els.connectError.textContent = data.error || "Bağlantı kurulamadı.";
      return;
    }

    setConnected(data.info);
  } catch (e) {
    els.connectError.textContent = "Sunucuya ulaşılamadı.";
  } finally {
    els.btnConnect.disabled = false;
    els.btnConnect.textContent = "Bağlan";
  }
});

els.btnDisconnect.addEventListener("click", async () => {
  await fetch("/api/disconnect", { method: "POST" });
  setDisconnected();
});

function setConnected(info) {
  state.connected = true;
  els.disconnectedView.classList.add("hidden");
  els.connectedView.classList.remove("hidden");
  els.statusServer.textContent = info.server;
  els.statusDb.textContent = info.database + " · " + info.table_count + " tablo";
  renderRoleBadge(info.role);
  els.inQuestion.disabled = false;
  els.btnAsk.disabled = false;
}

function renderRoleBadge(role) {
  if (!role) {
    els.roleBadge.textContent = "";
    els.roleBadge.className = "role-badge";
    return;
  }
  els.roleBadge.textContent = role === "yonetici" ? "Yönetici · yazma izinli" : "Analist · sadece SELECT";
  els.roleBadge.className = "role-badge role-badge-" + role;
}

function setDisconnected() {
  state.connected = false;
  els.disconnectedView.classList.remove("hidden");
  els.connectedView.classList.add("hidden");
  els.inQuestion.disabled = true;
  els.btnAsk.disabled = true;
}

// ---------- Soru sorma ----------

els.composer.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = els.inQuestion.value.trim();
  if (!question) return;

  hideEmptyState();
  addUserMessage(question);
  els.inQuestion.value = "";
  els.btnAsk.disabled = true;

  const thinkingMsg = addThinkingMessage();

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    thinkingMsg.remove();

    if (!data.ok) {
      addErrorMessage(data.error || "Bir hata oluştu.");
      return;
    }

    if (data.type === "select") {
      addAnswerMessage(data);
    } else if (data.type === "write") {
      addConfirmMessage(data, question);
    }
  } catch (err) {
    thinkingMsg.remove();
    addErrorMessage("Sunucuya ulaşılamadı.");
  } finally {
    els.btnAsk.disabled = false;
  }
});

function hideEmptyState() {
  els.emptyState.classList.add("hidden");
}

function addUserMessage(text) {
  const tpl = document.getElementById("tpl-message-user");
  const node = tpl.content.cloneNode(true);
  node.querySelector(".msg-bubble").textContent = text;
  els.thread.appendChild(node);
  scrollToBottom();
}

function addThinkingMessage() {
  const div = document.createElement("div");
  div.className = "msg msg-answer";
  div.innerHTML = `<span class="loading-dots" style="color: var(--text-dim); font-family: var(--mono); font-size: 12px;">sorgu hazırlanıyor</span>`;
  els.thread.appendChild(div);
  scrollToBottom();
  return div;
}

function addAnswerMessage(data) {
  const tpl = document.getElementById("tpl-message-answer");
  const node = tpl.content.cloneNode(true);

  node.querySelector(".sql-code").textContent = data.sql;

  const tableWrap = node.querySelector(".result-table-wrap");
  if (data.rows && data.rows.length) {
    tableWrap.appendChild(buildTable(data.columns, data.rows));
    if (data.row_count > data.rows.length) {
      const note = document.createElement("div");
      note.style.cssText = "font-family: var(--mono); font-size: 11px; color: var(--text-dim); margin-top: 6px;";
      note.textContent = `${data.row_count} satırdan ilk ${data.rows.length} tanesi gösteriliyor.`;
      tableWrap.appendChild(note);
    }
  } else {
    tableWrap.innerHTML = `<div style="color: var(--text-dim); font-size: 13px;">Sonuç bulunamadı.</div>`;
  }

  const chartWrap = node.querySelector(".chart-wrap");
  if (data.chart) {
    const img = document.createElement("img");
    img.src = data.chart;
    chartWrap.appendChild(img);
  }

  node.querySelector(".yorum-block").textContent = data.yorum;

  els.thread.appendChild(node);
  scrollToBottom();
}

function addConfirmMessage(data, question) {
  const tpl = document.getElementById("tpl-message-confirm");
  const node = tpl.content.cloneNode(true);

  node.querySelector(".sql-code").textContent = data.sql;
  node.querySelector(".confirm-aciklama").textContent = data.aciklama || "";

  const uyariEl = node.querySelector(".confirm-uyari");
  if (data.uyari) {
    uyariEl.textContent = "⚠ " + data.uyari;
  } else {
    uyariEl.remove();
  }

  const wrapper = node.querySelector(".msg-confirm");
  const approveBtn = node.querySelector(".btn-approve");
  const rejectBtn = node.querySelector(".btn-reject");

  approveBtn.addEventListener("click", async () => {
    approveBtn.disabled = true;
    approveBtn.textContent = "Çalıştırılıyor...";
    try {
      const res = await fetch("/api/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sql: data.sql }),
      });
      const result = await res.json();
      const actions = wrapper.querySelector(".confirm-actions");
      if (result.ok) {
        actions.innerHTML = `<span style="color: var(--teal); font-family: var(--mono); font-size: 12.5px;">✓ Çalıştırıldı — ${result.affected_rows} satır etkilendi.</span>`;
      } else {
        actions.innerHTML = `<span style="color: var(--red); font-family: var(--mono); font-size: 12.5px;">✗ ${result.error}</span>`;
      }
    } catch (e) {
      approveBtn.textContent = "Hata";
    }
  });

  rejectBtn.addEventListener("click", () => {
    const actions = wrapper.querySelector(".confirm-actions");
    actions.innerHTML = `<span style="color: var(--text-dim); font-family: var(--mono); font-size: 12.5px;">Vazgeçildi.</span>`;
  });

  els.thread.appendChild(node);
  scrollToBottom();
}

function addErrorMessage(text) {
  const tpl = document.getElementById("tpl-message-error");
  const node = tpl.content.cloneNode(true);
  node.querySelector(".msg-error").textContent = "✗ " + text;
  els.thread.appendChild(node);
  scrollToBottom();
}

function buildTable(columns, rows) {
  const table = document.createElement("table");
  table.className = "result-table";

  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  columns.forEach((c) => {
    const th = document.createElement("th");
    th.textContent = c;
    headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    row.forEach((cell) => {
      const td = document.createElement("td");
      td.textContent = cell === null ? "NULL" : cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  return table;
}

function scrollToBottom() {
  els.thread.scrollTop = els.thread.scrollHeight;
}

// ---------- Sayfa yuklenince baglanti durumunu kontrol et ----------

(async function checkStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    if (data.connected) {
      setConnected({
        server: data.info.server,
        database: data.info.database,
        table_count: "?",
        role: data.info.role,
      });
    }
  } catch (e) {
    // sessiz gec
  }
})();
