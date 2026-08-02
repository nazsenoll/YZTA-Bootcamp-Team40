const state = {
  authenticated: false,
  connected: false,
};

const els = {
  authGate: document.getElementById("auth-gate"),
  dbGate: document.getElementById("db-gate"),
  appRoot: document.getElementById("app"),
  loginForm: document.getElementById("login-form"),
  registerForm: document.getElementById("register-form"),
  verifyForm: document.getElementById("verify-form"),
  linkToRegister: document.getElementById("link-to-register"),
  linkToLogin: document.getElementById("link-to-login"),
  linkResendCode: document.getElementById("link-resend-code"),
  btnLogin: document.getElementById("btn-login"),
  loginError: document.getElementById("login-error"),
  btnRegister: document.getElementById("btn-register"),
  registerError: document.getElementById("register-error"),
  btnVerify: document.getElementById("btn-verify"),
  verifyError: document.getElementById("verify-error"),
  verifyEmailLabel: document.getElementById("verify-email-label"),
  btnConnect: document.getElementById("btn-connect"),
  btnDisconnect: document.getElementById("btn-disconnect"),
  btnLogout: document.getElementById("btn-logout"),
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

// ---------- Giris / Kayit / Dogrulama ekranlari arasi gecis ----------

let pendingVerifyEmail = "";

function switchAuthMode(mode) {
  els.loginForm.classList.toggle("hidden", mode !== "login");
  els.registerForm.classList.toggle("hidden", mode !== "register");
  els.verifyForm.classList.toggle("hidden", mode !== "verify");
  els.loginError.textContent = "";
  els.registerError.textContent = "";
  els.verifyError.textContent = "";
}

function goToVerifyScreen(email) {
  pendingVerifyEmail = email;
  els.verifyEmailLabel.textContent = email;
  document.getElementById("verify-code").value = "";
  switchAuthMode("verify");
}

els.linkToRegister.addEventListener("click", (e) => {
  e.preventDefault();
  switchAuthMode("register");
});
els.linkToLogin.addEventListener("click", (e) => {
  e.preventDefault();
  switchAuthMode("login");
});

// ---------- Sifre goster/gizle ----------

document.getElementById("toggle-login-pw").addEventListener("click", () => {
  const pw = document.getElementById("in-app-password");
  pw.type = pw.type === "password" ? "text" : "password";
});

// ---------- Giris (email + sifre) ----------

els.btnLogin.addEventListener("click", async () => {
  const payload = {
    email: document.getElementById("in-email").value,
    password: document.getElementById("in-app-password").value,
    remember: document.getElementById("remember-me").checked,
  };

  els.loginError.textContent = "";
  els.btnLogin.disabled = true;
  els.btnLogin.textContent = "Giriş yapılıyor...";

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!data.ok) {
      if (data.needs_verification) {
        goToVerifyScreen(payload.email.trim().toLowerCase());
        return;
      }
      els.loginError.textContent = data.error || "Giriş yapılamadı.";
      return;
    }

    setAuthenticated();
  } catch (e) {
    els.loginError.textContent = "Sunucuya ulaşılamadı.";
  } finally {
    els.btnLogin.disabled = false;
    els.btnLogin.textContent = "Giriş Yap";
  }
});

// ---------- Kayit (email + sifre + sifre tekrar) ----------

els.btnRegister.addEventListener("click", async () => {
  const email = document.getElementById("reg-email").value.trim();
  const payload = {
    email,
    password: document.getElementById("reg-password").value,
    password_confirm: document.getElementById("reg-password-confirm").value,
  };

  els.registerError.textContent = "";
  els.btnRegister.disabled = true;
  els.btnRegister.textContent = "Kayıt oluşturuluyor...";

  try {
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!data.ok) {
      els.registerError.textContent = data.error || "Kayıt oluşturulamadı.";
      if (data.needs_verification) {
        // Mail gonderimi basarisiz olsa bile kayit DB'de olustu; kullanici
        // "tekrar gonder" ile deneyebilsin diye dogrulama ekranina gecir.
        goToVerifyScreen(email.toLowerCase());
      }
      return;
    }

    goToVerifyScreen(email.toLowerCase());
  } catch (e) {
    els.registerError.textContent = "Sunucuya ulaşılamadı.";
  } finally {
    els.btnRegister.disabled = false;
    els.btnRegister.textContent = "Kayıt Ol";
  }
});

// ---------- E-posta dogrulama (6 haneli kod) ----------

els.btnVerify.addEventListener("click", async () => {
  const code = document.getElementById("verify-code").value.trim();

  els.verifyError.textContent = "";
  els.btnVerify.disabled = true;
  els.btnVerify.textContent = "Doğrulanıyor...";

  try {
    const res = await fetch("/api/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: pendingVerifyEmail, code }),
    });
    const data = await res.json();

    if (!data.ok) {
      els.verifyError.textContent = data.error || "Doğrulama başarısız.";
      return;
    }

    setAuthenticated();
  } catch (e) {
    els.verifyError.textContent = "Sunucuya ulaşılamadı.";
  } finally {
    els.btnVerify.disabled = false;
    els.btnVerify.textContent = "Doğrula";
  }
});

els.linkResendCode.addEventListener("click", async (e) => {
  e.preventDefault();
  els.verifyError.textContent = "";
  els.linkResendCode.textContent = "Gönderiliyor...";

  try {
    const res = await fetch("/api/resend_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: pendingVerifyEmail }),
    });
    const data = await res.json();

    if (!data.ok) {
      els.verifyError.textContent = data.error || "Kod tekrar gönderilemedi.";
      return;
    }
    els.verifyError.style.color = "var(--brand-light)";
    els.verifyError.textContent = "Yeni kod gönderildi.";
  } catch (e) {
    els.verifyError.textContent = "Sunucuya ulaşılamadı.";
  } finally {
    els.linkResendCode.textContent = "Tekrar gönder";
  }
});

els.btnLogout.addEventListener("click", async () => {
  await fetch("/api/logout", { method: "POST" });
  setLoggedOut();
});

document.getElementById("btn-switch-account").addEventListener("click", async () => {
  await fetch("/api/logout", { method: "POST" });
  setLoggedOut();
});

function setAuthenticated() {
  state.authenticated = true;
  els.authGate.classList.add("hidden");
  els.dbGate.classList.remove("hidden");
  document.getElementById("in-app-password").value = "";
  document.getElementById("reg-password").value = "";
  document.getElementById("reg-password-confirm").value = "";
}

function setLoggedOut() {
  state.authenticated = false;
  state.connected = false;
  els.appRoot.classList.add("hidden");
  els.dbGate.classList.add("hidden");
  els.authGate.classList.remove("hidden");
  switchAuthMode("login");
  document.getElementById("in-app-password").value = "";
  document.getElementById("in-password").value = "";
}

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
    els.btnConnect.textContent = "Bağlan →";
  }
});

els.btnDisconnect.addEventListener("click", async () => {
  await fetch("/api/disconnect", { method: "POST" });
  setDisconnected();
});

function setConnected(info) {
  state.connected = true;
  els.dbGate.classList.add("hidden");
  els.appRoot.classList.remove("hidden");
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
  els.appRoot.classList.add("hidden");
  els.dbGate.classList.remove("hidden");
  els.inQuestion.disabled = true;
  els.btnAsk.disabled = true;
  document.getElementById("in-password").value = "";
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
    if (data.truncated) {
      const warn = document.createElement("div");
      warn.style.cssText = "font-family: var(--mono); font-size: 11px; color: var(--amber); margin-top: 4px;";
      warn.textContent = `⚠ Sorgu 500 satır sınırına takıldı, gerçek eşleşen satır sayısı bundan fazla olabilir.`;
      tableWrap.appendChild(warn);
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

// ---------- Sayfa yuklenince once giris, sonra baglanti durumunu kontrol et ----------

(async function checkStatus() {
  try {
    const authRes = await fetch("/api/auth_status");
    const authData = await authRes.json();
    if (!authData.authenticated) {
      return; // varsayilan gorunum zaten login-gate
    }
    setAuthenticated();

    const dbRes = await fetch("/api/status");
    const dbData = await dbRes.json();
    if (dbData.connected) {
      setConnected({
        server: dbData.info.server,
        database: dbData.info.database,
        table_count: "?",
        role: dbData.info.role,
      });
    }
  } catch (e) {
    // sessiz gec
  }
})();
