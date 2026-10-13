"use strict";

const VOICES = [
  {
    name: "Microsoft Mark - English (United States)",
    label: "Microsoft Mark",
  },
  {
    name: "Microsoft Zira - English (United States)",
    label: "Microsoft Zira",
  },
  {
    name: "Google US English",
    label: "Google US English",
  },
];

const PARTS_OF_SPEECH = [
  "noun",
  "verb",
  "adjective",
  "adverb",
  "pronoun",
  "preposition",
  "conjunction",
  "interjection",
  "determiner",
  "article",
  "auxiliary verb",
  "modal verb",
  "phrase",
  "phrasal verb",
  "idiom",
];

const PART_OF_SPEECH_ALIASES = Object.freeze({
  n: "noun",
  "n.": "noun",
  v: "verb",
  "v.": "verb",
  adj: "adjective",
  "adj.": "adjective",
  adv: "adverb",
  "adv.": "adverb",
  pron: "pronoun",
  "pron.": "pronoun",
  prep: "preposition",
  "prep.": "preposition",
  conj: "conjunction",
  "conj.": "conjunction",
  interj: "interjection",
  "interj.": "interjection",
  int: "interjection",
  "int.": "interjection",
  det: "determiner",
  "det.": "determiner",
  art: "article",
  "art.": "article",
  aux: "auxiliary verb",
  "aux.": "auxiliary verb",
  auxiliary: "auxiliary verb",
  modal: "modal verb",
  "modal.": "modal verb",
  "phr v": "phrasal verb",
  "phr. v.": "phrasal verb",
});

const ROUTE_META = {
  dashboard: ["Không gian học của bạn", "Hôm nay"],
  library: ["Mọi từ bạn đã thêm", "Thư viện từ vựng"],
  formulas: ["Ghi lại cấu trúc cần nhớ", "Sổ công thức"],
  add: ["Mở rộng vốn từ", "Thêm từ vựng"],
  settings: ["Cá nhân hoá trải nghiệm", "Cài đặt"],
};

const state = {
  route: "dashboard",
  stats: null,
  voiceName: "Microsoft Zira - English (United States)",
  browserVoices: [],
  library: {
    items: [],
    page: 1,
    pages: 0,
    total: 0,
    q: "",
    status: "all",
    partOfSpeech: "",
  },
  formulas: {
    items: [],
    total: 0,
    loading: false,
    error: "",
    editingId: null,
  },
  bulkRows: [],
  bulkPosAutocomplete: {
    open: false,
    items: [],
    activeIndex: -1,
  },
  selectedWord: null,
  study: null,
};

const el = (id) => document.getElementById(id);

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sleep(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

async function api(path, options = {}) {
  const config = {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  };
  const response = await fetch(path, config);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(payload.error || "Không thể hoàn tất yêu cầu.");
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
}

function toast(title, message = "", type = "success") {
  const item = document.createElement("div");
  item.className = `toast ${type}`;
  item.innerHTML = `<div><strong>${escapeHtml(title)}</strong>${message ? `<span>${escapeHtml(message)}</span>` : ""}</div>`;
  el("toastStack").appendChild(item);
  window.setTimeout(() => item.remove(), 3800);
}

function debounce(fn, delay = 250) {
  let timer;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), delay);
  };
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const target = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[target]] = [copy[target], copy[index]];
  }
  return copy;
}

function cleanExampleList(values) {
  const seen = new Set();
  return (values || []).reduce((items, value) => {
    const text = String(value ?? "").trim().replace(/\s+/g, " ");
    const key = text.normalize("NFKC").toLocaleLowerCase("en-US");
    if (!text || seen.has(key)) return items;
    seen.add(key);
    items.push(text);
    return items;
  }, []);
}

function parseExampleLines(value) {
  return cleanExampleList(String(value ?? "").split(/\r?\n/));
}

function parseBulkExamples(value) {
  return cleanExampleList(String(value ?? "").split(/\s*\|\|\s*/));
}

function parseItemLines(value) {
  return cleanExampleList(String(value ?? "").split(/\r?\n/));
}

function parseBulkItems(value) {
  return cleanExampleList(String(value ?? "").split(/\s*\|\|\s*/));
}

function wordExamples(word) {
  const current = Array.isArray(word?.examples)
    ? cleanExampleList(word.examples)
    : parseExampleLines(word?.examples);
  if (current.length) return current;
  return cleanExampleList([word?.example]);
}

function wordUsageItems(word, arrayKey, legacyKey) {
  if (Array.isArray(word?.[arrayKey])) return cleanExampleList(word[arrayKey]);
  return cleanExampleList(String(word?.[legacyKey] || "").split(/\r?\n|\s*\|\|\s*/));
}

function randomItem(items) {
  return items.length ? items[Math.floor(Math.random() * items.length)] : null;
}

function libraryContentBlockHtml(label, items, emptyLabel) {
  const cleanedItems = cleanExampleList(items);
  const visibleItems = cleanedItems.slice(0, 2);
  return `<section class="library-content-block">
    <h4>${escapeHtml(label)}</h4>
    ${visibleItems.length
      ? `<ul>${visibleItems.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
      : `<p class="library-content-empty">${escapeHtml(emptyLabel)}</p>`}
    ${cleanedItems.length > visibleItems.length
      ? `<small class="library-content-count">+${cleanedItems.length - visibleItems.length} mục khác</small>`
      : ""}
  </section>`;
}

function libraryContentHtml(word) {
  return `<div class="library-content-grid">
    ${libraryContentBlockHtml("Ví dụ", wordExamples(word), "Chưa có ví dụ")}
    ${libraryContentBlockHtml("Collocation", wordUsageItems(word, "collocations", "collocation"), "Chưa có collocation")}
    ${libraryContentBlockHtml("Word pattern", wordUsageItems(word, "word_patterns", "word_pattern"), "Chưa có word pattern")}
  </div>`;
}

function formatNumber(value) {
  return new Intl.NumberFormat("vi-VN").format(value || 0);
}

function toDate(value) {
  return value ? new Date(value) : null;
}

function relativeTime(value) {
  const date = toDate(value);
  if (!date || Number.isNaN(date.getTime())) return "—";
  const diff = date.getTime() - Date.now();
  const abs = Math.abs(diff);
  if (abs < 60_000) return diff <= 0 ? "Đến hạn" : "Dưới 1 phút";
  const units = [
    [86_400_000, "ngày"],
    [3_600_000, "giờ"],
    [60_000, "phút"],
  ];
  for (const [size, label] of units) {
    if (abs >= size) {
      const amount = Math.max(1, Math.round(abs / size));
      return diff < 0 ? `Quá hạn ${amount} ${label}` : `Sau ${amount} ${label}`;
    }
  }
  return "Sắp đến hạn";
}

function fullDateTime(value) {
  const date = toDate(value);
  if (!date || Number.isNaN(date.getTime())) return "Chưa có lịch";
  return new Intl.DateTimeFormat("vi-VN", {
    weekday: "short",
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function normalizeAnswer(value) {
  return String(value ?? "")
    .normalize("NFKC")
    .toLocaleLowerCase("en-US")
    .replace(/[‘’]/g, "'")
    .replace(/\s+/g, " ")
    .replace(/[.!?]+$/g, "")
    .trim();
}

function normalizePartOfSpeech(value) {
  const cleaned = String(value ?? "")
    .normalize("NFKC")
    .replace(/\s+/g, " ")
    .trim();
  const lookup = cleaned.toLocaleLowerCase("en-US");
  if (PART_OF_SPEECH_ALIASES[lookup]) return PART_OF_SPEECH_ALIASES[lookup];
  return PARTS_OF_SPEECH.includes(lookup) ? lookup : cleaned;
}

function setRoute(route) {
  if (!ROUTE_META[route]) return;
  state.route = route;
  document.querySelectorAll("[data-view]").forEach((view) => {
    view.classList.toggle("active", view.dataset.view === route);
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    const active = button.dataset.route === route;
    button.classList.toggle("active", active);
    if (active) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  el("pageEyebrow").textContent = ROUTE_META[route][0];
  el("pageTitle").textContent = ROUTE_META[route][1];
  window.scrollTo({ top: 0, behavior: "smooth" });
  if (route === "dashboard") loadStats();
  if (route === "library") loadLibrary();
  if (route === "formulas") loadFormulas();
  if (route === "settings") refreshVoiceAvailability();
}

function setFormulaEditorMode(formula = null) {
  const contentField = el("formulaContent");
  const cancelButton = el("formulaCancelEditButton");
  const saveButton = el("formulaSaveButton");
  if (!contentField || !cancelButton || !saveButton) return;

  if (formula) {
    state.formulas.editingId = formula.id;
    contentField.value = formula.content;
    el("formulaEditorEyebrow").textContent = "Đang chỉnh sửa";
    el("formulaEditorTitle").textContent = "Sửa công thức";
    saveButton.textContent = "Lưu thay đổi";
    cancelButton.classList.remove("hidden");
  } else {
    state.formulas.editingId = null;
    el("formulaForm").reset();
    el("formulaEditorEyebrow").textContent = "Ghi chú mới";
    el("formulaEditorTitle").textContent = "Thêm công thức";
    saveButton.textContent = "Thêm công thức";
    cancelButton.classList.add("hidden");
  }
}

function renderFormulas() {
  const loading = el("formulasLoading");
  const error = el("formulasError");
  const empty = el("formulasEmpty");
  const list = el("formulaList");
  const count = el("formulaCount");
  if (!loading || !error || !empty || !list || !count) return;

  loading.classList.toggle("hidden", !state.formulas.loading);
  error.classList.toggle("hidden", state.formulas.loading || !state.formulas.error);
  empty.classList.toggle(
    "hidden",
    state.formulas.loading || Boolean(state.formulas.error) || state.formulas.items.length > 0,
  );
  list.classList.toggle(
    "hidden",
    state.formulas.loading || Boolean(state.formulas.error) || state.formulas.items.length === 0,
  );
  count.textContent = `${formatNumber(state.formulas.total)} ghi chú`;
  el("formulasErrorMessage").textContent = state.formulas.error || "Vui lòng thử lại.";

  list.replaceChildren();
  if (state.formulas.loading || state.formulas.error) return;

  state.formulas.items.forEach((formula, index) => {
    const card = document.createElement("article");
    card.className = "formula-card";

    const number = document.createElement("span");
    number.className = "formula-card-number";
    number.textContent = String(index + 1).padStart(2, "0");

    const content = document.createElement("p");
    content.className = "formula-note-content";
    content.textContent = formula.content;

    const actions = document.createElement("div");
    actions.className = "formula-card-actions";

    const editButton = document.createElement("button");
    editButton.className = "secondary-button formula-action-button";
    editButton.type = "button";
    editButton.textContent = "Sửa";
    editButton.setAttribute("aria-label", `Sửa công thức số ${index + 1}`);
    editButton.addEventListener("click", () => {
      setFormulaEditorMode(formula);
      el("formulaForm").scrollIntoView({ behavior: "smooth", block: "start" });
      window.setTimeout(() => el("formulaContent").focus(), 220);
    });

    const deleteButton = document.createElement("button");
    deleteButton.className = "danger-text-button formula-action-button";
    deleteButton.type = "button";
    deleteButton.textContent = "Xoá";
    deleteButton.setAttribute("aria-label", `Xoá công thức số ${index + 1}`);
    deleteButton.addEventListener("click", async () => {
      const approved = await askConfirm({
        title: "Xoá công thức này?",
        message: "Ghi chú này sẽ bị xoá khỏi Sổ công thức và không thể khôi phục.",
        confirmText: "Xoá công thức",
      });
      if (!approved) return;

      deleteButton.disabled = true;
      try {
        await api(`/api/formulas/${formula.id}`, { method: "DELETE" });
        if (state.formulas.editingId === formula.id) setFormulaEditorMode();
        toast("Đã xoá công thức");
        await loadFormulas();
      } catch (deleteError) {
        toast("Chưa thể xoá công thức", deleteError.message, "error");
      } finally {
        deleteButton.disabled = false;
      }
    });

    actions.append(editButton, deleteButton);
    card.append(number, content, actions);
    list.appendChild(card);
  });
}

async function loadFormulas() {
  if (!el("formulaList")) return;
  state.formulas.loading = true;
  state.formulas.error = "";
  renderFormulas();
  try {
    const result = await api("/api/formulas");
    state.formulas.items = Array.isArray(result.items)
      ? result.items.map((formula) => ({
        id: Number(formula.id),
        content: String(formula.content ?? ""),
        createdAt: formula.created_at || null,
        updatedAt: formula.updated_at || null,
      }))
      : [];
    state.formulas.total = Number.isFinite(Number(result.total))
      ? Number(result.total)
      : state.formulas.items.length;
  } catch (loadError) {
    state.formulas.items = [];
    state.formulas.total = 0;
    state.formulas.error = loadError.message;
  } finally {
    state.formulas.loading = false;
    renderFormulas();
  }
}

async function saveFormula(event) {
  event.preventDefault();
  const contentField = el("formulaContent");
  const saveButton = el("formulaSaveButton");
  const cancelButton = el("formulaCancelEditButton");
  const content = contentField.value.trim();
  if (!content) {
    contentField.focus();
    return;
  }

  const editingId = state.formulas.editingId;
  saveButton.disabled = true;
  cancelButton.disabled = true;
  saveButton.textContent = "Đang lưu…";
  try {
    const path = editingId ? `/api/formulas/${editingId}` : "/api/formulas";
    await api(path, {
      method: editingId ? "PUT" : "POST",
      body: JSON.stringify({ content }),
    });
    setFormulaEditorMode();
    toast(editingId ? "Đã lưu thay đổi" : "Đã thêm công thức");
    await loadFormulas();
    if (!editingId) contentField.focus();
  } catch (saveError) {
    toast("Chưa thể lưu công thức", saveError.message, "error");
    saveButton.textContent = editingId ? "Lưu thay đổi" : "Thêm công thức";
  } finally {
    saveButton.disabled = false;
    cancelButton.disabled = false;
  }
}

function renderSchedule(schedule = []) {
  const horizontal = schedule
    .map(
      (step) => `
      <div class="schedule-step">
        <span class="schedule-dot">${step.stage + 1}</span>
        <span>${escapeHtml(step.label)}</span>
      </div>`,
    )
    .join("");
  el("dashboardSchedule").innerHTML = horizontal;

  el("settingsSchedule").innerHTML = schedule
    .map(
      (step) => `
      <div class="vertical-step">
        <span>${step.stage + 1}</span>
        <span>Mốc ${step.stage + 1} · <strong>${escapeHtml(step.label)}</strong></span>
      </div>`,
    )
    .join("");
}

async function loadStats() {
  try {
    const stats = await api("/api/stats");
    state.stats = stats;
    el("todayReviewCount").textContent = formatNumber(stats.reviewed_today);
    el("dueBadge").textContent = `${formatNumber(stats.due)} từ`;
    el("newBadge").textContent = `${formatNumber(stats.new + stats.learning)} từ`;
    el("statTotal").textContent = formatNumber(stats.total);
    el("statLearned").textContent = formatNumber(stats.learned);
    el("statLearning").textContent = formatNumber(stats.learning);
    el("statAccuracy").textContent = stats.accuracy_today === null ? "—" : `${stats.accuracy_today}%`;

    if (stats.due > 0) {
      el("reviewActionDescription").textContent = `${stats.due} từ đang chờ bạn củng cố ngay bây giờ.`;
      el("startReviewButton").disabled = false;
      el("startReviewButton").textContent = `Ôn ${stats.due} từ`;
    } else {
      el("reviewActionDescription").textContent = stats.learned
        ? "Bạn đã hoàn tất các lượt ôn đang đến hạn."
        : "Học xong từ mới để tạo lịch ôn đầu tiên.";
      el("startReviewButton").disabled = true;
      el("startReviewButton").textContent = "Chưa có từ đến hạn";
    }

    if (stats.speed_available) {
      el("speedBadge").textContent = `${formatNumber(stats.due)} từ · 3 tim`;
      el("speedActionDescription").textContent = `${stats.due} từ đã đến hạn. Trả lời trước khi đồng hồ về 0.`;
      el("startSpeedReviewButton").disabled = false;
      el("startSpeedReviewButton").textContent = "Bắt đầu Ôn siêu tốc";
    } else if (stats.learned < stats.speed_minimum_learned) {
      const remaining = stats.speed_minimum_learned - stats.learned;
      el("speedBadge").textContent = `${stats.learned} / ${stats.speed_minimum_learned} từ`;
      el("speedActionDescription").textContent = `Học xong thêm ${remaining} từ để mở chế độ này.`;
      el("startSpeedReviewButton").disabled = true;
      el("startSpeedReviewButton").textContent = "Cần ít nhất 3 từ đã học";
    } else {
      el("speedBadge").textContent = "3 tim";
      el("speedActionDescription").textContent = "Không có từ đang đến hạn. Từ chưa đến hạn sẽ không bị đưa vào.";
      el("startSpeedReviewButton").disabled = true;
      el("startSpeedReviewButton").textContent = "Chưa có từ đến hạn";
    }

    const availableToLearn = stats.new + stats.learning;
    if (availableToLearn > 0) {
      const amount = Math.min(5, availableToLearn);
      el("learnActionDescription").textContent = `${availableToLearn} từ đang chờ trong hàng học mới.`;
      el("startLearnButton").disabled = false;
      el("startLearnButton").textContent = `Học ${amount} từ mới`;
    } else {
      el("learnActionDescription").textContent = stats.total
        ? "Mọi từ trong thư viện đều đã qua giai đoạn học mới."
        : "Thêm từ vào thư viện để bắt đầu.";
      el("startLearnButton").disabled = true;
      el("startLearnButton").textContent = "Không có từ mới";
    }

    if (stats.due > 0) {
      el("nextReviewTime").textContent = "Ngay bây giờ";
      el("nextReviewHint").textContent = `${stats.due} từ đã đến hạn.`;
    } else if (stats.next_due_at) {
      el("nextReviewTime").textContent = relativeTime(stats.next_due_at);
      el("nextReviewHint").textContent = fullDateTime(stats.next_due_at);
    } else {
      el("nextReviewTime").textContent = "Chưa có lịch ôn";
      el("nextReviewHint").textContent = "Học xong một từ để tạo lịch đầu tiên.";
    }
    renderSchedule(stats.schedule);
  } catch (error) {
    toast("Không tải được bảng hôm nay", error.message, "error");
  }
}

function statusMeta(word) {
  const progress = word.progress;
  if (progress.state === "new") return ["Chưa học", "new"];
  if (progress.state === "learning") return [`Đang học ${progress.learning_step}/6`, "learning"];
  const due = progress.next_review_at && toDate(progress.next_review_at).getTime() <= Date.now();
  if (due) return ["Đến hạn", `due${progress.is_difficult ? " difficult" : ""}`];
  if (progress.is_difficult) return ["Cần củng cố", "learned difficult"];
  return ["Đã học", "learned"];
}

async function loadLibrary(page = state.library.page) {
  const query = new URLSearchParams({
    page: String(page),
    per_page: "20",
    q: state.library.q,
    status: state.library.status,
    part_of_speech: state.library.partOfSpeech,
  });
  try {
    const result = await api(`/api/words?${query}`);
    Object.assign(state.library, {
      items: result.items,
      page: result.page,
      pages: result.pages,
      total: result.total,
    });
    renderLibrary(result);
  } catch (error) {
    toast("Không tải được thư viện", error.message, "error");
  }
}

function renderLibrary(result) {
  el("libraryTotal").textContent = formatNumber(result.total);
  const body = el("libraryTableBody");
  const empty = el("libraryEmpty");
  body.innerHTML = "";
  empty.classList.toggle("hidden", result.items.length > 0);

  result.items.forEach((word) => {
    const [statusLabel, statusClass] = statusMeta(word);
    const row = document.createElement("tr");
    row.className = "library-main-row";
    row.dataset.wordId = String(word.id);
    row.tabIndex = 0;
    const wordPartOfSpeech = normalizePartOfSpeech(word.part_of_speech);
    row.setAttribute("aria-label", `Mở từ ${word.english}${wordPartOfSpeech ? `, ${wordPartOfSpeech}` : ""}`);
    row.innerHTML = `
      <td class="word-cell">
        <strong>${escapeHtml(word.english)}</strong>
        <small class="phonetic-text">${escapeHtml(word.phonetic || "Chưa có phiên âm")}</small>
      </td>
      <td>${escapeHtml(word.vietnamese)}</td>
      <td>${wordPartOfSpeech ? `<span class="pos-chip">${escapeHtml(wordPartOfSpeech)}</span>` : "<span class='muted'>—</span>"}</td>
      <td><span class="status-chip ${statusClass}">${escapeHtml(statusLabel)}</span></td>
      <td><span title="${escapeHtml(fullDateTime(word.progress.next_review_at))}">${word.progress.next_review_at ? escapeHtml(relativeTime(word.progress.next_review_at)) : "—"}</span></td>
      <td><button class="row-action" type="button" aria-label="Mở chi tiết ${escapeHtml(word.english)}${wordPartOfSpeech ? `, ${escapeHtml(wordPartOfSpeech)}` : ""}">•••</button></td>`;
    const contentRow = document.createElement("tr");
    contentRow.className = "library-content-row";
    contentRow.dataset.wordId = String(word.id);
    contentRow.innerHTML = `<td colspan="6">${libraryContentHtml(word)}</td>`;
    const open = () => openWordDialog(word);
    row.addEventListener("click", open);
    contentRow.addEventListener("click", open);
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
    body.appendChild(row);
    body.appendChild(contentRow);
  });

  const currentPos = state.library.partOfSpeech;
  const posFilter = el("posFilter");
  posFilter.innerHTML = '<option value="">Tất cả loại từ</option>' + result.part_of_speech_options
    .map((part) => `<option value="${escapeHtml(part)}">${escapeHtml(part)}</option>`)
    .join("");
  posFilter.value = currentPos;
  renderPagination(result.page, result.pages);
}

function renderPagination(current, pages) {
  const container = el("libraryPagination");
  container.innerHTML = "";
  if (pages <= 1) return;
  const candidates = new Set([1, pages, current - 1, current, current + 1]);
  const pageList = [...candidates].filter((page) => page >= 1 && page <= pages).sort((a, b) => a - b);
  let previous = 0;
  pageList.forEach((page) => {
    if (page - previous > 1) {
      const dots = document.createElement("span");
      dots.className = "page-button";
      dots.textContent = "…";
      container.appendChild(dots);
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = `page-button${page === current ? " active" : ""}`;
    button.textContent = String(page);
    button.setAttribute("aria-label", `Trang ${page}`);
    button.addEventListener("click", () => loadLibrary(page));
    container.appendChild(button);
    previous = page;
  });
}

function switchAddTab(tab) {
  const single = tab === "single";
  if (single) closeBulkPosSuggestions();
  el("singleTab").classList.toggle("active", single);
  el("bulkTab").classList.toggle("active", !single);
  el("singleTab").setAttribute("aria-selected", String(single));
  el("bulkTab").setAttribute("aria-selected", String(!single));
  el("singleAddPanel").classList.toggle("hidden", !single);
  el("bulkAddPanel").classList.toggle("hidden", single);
  window.setTimeout(() => (single ? el("singleEnglish") : el("bulkInput")).focus(), 50);
}

function formToObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function wordFormPayload(form) {
  const payload = formToObject(form);
  payload.part_of_speech = normalizePartOfSpeech(payload.part_of_speech);
  payload.collocations = parseItemLines(payload.collocations ?? payload.collocation);
  payload.word_patterns = parseItemLines(payload.word_patterns ?? payload.word_pattern);
  payload.collocation = payload.collocations.join("\n");
  payload.word_pattern = payload.word_patterns.join("\n");
  payload.examples = parseExampleLines(payload.examples);
  return payload;
}

async function submitSingleWord(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const mode = event.submitter?.value || "save";
  const payload = wordFormPayload(form);
  try {
    await api("/api/words", { method: "POST", body: JSON.stringify(payload) });
    toast("Đã thêm từ", `${payload.english} đã có trong thư viện.`);
    form.reset();
    localStorage.removeItem("lexiloop-word-draft");
    await loadStats();
    if (mode === "continue") el("singleEnglish").focus();
    else setRoute("library");
  } catch (error) {
    toast("Chưa thể thêm từ", error.message, "error");
  }
}

function saveSingleDraft() {
  const data = formToObject(el("singleWordForm"));
  if (Object.values(data).some(Boolean)) localStorage.setItem("lexiloop-word-draft", JSON.stringify(data));
  else localStorage.removeItem("lexiloop-word-draft");
}

function restoreSingleDraft() {
  try {
    const draft = JSON.parse(localStorage.getItem("lexiloop-word-draft") || "null");
    if (!draft) return;
    Object.entries(draft).forEach(([key, value]) => {
      let migratedKey = key;
      if (key === "example" && !draft.examples) migratedKey = "examples";
      if (key === "collocation" && !draft.collocations) migratedKey = "collocations";
      if (key === "word_pattern" && !draft.word_patterns) migratedKey = "word_patterns";
      const legacyFallback = migratedKey === "collocations"
        ? "collocation"
        : migratedKey === "word_patterns"
          ? "word_pattern"
          : "";
      const input = el("singleWordForm").elements.namedItem(migratedKey)
        || (legacyFallback ? el("singleWordForm").elements.namedItem(legacyFallback) : null);
      if (input) input.value = Array.isArray(value) ? value.join("\n") : value;
    });
  } catch (_error) {
    localStorage.removeItem("lexiloop-word-draft");
  }
}

function parseDelimitedLine(line, delimiter) {
  const cells = [];
  let current = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === delimiter && !quoted) {
      cells.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current.trim());
  return cells;
}

const BULK_EXAMPLE_SEPARATOR_PLACEHOLDER = "\uE000";

function parseBulkDelimitedLine(line, delimiter) {
  if (delimiter !== "|") return parseDelimitedLine(line, delimiter);
  const protectedLine = line.replaceAll("||", BULK_EXAMPLE_SEPARATOR_PLACEHOLDER);
  return parseDelimitedLine(protectedLine, delimiter)
    .map((cell) => cell.replaceAll(BULK_EXAMPLE_SEPARATOR_PLACEHOLDER, "||"));
}

function getBulkPartOfSpeechField(input = el("bulkInput")) {
  const cursor = input.selectionStart;
  if (cursor !== input.selectionEnd) return null;
  const lineStart = input.value.lastIndexOf("\n", Math.max(0, cursor - 1)) + 1;
  const nextLineBreak = input.value.indexOf("\n", cursor);
  const lineEnd = nextLineBreak === -1 ? input.value.length : nextLineBreak;
  const beforeCursor = input.value.slice(lineStart, cursor);
  const column = (beforeCursor.match(/\t/g) || []).length;
  if (column !== 3) return null;
  const previousTab = input.value.lastIndexOf("\t", Math.max(lineStart, cursor - 1));
  const fieldStart = previousTab + 1;
  const nextTab = input.value.indexOf("\t", cursor);
  const fieldEnd = nextTab !== -1 && nextTab < lineEnd ? nextTab : lineEnd;
  return {
    start: fieldStart,
    end: fieldEnd,
    query: input.value.slice(fieldStart, cursor).trim(),
  };
}

function getBulkCaretCoordinates(input) {
  const style = window.getComputedStyle(input);
  const mirror = document.createElement("div");
  const copiedProperties = [
    "borderTopWidth",
    "borderRightWidth",
    "borderBottomWidth",
    "borderLeftWidth",
    "fontFamily",
    "fontSize",
    "fontStyle",
    "fontWeight",
    "letterSpacing",
    "lineHeight",
    "paddingTop",
    "paddingRight",
    "paddingBottom",
    "paddingLeft",
    "textIndent",
    "textTransform",
    "wordSpacing",
  ];
  mirror.style.position = "absolute";
  mirror.style.visibility = "hidden";
  mirror.style.top = "0";
  mirror.style.left = "-9999px";
  mirror.style.width = `${input.clientWidth}px`;
  mirror.style.boxSizing = "border-box";
  mirror.style.whiteSpace = "pre-wrap";
  mirror.style.overflowWrap = "break-word";
  copiedProperties.forEach((property) => {
    mirror.style[property] = style[property];
  });
  mirror.textContent = input.value.slice(0, input.selectionStart);
  if (mirror.textContent.endsWith("\n")) mirror.textContent += " ";
  const marker = document.createElement("span");
  marker.textContent = "\u200b";
  mirror.appendChild(marker);
  document.body.appendChild(mirror);
  const coordinates = {
    left: marker.offsetLeft - input.scrollLeft,
    top: marker.offsetTop - input.scrollTop,
    lineHeight: Number.parseFloat(style.lineHeight) || 20,
  };
  mirror.remove();
  return coordinates;
}

function positionBulkPosSuggestions() {
  const input = el("bulkInput");
  const menu = el("bulkPosSuggestions");
  if (!state.bulkPosAutocomplete.open) return;
  const caret = getBulkCaretCoordinates(input);
  const menuWidth = menu.offsetWidth || 245;
  const menuHeight = menu.offsetHeight || 180;
  const maxLeft = Math.max(8, input.clientWidth - menuWidth - 8);
  const left = Math.max(8, Math.min(caret.left, maxLeft));
  let top = caret.top + caret.lineHeight + 5;
  if (top + menuHeight > input.clientHeight && caret.top > menuHeight) {
    top = caret.top - menuHeight - 5;
  }
  menu.style.left = `${left}px`;
  menu.style.top = `${Math.max(5, top)}px`;
}

function closeBulkPosSuggestions() {
  const menu = el("bulkPosSuggestions");
  if (!menu) return;
  state.bulkPosAutocomplete.open = false;
  state.bulkPosAutocomplete.items = [];
  state.bulkPosAutocomplete.activeIndex = -1;
  menu.classList.add("hidden");
  el("bulkInput")?.setAttribute("aria-expanded", "false");
  el("bulkInput")?.removeAttribute("aria-activedescendant");
}

function renderBulkPosSuggestions() {
  const menu = el("bulkPosSuggestions");
  const autocomplete = state.bulkPosAutocomplete;
  if (!autocomplete.open) {
    closeBulkPosSuggestions();
    return;
  }
  if (!autocomplete.items.length) {
    menu.innerHTML = '<p class="bulk-pos-empty">Không có gợi ý phù hợp · bạn vẫn có thể nhập tự do</p>';
  } else {
    menu.innerHTML = autocomplete.items.map((item, index) => `
      <button class="bulk-pos-option${index === autocomplete.activeIndex ? " active" : ""}"
        id="bulkPosOption${index}" type="button" role="option" data-pos-index="${index}"
        aria-selected="${index === autocomplete.activeIndex}">${escapeHtml(item)}</button>`).join("");
    menu.querySelectorAll(".bulk-pos-option").forEach((button) => {
      button.addEventListener("mousedown", (event) => {
        event.preventDefault();
        chooseBulkPartOfSpeech(Number(button.dataset.posIndex), true);
      });
    });
  }
  menu.classList.remove("hidden");
  el("bulkInput").setAttribute("aria-expanded", "true");
  if (autocomplete.activeIndex >= 0) {
    el("bulkInput").setAttribute("aria-activedescendant", `bulkPosOption${autocomplete.activeIndex}`);
  } else {
    el("bulkInput").removeAttribute("aria-activedescendant");
  }
  positionBulkPosSuggestions();
}

function refreshBulkPosSuggestions() {
  const field = getBulkPartOfSpeechField();
  if (!field) {
    closeBulkPosSuggestions();
    return;
  }
  const query = field.query.toLocaleLowerCase("en-US");
  const startsWith = PARTS_OF_SPEECH.filter((item) => item.startsWith(query));
  const contains = PARTS_OF_SPEECH.filter((item) => !item.startsWith(query) && item.includes(query));
  state.bulkPosAutocomplete.open = true;
  state.bulkPosAutocomplete.items = [...startsWith, ...contains];
  state.bulkPosAutocomplete.activeIndex = query ? (state.bulkPosAutocomplete.items.length ? 0 : -1) : -1;
  renderBulkPosSuggestions();
}

function moveBulkPosSelection(direction) {
  const autocomplete = state.bulkPosAutocomplete;
  if (!autocomplete.items.length) return;
  if (autocomplete.activeIndex < 0) {
    autocomplete.activeIndex = direction > 0 ? 0 : autocomplete.items.length - 1;
  } else {
    autocomplete.activeIndex = (
      autocomplete.activeIndex + direction + autocomplete.items.length
    ) % autocomplete.items.length;
  }
  renderBulkPosSuggestions();
  el(`bulkPosOption${autocomplete.activeIndex}`)?.scrollIntoView({ block: "nearest" });
}

function chooseBulkPartOfSpeech(index, advanceToExample) {
  const input = el("bulkInput");
  const field = getBulkPartOfSpeechField(input);
  const choice = state.bulkPosAutocomplete.items[index];
  if (!field || !choice) return;
  input.setRangeText(choice, field.start, field.end, "end");
  let cursor = field.start + choice.length;
  if (advanceToExample) {
    if (input.value[cursor] !== "\t") {
      input.setRangeText("\t", cursor, cursor, "end");
    } else {
      cursor += 1;
      input.setSelectionRange(cursor, cursor);
    }
  }
  input.dispatchEvent(new Event("input", { bubbles: true }));
  closeBulkPosSuggestions();
  input.focus();
}

function insertTabIntoBulkInput(event) {
  const autocomplete = state.bulkPosAutocomplete;
  if (autocomplete.open && event.key === "ArrowDown") {
    event.preventDefault();
    moveBulkPosSelection(1);
    return;
  }
  if (autocomplete.open && event.key === "ArrowUp") {
    event.preventDefault();
    moveBulkPosSelection(-1);
    return;
  }
  if (autocomplete.open && event.key === "Escape") {
    event.preventDefault();
    closeBulkPosSuggestions();
    return;
  }
  if (
    autocomplete.open
    && autocomplete.activeIndex >= 0
    && (event.key === "Enter" || (event.key === "Tab" && !event.shiftKey))
  ) {
    event.preventDefault();
    chooseBulkPartOfSpeech(autocomplete.activeIndex, true);
    return;
  }
  if (event.key !== "Tab" || event.shiftKey || event.ctrlKey || event.altKey || event.metaKey) return;
  event.preventDefault();
  const input = event.currentTarget;
  const start = input.selectionStart;
  const end = input.selectionEnd;
  const scrollTop = input.scrollTop;
  input.setRangeText("\t", start, end, "end");
  input.scrollTop = scrollTop;
  input.dispatchEvent(new Event("input", { bubbles: true }));
}

function countUnquotedDelimiter(line, delimiter) {
  let count = 0;
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    if (line[index] === '"') {
      if (quoted && line[index + 1] === '"') index += 1;
      else quoted = !quoted;
    } else if (!quoted && line[index] === delimiter) {
      count += 1;
    }
  }
  return count;
}

function detectDelimiter(lines) {
  const samples = lines.slice(0, 5);
  if (samples.some((line) => countUnquotedDelimiter(line, "\t") > 0)) return "\t";

  const scores = samples.reduce(
    (result, line) => {
      const protectedLine = line.replaceAll("||", BULK_EXAMPLE_SEPARATOR_PLACEHOLDER);
      result.pipe += countUnquotedDelimiter(protectedLine, "|");
      result.comma += countUnquotedDelimiter(protectedLine, ",");
      return result;
    },
    { pipe: 0, comma: 0 },
  );
  if (scores.pipe > scores.comma) return "|";
  return scores.comma ? "," : "\t";
}

function splitBulkRecords(value) {
  const records = [];
  let current = "";
  let quoted = false;
  const source = String(value || "");
  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    if (char === '"') {
      current += char;
      if (quoted && source[index + 1] === '"') {
        current += source[index + 1];
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && source[index + 1] === "\n") index += 1;
      if (current.trim()) records.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  if (current.trim()) records.push(current);
  return records;
}

function parseBulkInput() {
  const lines = splitBulkRecords(el("bulkInput").value);
  const delimiter = detectDelimiter(lines);
  const firstCells = lines.length ? parseBulkDelimitedLine(lines[0], delimiter) : [];
  const isOldLibraryExport = /^(examples?|câu ví dụ)/i.test(firstCells[4] || "")
    && /^(state|trạng thái)$/i.test(firstCells[5] || "")
    && /^(next review|ôn tiếp)$/i.test(firstCells[6] || "");
  const isNewLibraryExport = /^(examples?|câu ví dụ)/i.test(firstCells[4] || "")
    && /^collocations?\b/i.test(firstCells[5] || "")
    && /^(?:word[ _-]?patterns?|mẫu từ)(?:\s|\(|$)/i.test(firstCells[6] || "")
    && /^(state|trạng thái)$/i.test(firstCells[7] || "")
    && /^(next review|ôn tiếp)$/i.test(firstCells[8] || "");
  const isMultilineListExport = isNewLibraryExport
    && /(?:one per line|mỗi dòng)/i.test(firstCells[5] || "")
    && /(?:one per line|mỗi dòng)/i.test(firstCells[6] || "");
  const seen = new Set();
  state.bulkRows = lines.map((line, index) => {
    const cells = parseBulkDelimitedLine(line, delimiter);
    // Six cells already means the optional Collocation column is present;
    // Word pattern may legitimately be left empty.
    const usesNewFormat = isNewLibraryExport || (!isOldLibraryExport && cells.length >= 6);
    const exampleText = (
      isOldLibraryExport || usesNewFormat ? (cells[4] || "") : cells.slice(4).join(delimiter)
    ).trim();
    const record = {
      english: (cells[0] || "").trim(),
      phonetic: (cells[1] || "").trim(),
      vietnamese: (cells[2] || "").trim(),
      part_of_speech: normalizePartOfSpeech(cells[3]),
      examples: parseBulkExamples(exampleText),
      collocations: usesNewFormat
        ? (isMultilineListExport ? parseItemLines(cells[5]) : parseBulkItems(cells[5]))
        : [],
      word_patterns: usesNewFormat
        ? (isMultilineListExport ? parseItemLines(cells[6]) : parseBulkItems(cells[6]))
        : [],
    };
    const header = index === 0
      && /^(english|tiếng anh)$/i.test(record.english)
      && /^(phonetic|phiên âm|ipa)$/i.test(record.phonetic)
      && /^(vietnamese|nghĩa|tiếng việt)$/i.test(record.vietnamese);
    const key = [
      normalizeAnswer(record.english),
      normalizeAnswer(normalizePartOfSpeech(record.part_of_speech)),
      normalizeAnswer(record.vietnamese),
    ].join("|");
    let error = "";
    if (header) error = "header";
    else if (!record.english || !record.vietnamese) error = "Thiếu tiếng Anh hoặc nghĩa tiếng Việt";
    else if (seen.has(key)) error = "Trùng trong danh sách";
    else seen.add(key);
    return { row: index + 1, ...record, valid: !error, error };
  }).filter((row) => row.error !== "header");
  renderBulkPreview();
}

function bulkItemListHtml(items) {
  if (!items?.length) return "—";
  return `<ul class="bulk-item-list">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderBulkPreview() {
  const body = el("bulkPreviewBody");
  const validRows = state.bulkRows.filter((row) => row.valid);
  body.innerHTML = state.bulkRows
    .slice(0, 200)
    .map(
      (row) => `<tr class="${row.valid ? "" : "invalid"}" title="${escapeHtml(row.error)}">
        <td>${row.row}</td><td>${escapeHtml(row.english || "—")}</td><td>${escapeHtml(row.phonetic || "—")}</td><td>${escapeHtml(row.vietnamese || "—")}</td>
        <td>${escapeHtml(row.part_of_speech || "—")}</td>
        <td>${row.examples.length
          ? `<ol class="bulk-example-list">${row.examples.map((example) => `<li>${escapeHtml(example)}</li>`).join("")}</ol>`
          : "—"}</td>
        <td>${bulkItemListHtml(row.collocations)}</td>
        <td>${bulkItemListHtml(row.word_patterns)}</td>
      </tr>`,
    )
    .join("");
  el("bulkPreviewEmpty").classList.toggle("hidden", state.bulkRows.length > 0);
  el("bulkPreviewCount").textContent = `${state.bulkRows.length} dòng`;
  el("importBulkButton").disabled = validRows.length === 0;
  const invalidCount = state.bulkRows.length - validRows.length;
  el("bulkImportNote").textContent = validRows.length
    ? `${validRows.length} dòng hợp lệ${invalidCount ? ` · ${invalidCount} dòng sẽ bỏ qua` : ""}.`
    : "Chưa có dòng nào sẵn sàng.";
}

async function importBulkWords() {
  const items = state.bulkRows.filter((row) => row.valid).map(({ english, phonetic, vietnamese, part_of_speech, examples, collocations, word_patterns }) => ({
    english,
    phonetic,
    vietnamese,
    part_of_speech,
    examples,
    collocations,
    word_patterns,
    collocation: collocations.join("\n"),
    word_pattern: word_patterns.join("\n"),
  }));
  if (!items.length) return;
  el("importBulkButton").disabled = true;
  try {
    const result = await api("/api/words/bulk", { method: "POST", body: JSON.stringify({ items }) });
    const skipped = result.skipped?.length || 0;
    toast("Đã nhập danh sách", `${result.added} từ được thêm${skipped ? `, ${skipped} dòng trùng được bỏ qua` : ""}.`);
    el("bulkInput").value = "";
    state.bulkRows = [];
    renderBulkPreview();
    await loadStats();
    setRoute("library");
  } catch (error) {
    toast("Không thể nhập danh sách", error.message, "error");
  } finally {
    el("importBulkButton").disabled = state.bulkRows.filter((row) => row.valid).length === 0;
  }
}

function openWordDialog(word) {
  state.selectedWord = word;
  const form = el("editWordForm");
  form.elements.id.value = word.id;
  form.elements.english.value = word.english;
  form.elements.phonetic.value = word.phonetic;
  form.elements.vietnamese.value = word.vietnamese;
  form.elements.part_of_speech.value = normalizePartOfSpeech(word.part_of_speech);
  const collocationsField = form.elements.collocations || form.elements.collocation;
  const wordPatternsField = form.elements.word_patterns || form.elements.word_pattern;
  if (collocationsField) {
    collocationsField.value = wordUsageItems(word, "collocations", "collocation").join("\n");
  }
  if (wordPatternsField) {
    wordPatternsField.value = wordUsageItems(word, "word_patterns", "word_pattern").join("\n");
  }
  form.elements.examples.value = wordExamples(word).join("\n");
  const [label] = statusMeta(word);
  el("dialogProgress").innerHTML = `
    <strong>${escapeHtml(label)}</strong> · Độ chính xác ${word.progress.accuracy === null ? "chưa có" : `${word.progress.accuracy}%`}
    ${word.progress.next_review_at ? `<br>Ôn tiếp: ${escapeHtml(fullDateTime(word.progress.next_review_at))} (${escapeHtml(relativeTime(word.progress.next_review_at))})` : ""}`;
  el("wordDialog").showModal();
  window.setTimeout(() => form.elements.english.focus(), 60);
}

function askConfirm({ title, message, confirmText = "Xác nhận", danger = true }) {
  const dialog = el("confirmDialog");
  el("confirmTitle").textContent = title;
  el("confirmMessage").textContent = message;
  const action = el("confirmActionButton");
  action.textContent = confirmText;
  action.className = danger ? "danger-button" : "primary-button compact";
  dialog.showModal();
  return new Promise((resolve) => {
    const onClose = () => {
      dialog.removeEventListener("close", onClose);
      resolve(dialog.returnValue === "confirm");
    };
    dialog.addEventListener("close", onClose);
  });
}

async function saveEditedWord(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const id = Number(form.elements.id.value);
  const payload = wordFormPayload(form);
  delete payload.id;
  const meaningChanged = state.selectedWord
    && (normalizeAnswer(state.selectedWord.english) !== normalizeAnswer(payload.english)
      || normalizeAnswer(state.selectedWord.vietnamese) !== normalizeAnswer(payload.vietnamese)
      || normalizeAnswer(normalizePartOfSpeech(state.selectedWord.part_of_speech))
        !== normalizeAnswer(normalizePartOfSpeech(payload.part_of_speech)));
  try {
    const result = await api(`/api/words/${id}`, { method: "PUT", body: JSON.stringify(payload) });
    state.selectedWord = result.word;
    toast("Đã lưu thay đổi", payload.english);
    el("wordDialog").close();
    if (meaningChanged && result.word.progress.state !== "new") {
      const reset = await askConfirm({
        title: "Đặt lại tiến độ của từ này?",
        message: "Bạn vừa đổi từ, nghĩa hoặc loại từ. Có thể giữ lịch cũ, hoặc học lại từ đầu để đảm bảo trí nhớ chính xác.",
        confirmText: "Học lại từ đầu",
        danger: false,
      });
      if (reset) await api(`/api/words/${id}/reset`, { method: "POST", body: "{}" });
    }
    await Promise.all([loadLibrary(), loadStats()]);
  } catch (error) {
    toast("Chưa thể lưu thay đổi", error.message, "error");
  }
}

async function deleteSelectedWord() {
  if (!state.selectedWord) return;
  const approved = await askConfirm({
    title: `Xoá “${state.selectedWord.english}”?`,
    message: "Từ, tiến độ và toàn bộ lịch sử ôn của từ này sẽ bị xoá khỏi cơ sở dữ liệu.",
    confirmText: "Xoá từ",
  });
  if (!approved) return;
  try {
    await api(`/api/words/${state.selectedWord.id}`, { method: "DELETE" });
    el("wordDialog").close();
    toast("Đã xoá từ", state.selectedWord.english);
    state.selectedWord = null;
    await Promise.all([loadLibrary(), loadStats()]);
  } catch (error) {
    toast("Không thể xoá từ", error.message, "error");
  }
}

async function resetSelectedWord() {
  if (!state.selectedWord) return;
  const approved = await askConfirm({
    title: `Học lại “${state.selectedWord.english}” từ đầu?`,
    message: "Tiến độ SRS và lịch sử trả lời của riêng từ này sẽ được đặt lại.",
    confirmText: "Đặt lại tiến độ",
  });
  if (!approved) return;
  try {
    await api(`/api/words/${state.selectedWord.id}/reset`, { method: "POST", body: "{}" });
    el("wordDialog").close();
    toast("Đã đặt lại tiến độ", state.selectedWord.english);
    state.selectedWord = null;
    await Promise.all([loadLibrary(), loadStats()]);
  } catch (error) {
    toast("Không thể đặt lại", error.message, "error");
  }
}

/* Speech synthesis */
function refreshVoiceAvailability() {
  if (!("speechSynthesis" in window)) {
    el("voiceLoadState").textContent = "Trình duyệt không hỗ trợ";
    el("voiceFallbackNote").textContent = "Trình duyệt này không cung cấp Web Speech API.";
    el("voiceFallbackNote").classList.add("visible");
    return;
  }
  state.browserVoices = window.speechSynthesis.getVoices();
  const loaded = state.browserVoices.length > 0;
  el("voiceLoadState").textContent = loaded ? `${state.browserVoices.length} giọng đã tải` : "Đang tải giọng…";
  document.querySelectorAll(".voice-card").forEach((card) => {
    const available = state.browserVoices.some((voice) => voice.name === card.dataset.voice);
    const badge = card.querySelector(".availability");
    badge.textContent = loaded ? (available ? "Có sẵn" : "Không tìm thấy") : "Đang kiểm tra";
    badge.className = `availability${loaded ? (available ? " available" : " unavailable") : ""}`;
  });
  const chosenAvailable = state.browserVoices.some((voice) => voice.name === state.voiceName);
  const fallback = state.browserVoices.find((voice) => /^en-US$/i.test(voice.lang))
    || state.browserVoices.find((voice) => voice.lang?.toLowerCase().startsWith("en"));
  const note = el("voiceFallbackNote");
  if (loaded && !chosenAvailable) {
    note.textContent = fallback
      ? `Không tìm thấy đúng giọng đã chọn trên máy. Khi phát âm, trình duyệt sẽ tạm dùng “${fallback.name}”.`
      : "Không tìm thấy giọng tiếng Anh phù hợp trên máy này.";
    note.classList.add("visible");
  } else {
    note.classList.remove("visible");
  }
}

function findVoice(name = state.voiceName) {
  return state.browserVoices.find((voice) => voice.name === name)
    || state.browserVoices.find((voice) => /^en-US$/i.test(voice.lang))
    || state.browserVoices.find((voice) => voice.lang?.toLowerCase().startsWith("en"))
    || null;
}

function speak(text, voiceName = state.voiceName) {
  if (!text || !("speechSynthesis" in window)) {
    toast("Không thể phát âm", "Trình duyệt hiện tại không hỗ trợ giọng đọc.", "error");
    return Promise.resolve(false);
  }
  refreshVoiceAvailability();
  const utterance = new SpeechSynthesisUtterance(text);
  const voice = findVoice(voiceName);
  if (voice) utterance.voice = voice;
  utterance.lang = "en-US";
  utterance.rate = 0.86;
  utterance.pitch = 1;
  return new Promise((resolve) => {
    let settled = false;
    const finish = (spoken) => {
      if (settled) return;
      settled = true;
      resolve(spoken);
    };
    utterance.addEventListener("end", () => finish(true), { once: true });
    utterance.addEventListener("error", () => finish(false), { once: true });
    window.setTimeout(
      () => finish(true),
      Math.min(6000, Math.max(1400, String(text).length * 110)),
    );
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  });
}

async function selectVoice(voiceName) {
  if (!VOICES.some((voice) => voice.name === voiceName)) return;
  state.voiceName = voiceName;
  el("voiceSelectTop").value = voiceName;
  document.querySelectorAll('input[name="voice"]').forEach((radio) => {
    radio.checked = radio.value === voiceName;
  });
  refreshVoiceAvailability();
  try {
    await api("/api/settings", { method: "PUT", body: JSON.stringify({ voice_name: voiceName }) });
  } catch (error) {
    toast("Chưa lưu được giọng đọc", error.message, "error");
  }
}

async function loadSettings() {
  try {
    const settings = await api("/api/settings");
    state.voiceName = settings.voice_name;
    el("voiceSelectTop").value = state.voiceName;
    document.querySelectorAll('input[name="voice"]').forEach((radio) => {
      radio.checked = radio.value === state.voiceName;
    });
  } catch (error) {
    toast("Không tải được cài đặt", error.message, "error");
  }
  refreshVoiceAvailability();
}

/* Study engine */
function studyWordById(id) {
  return state.study?.items.find((word) => word.id === id);
}

function learningDots(step) {
  return `<div class="learning-dots" aria-label="Đã hoàn thành ${step} trên 6 lượt">${Array.from({ length: 6 }, (_, index) => `<span class="learning-dot${index < step ? " filled" : ""}"></span>`).join("")}</div>`;
}

async function startStudy(mode) {
  try {
    let result;
    if (mode === "learn") {
      result = await api("/api/study/new?limit=5");
    } else if (mode === "review") {
      result = await api("/api/study/review?limit=20");
    } else {
      result = await api("/api/study/speed/start", { method: "POST", body: "{}" });
    }
    if (!result.items.length) {
      toast(
        mode === "learn" ? "Không còn từ mới" : "Chưa có từ đến hạn",
        mode === "learn" ? "Hãy thêm từ vào thư viện." : "Bạn đã hoàn thành lịch ôn hiện tại.",
        "error",
      );
      await loadStats();
      return;
    }
    const items = mode === "speed" ? shuffle(result.items) : result.items;
    const remainingGoal = mode === "learn"
      ? items.reduce((sum, word) => sum + (6 - word.progress.learning_step), 0)
      : items.length;
    const speedRules = result.rules || {
      starting_hearts: 3,
      extra_heart_streak: 15,
      question_seconds: 8,
      minimum_score: 100,
      maximum_score: 1000,
    };
    state.study = {
      mode,
      items,
      pool: result.pool,
      queue: items.map((word) => word.id),
      introduced: new Set(items.filter((word) => word.progress.learning_step > 0).map((word) => word.id)),
      current: null,
      answering: false,
      showingFeedback: false,
      successful: 0,
      processed: 0,
      correct: 0,
      wrong: 0,
      learnedCompleted: 0,
      remainingGoal,
      originalTotal: items.length,
      sessionId: result.session_id || null,
      hearts: speedRules.starting_hearts,
      streak: 0,
      bestStreak: 0,
      score: 0,
      skipped: 0,
      speedRules,
      timerFrame: null,
      timerTimeout: null,
      deadline: 0,
      questionToken: 0,
      gameOver: false,
    };
    document.body.style.overflow = "hidden";
    el("appShell").classList.add("hidden");
    el("studyView").classList.remove("hidden");
    el("studyView").classList.toggle("speed-mode", mode === "speed");
    el("speedHud").classList.toggle("hidden", mode !== "speed");
    el("studyVoiceButton").classList.toggle("hidden", mode === "speed");
    el("studyModeLabel").textContent = mode === "learn"
      ? "Học từ mới · 6 lượt đúng mỗi từ"
      : mode === "speed"
        ? "Ôn siêu tốc · chỉ từ đang đến hạn"
        : "Ôn theo lịch SRS";
    updateSpeedHud();
    nextStudyCard();
  } catch (error) {
    toast(mode === "speed" ? "Không thể bắt đầu Ôn siêu tốc" : "Không thể bắt đầu phiên học", error.message, "error");
    await loadStats();
  }
}

function updateStudyHeader() {
  const study = state.study;
  if (!study) return;
  let numerator;
  let denominator;
  if (study.mode === "learn") {
    numerator = study.successful;
    denominator = study.remainingGoal;
  } else {
    numerator = study.processed;
    denominator = study.originalTotal;
  }
  const percent = denominator ? Math.min(100, Math.round((numerator / denominator) * 100)) : 100;
  el("studyCounter").textContent = `${numerator} / ${denominator}`;
  el("studyProgressBar").style.width = `${percent}%`;
}

function nextStudyCard() {
  const study = state.study;
  if (!study) return;
  stopSpeedTimer();
  study.showingFeedback = false;
  study.answering = false;
  el("feedbackZone").className = "feedback-zone hidden";
  updateStudyHeader();

  if (study.mode === "speed" && study.hearts <= 0) {
    study.gameOver = true;
    finishStudyScreen();
    return;
  }

  if (!study.queue.length) {
    finishStudyScreen();
    return;
  }

  const wordId = study.queue.shift();
  const word = studyWordById(wordId);
  if (!word || (study.mode === "learn" && word.progress.state === "learned")) {
    nextStudyCard();
    return;
  }

  if (study.mode === "learn" && !study.introduced.has(wordId)) {
    study.current = {
      word,
      type: "introduction",
      selectedExample: randomItem(wordExamples(word)),
    };
    renderIntroduction(word);
    return;
  }

  let type = study.mode === "learn"
    ? learningQuestionType(word)
    : study.mode === "speed"
      ? speedQuestionType(word, study.processed)
      : reviewQuestionType(word, study.processed);
  if (study.mode === "speed" && !type) {
    study.current = { word, type: "speed-skip", attemptId: makeAttemptId() };
    skipUnanswerableSpeedWord(study, word);
    return;
  }
  const current = { word, type };
  if (type === "cloze") {
    current.selectedExample = randomItem(clozeExamples(word));
    current.clozeText = buildCloze(word, current.selectedExample);
    if (!current.clozeText) type = current.type = "typing";
  }
  study.current = current;
  renderQuestion(word, type);
}

function introductionUsageHtml(word) {
  const notes = [
    ["Collocation", wordUsageItems(word, "collocations", "collocation")],
    ["Word pattern", wordUsageItems(word, "word_patterns", "word_pattern")],
  ].filter(([, items]) => items.length);
  if (!notes.length) return "";
  return `<dl class="intro-language-notes">
    ${notes.map(([label, items]) => `<div><dt>${escapeHtml(label)}</dt><dd><ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></dd></div>`).join("")}
  </dl>`;
}

function renderIntroduction(word) {
  const example = state.study?.current?.selectedExample;
  el("questionArea").innerHTML = `
    <p class="question-kicker">Làm quen với từ</p>
    <h2 class="intro-word">${escapeHtml(word.english)}</h2>
    ${word.phonetic ? `<p class="intro-phonetic">${escapeHtml(word.phonetic)}</p>` : ""}
    ${word.part_of_speech ? `<span class="pos-chip intro-pos">${escapeHtml(normalizePartOfSpeech(word.part_of_speech))}</span>` : ""}
    <p class="intro-meaning">${escapeHtml(word.vietnamese)}</p>
    ${introductionUsageHtml(word)}
    ${example ? `<p class="intro-example">“${escapeHtml(example)}”</p>` : ""}
    ${learningDots(word.progress.learning_step)}
    <div class="intro-actions">
      <button class="secondary-button" id="introListen" type="button">▶ Nghe từ</button>
      <button class="primary-button compact" id="introContinue" type="button">Bắt đầu ghi nhớ</button>
    </div>`;
  el("introListen").addEventListener("click", () => speak(word.english));
  el("introContinue").addEventListener("click", () => {
    state.study.introduced.add(word.id);
    state.study.queue.unshift(word.id);
    nextStudyCard();
  });
  speak(word.english);
  el("introContinue").focus();
}

function renderReviewCorrection(word) {
  const study = state.study;
  // if (!study || study.mode !== "review" || !study.current) return;
  if (!study || !["review", "learn"].includes(study.mode) || !study.current) return;
  if (!Object.prototype.hasOwnProperty.call(study.current, "correctionExample")) {
    study.current.correctionExample = randomItem(wordExamples(word));
  }
  const example = study.current.correctionExample;
  el("questionArea").innerHTML = `
    <p class="question-kicker">Xem lại đáp án</p>
    <h2 class="intro-word">${escapeHtml(word.english)}</h2>
    ${word.phonetic ? `<p class="intro-phonetic">${escapeHtml(word.phonetic)}</p>` : ""}
    ${word.part_of_speech ? `<span class="pos-chip intro-pos">${escapeHtml(normalizePartOfSpeech(word.part_of_speech))}</span>` : ""}
    <p class="intro-meaning">${escapeHtml(word.vietnamese)}</p>
    ${introductionUsageHtml(word)}
    ${example ? `<p class="intro-example">“${escapeHtml(example)}”</p>` : ""}
    <div class="intro-actions review-correction-actions">
      <button class="secondary-button" id="reviewCorrectionListen" type="button">▶ Nghe lại</button>
    </div>`;
  el("reviewCorrectionListen").addEventListener("click", () => speak(word.english));
}

function learningQuestionType(word) {
  const types = ["meaning-choice", "word-choice", "typing", "listening-choice", "cloze", "listening-typing"];
  const type = types[Math.min(word.progress.learning_step, types.length - 1)];
  if (type === "cloze" && !clozeExamples(word).length) return "typing";
  if (type.endsWith("choice") && getOptions(word, type).length < 2) {
    return choiceFallbackType(type);
  }
  return type;
}

function reviewQuestionType(word, index) {
  const types = ["meaning-choice", "typing", "typing", "typing", "typing", "typing", "typing", "word-choice", "listening-typing"];
  let type = types[(word.id + index) % types.length];
  if (type.endsWith("choice") && getOptions(word, type).length < 2) type = choiceFallbackType(type);
  return type;
}

function speedQuestionType(word, index) {
  const preferred = (word.id + index) % 2 === 0 ? "meaning-choice" : "word-choice";
  if (getOptions(word, preferred).length >= 2) return preferred;
  const alternate = preferred === "meaning-choice" ? "word-choice" : "meaning-choice";
  return getOptions(word, alternate).length >= 2 ? alternate : null;
}

function updateSpeedHud() {
  const study = state.study;
  if (!study || study.mode !== "speed") return;
  const target = study.speedRules.extra_heart_streak;
  el("speedHearts").textContent = Array.from({ length: Math.max(0, study.hearts) }, () => "♥").join(" ") || "0";
  el("speedScore").textContent = formatNumber(study.score);
  el("speedStreak").textContent = `${study.streak} / ${target}`;
}

function stopSpeedTimer() {
  const study = state.study;
  if (!study) return;
  if (study.timerFrame !== null) {
    window.cancelAnimationFrame(study.timerFrame);
    study.timerFrame = null;
  }
  if (study.timerTimeout !== null) {
    window.clearTimeout(study.timerTimeout);
    study.timerTimeout = null;
  }
}

function updateSpeedTimerDisplay(remainingMs, durationMs) {
  const ratio = Math.max(0, Math.min(1, remainingMs / durationMs));
  const seconds = Math.max(0, remainingMs / 1000);
  el("speedTimerBar").style.transform = `scaleX(${ratio})`;
  el("speedTimerText").textContent = `${seconds.toFixed(1).replace(".", ",")} giây`;
  el("speedTimer").classList.toggle("urgent", ratio <= 0.25);
  el("speedTimer").setAttribute("aria-valuemax", String(durationMs / 1000));
  el("speedTimer").setAttribute("aria-valuenow", String(Math.ceil(seconds)));
}

function startSpeedTimer() {
  const study = state.study;
  if (!study || study.mode !== "speed") return;
  stopSpeedTimer();
  const durationMs = study.speedRules.question_seconds * 1000;
  const token = ++study.questionToken;
  study.deadline = performance.now() + durationMs;
  updateSpeedTimerDisplay(durationMs, durationMs);

  const paint = () => {
    if (state.study !== study || study.answering || token !== study.questionToken) return;
    const remaining = Math.max(0, study.deadline - performance.now());
    updateSpeedTimerDisplay(remaining, durationMs);
    if (remaining > 0) study.timerFrame = window.requestAnimationFrame(paint);
  };
  study.timerFrame = window.requestAnimationFrame(paint);
  study.timerTimeout = window.setTimeout(() => expireSpeedQuestion(token), durationMs);
}

function expireSpeedQuestion(token) {
  const study = state.study;
  if (
    !study
    || study.mode !== "speed"
    || study.answering
    || token !== study.questionToken
  ) return;
  updateSpeedTimerDisplay(0, study.speedRules.question_seconds * 1000);
  document.querySelectorAll(".answer-option").forEach((button) => {
    button.disabled = true;
    if (Number(button.dataset.optionIndex) === study.current.correctIndex) {
      button.classList.add("correct-answer");
    }
  });
  recordSpeedAnswer(false, true);
}

function makeAttemptId() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

async function skipUnanswerableSpeedWord(study, word) {
  if (state.study !== study || study.mode !== "speed" || study.answering) return;
  study.answering = true;
  study.showingFeedback = false;
  el("questionArea").innerHTML = `
    <p class="question-kicker">Đang chuẩn bị câu tiếp theo</p>
    <h2 class="question-title">Giữ nguyên lịch của “${escapeHtml(word.english)}”</h2>
    ${questionMetaHtml(word, "speed-skip")}
    <p class="question-subtitle">Chưa có đủ đáp án nhiễu rõ ràng nên từ này không bị chấm.</p>`;
  try {
    await api("/api/study/speed/skip", {
      method: "POST",
      body: JSON.stringify({
        session_id: study.sessionId,
        word_id: word.id,
        attempt_id: study.current.attemptId,
      }),
    });
    if (state.study !== study) return;
    study.skipped += 1;
    study.processed += 1;
    study.answering = false;
    study.current = null;
    updateStudyHeader();
    nextStudyCard();
  } catch (error) {
    if (state.study !== study) return;
    study.answering = false;
    el("questionArea").innerHTML = `
      <p class="question-kicker">Chưa lưu được trạng thái</p>
      <h2 class="question-title">Không thể bỏ qua an toàn</h2>
      <p class="question-subtitle">${escapeHtml(error.message)}</p>
      <button class="primary-button compact" id="retrySpeedSkipButton" type="button">Thử lại</button>`;
    el("retrySpeedSkipButton").addEventListener("click", () => skipUnanswerableSpeedWord(study, word));
    el("retrySpeedSkipButton").focus();
  }
}

function getOptions(word, type) {
  const field = type === "meaning-choice" ? "vietnamese" : "english";
  const correct = word[field];
  const distractors = [];
  const seen = new Set([normalizeAnswer(correct)]);
  const targetEnglish = normalizeAnswer(word.english);
  const targetVietnamese = normalizeAnswer(word.vietnamese);
  const pool = state.study?.pool || state.study?.items || [];
  for (const candidate of shuffle(pool)) {
    if (candidate.id === word.id) continue;
    if (type === "meaning-choice" && normalizeAnswer(candidate.english) === targetEnglish) continue;
    if (type === "word-choice" && normalizeAnswer(candidate.vietnamese) === targetVietnamese) continue;
    const value = candidate[field];
    const key = normalizeAnswer(value);
    if (!value || seen.has(key)) continue;
    seen.add(key);
    distractors.push(value);
    if (distractors.length === 3) break;
  }
  return shuffle([correct, ...distractors]);
}

function choiceFallbackType(type) {
  return type === "listening-choice" ? "listening-typing" : "typing";
}

function questionMetaHtml(word, type) {
  const partOfSpeech = normalizePartOfSpeech(word.part_of_speech);
  const phonetic = type === "meaning-choice" ? String(word.phonetic || "").trim() : "";
  return `<div class="question-meta">
    <span class="pos-chip question-pos${partOfSpeech ? "" : " unclassified"}">${escapeHtml(partOfSpeech || "chưa phân loại")}</span>
    ${phonetic ? `<span class="question-phonetic">${escapeHtml(phonetic)}</span>` : ""}
  </div>`;
}

function clozePattern(word, global = false) {
  const escaped = word.english.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(^|[^A-Za-z0-9_])(${escaped})(?=$|[^A-Za-z0-9_])`, global ? "gi" : "i");
}

function clozeExamples(word) {
  const pattern = clozePattern(word);
  return wordExamples(word).filter((example) => pattern.test(example));
}

function buildCloze(word, example) {
  if (!example) return null;
  const pattern = clozePattern(word, true);
  if (!pattern.test(example)) return null;
  pattern.lastIndex = 0;
  return example.replace(pattern, "$1________");
}

function renderQuestion(word, type) {
  if (type.endsWith("choice") && getOptions(word, type).length < 2) {
    const fallback = choiceFallbackType(type);
    state.study.current.type = fallback;
    renderQuestion(word, fallback);
    return;
  }
  const descriptions = {
    "meaning-choice": ["Chọn nghĩa đúng", word.english, "Từ này có nghĩa là gì?"],
    "word-choice": ["Chọn từ đúng", word.vietnamese, "Từ tiếng Anh phù hợp là gì?"],
    typing: ["Gõ từ tiếng Anh", word.vietnamese, "Nhập chính xác từ hoặc cụm từ."],
    "listening-choice": ["Nghe và chọn", "Bạn nghe thấy từ nào?", "Bấm nút loa để nghe lại."],
    cloze: ["Điền vào câu", state.study.current.clozeText, word.vietnamese],
    "listening-typing": ["Nghe và gõ", "Bạn nghe thấy gì?", "Nhập chính xác từ hoặc cụm từ."],
  };
  const [kicker, title, subtitle] = descriptions[type];
  let interaction = "";

  if (type === "meaning-choice" || type === "word-choice" || type === "listening-choice") {
    const options = getOptions(word, type);
    state.study.current.options = options;
    const correctValue = type === "meaning-choice" ? word.vietnamese : word.english;
    state.study.current.correctIndex = options.findIndex((option) => normalizeAnswer(option) === normalizeAnswer(correctValue));
    interaction = `<div class="answer-options">${options.map((option, index) => `
      <button class="answer-option" type="button" data-option-index="${index}">
        ${escapeHtml(option)}<span class="key-hint">${index + 1}</span>
      </button>`).join("")}</div>`;
  } else {
    interaction = `<form class="typing-form" id="typingAnswerForm">
      <label class="sr-only" for="typingAnswerInput">Nhập câu trả lời</label>
      <input class="typing-input" id="typingAnswerInput" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Nhập câu trả lời…">
      <button class="primary-button" type="submit">Kiểm tra</button>
      <p class="question-help">Không phân biệt chữ hoa/thường · Nhấn Enter để kiểm tra</p>
    </form>`;
  }

  const listen = type.startsWith("listening")
    ? `<button class="listen-orb" id="questionListenButton" type="button" aria-label="Nghe từ tiếng Anh">◖))</button>`
    : "";
  el("questionArea").innerHTML = `
    <p class="question-kicker">${escapeHtml(kicker)}</p>
    ${listen}
    <h2 class="question-title">${escapeHtml(title)}</h2>
    ${questionMetaHtml(word, type)}
    <p class="question-subtitle">${escapeHtml(subtitle)}</p>
    ${interaction}
    ${state.study.mode === "learn" ? learningDots(word.progress.learning_step) : ""}`;

  if (listen) {
    el("questionListenButton").addEventListener("click", () => speak(word.english));
    window.setTimeout(() => speak(word.english), 100);
  }
  document.querySelectorAll(".answer-option").forEach((button) => {
    button.addEventListener("click", () => answerChoice(Number(button.dataset.optionIndex)));
  });
  const typingForm = el("typingAnswerForm");
  if (typingForm) {
    typingForm.addEventListener("submit", (event) => {
      event.preventDefault();
      answerTyping(el("typingAnswerInput").value);
    });
    el("typingAnswerInput").focus();
  } else {
    document.querySelector(".answer-option")?.focus();
  }
  if (state.study?.mode === "speed") startSpeedTimer();
}

function answerChoice(index) {
  const study = state.study;
  if (!study || study.answering || study.showingFeedback) return;
  const correct = index === study.current.correctIndex;
  document.querySelectorAll(".answer-option").forEach((button) => {
    const buttonIndex = Number(button.dataset.optionIndex);
    button.disabled = true;
    if (buttonIndex === study.current.correctIndex) button.classList.add("correct-answer");
    if (buttonIndex === index && !correct) button.classList.add("wrong-answer");
  });
  recordAnswer(correct);
}

function answerTyping(answer) {
  const study = state.study;
  if (!study || study.answering || study.showingFeedback) return;
  const correct = normalizeAnswer(answer) === normalizeAnswer(study.current.word.english);
  const input = el("typingAnswerInput");
  if (input) {
    input.disabled = true;
    input.style.borderColor = correct ? "var(--success)" : "var(--danger)";
  }
  recordAnswer(correct);
}

async function recordAnswer(correct) {
  const study = state.study;
  if (!study || study.answering) return;
  if (study.mode === "speed") {
    await recordSpeedAnswer(correct, false);
    return;
  }
  study.answering = true;
  const word = study.current.word;
  const questionType = study.current.type;
  try {
    const result = await api("/api/study/result", {
      method: "POST",
      body: JSON.stringify({
        word_id: word.id,
        mode: study.mode,
        correct,
        question_type: study.current.type,
      }),
    });
    const updatedIndex = study.items.findIndex((item) => item.id === word.id);
    if (updatedIndex >= 0) study.items[updatedIndex] = result.word;
    study.current.word = result.word;
    study.processed += study.mode === "review" ? 1 : 0;
    if (correct) {
      study.correct += 1;
      if (study.mode === "learn") study.successful += 1;
    } else {
      study.wrong += 1;
    }

    if (study.mode === "learn") {
      if (result.word.progress.state === "learned") {
        study.learnedCompleted += 1;
      } else {
        const insertAfter = correct ? study.queue.length : Math.min(2, study.queue.length);
        study.queue.splice(insertAfter, 0, word.id);
      }
    }
    updateStudyHeader();
    // const showingReviewCorrection = study.mode === "review" && !correct;
    // if (showingReviewCorrection) renderReviewCorrection(result.word);
    // showFeedback(correct, result.word, result.schedule_reset);
    // if (showingReviewCorrection || !questionType.startsWith("listening")) {
    const showingCorrection = !correct && ["review", "learn"].includes(study.mode);
    if (showingCorrection) renderReviewCorrection(result.word);
    showFeedback(correct, result.word, result.schedule_reset);
    if (showingCorrection || !questionType.startsWith("listening")) {
      window.setTimeout(() => {
        if (
          state.study === study
          && study.showingFeedback
          && study.current?.word.id === word.id
        ) speak(result.word.english);
      }, 80);
    }
  } catch (error) {
    study.answering = false;
    toast("Không ghi được kết quả", error.message, "error");
  }
}

async function recordSpeedAnswer(correct, timedOut = false) {
  const study = state.study;
  if (!study || study.mode !== "speed" || study.answering) return;
  const word = study.current.word;
  const pending = study.current.pendingSpeedResult || (() => {
    const durationMs = study.speedRules.question_seconds * 1000;
    const remainingMs = timedOut ? 0 : Math.max(0, study.deadline - performance.now());
    return {
      attemptId: makeAttemptId(),
      correct,
      timedOut,
      questionType: study.current.type,
      remainingRatio: Math.max(0, Math.min(1, remainingMs / durationMs)),
    };
  })();
  study.current.pendingSpeedResult = pending;
  study.answering = true;
  stopSpeedTimer();

  try {
    const result = await api("/api/study/speed/result", {
      method: "POST",
      body: JSON.stringify({
        session_id: study.sessionId,
        word_id: word.id,
        attempt_id: pending.attemptId,
        correct: pending.correct,
        timed_out: pending.timedOut,
        question_type: `speed-${pending.questionType}`,
      }),
    });
    const updatedIndex = study.items.findIndex((item) => item.id === word.id);
    if (updatedIndex >= 0) study.items[updatedIndex] = result.word;
    study.current.word = result.word;
    study.processed += 1;

    let points = 0;
    let bonusHeart = false;
    if (pending.correct && !pending.timedOut) {
      const minimum = study.speedRules.minimum_score;
      const maximum = study.speedRules.maximum_score;
      points = minimum + Math.floor((maximum - minimum) * pending.remainingRatio);
      study.score += points;
      study.correct += 1;
      study.streak += 1;
      study.bestStreak = Math.max(study.bestStreak, study.streak);
      if (study.streak >= study.speedRules.extra_heart_streak) {
        study.hearts += 1;
        study.streak = 0;
        bonusHeart = true;
      }
    } else {
      study.wrong += 1;
      study.hearts = Math.max(0, study.hearts - 1);
      study.streak = 0;
    }

    updateStudyHeader();
    updateSpeedHud();
    showSpeedFeedback({
      correct: pending.correct && !pending.timedOut,
      timedOut: pending.timedOut,
      word: result.word,
      points,
      bonusHeart,
    });
    study.current.pendingSpeedResult = null;

    await Promise.all([
      sleep(pending.correct && !pending.timedOut ? 550 : 950),
      speak(result.word.english),
    ]);
    if (state.study === study) nextStudyCard();
  } catch (error) {
    study.answering = false;
    toast("Không ghi được kết quả Ôn siêu tốc", error.message, "error");
    showSpeedSaveError(error.message);
  }
}

function showSpeedSaveError(message) {
  const study = state.study;
  if (!study || study.mode !== "speed") return;
  study.showingFeedback = true;
  const zone = el("feedbackZone");
  zone.className = "feedback-zone incorrect";
  zone.innerHTML = `
    <div class="feedback-content">
      <span class="feedback-mark">!</span>
      <div class="feedback-copy"><strong>Chưa lưu được kết quả</strong><span>${escapeHtml(message)} Đồng hồ đã dừng; bấm thử lại để không bị chấm hai lần.</span></div>
      <button class="primary-button compact" id="retrySpeedResultButton" type="button">Thử lưu lại</button>
    </div>`;
  el("retrySpeedResultButton").addEventListener("click", () => {
    study.showingFeedback = false;
    recordSpeedAnswer(false, false);
  });
  el("retrySpeedResultButton").focus();
}

function showSpeedFeedback({ correct, timedOut, word, points, bonusHeart }) {
  const study = state.study;
  if (!study) return;
  study.showingFeedback = true;
  const zone = el("feedbackZone");
  zone.className = `feedback-zone ${correct ? "correct" : "incorrect"}`;
  const headline = timedOut ? "Hết giờ · mất 1 tim" : correct ? `Chính xác · +${formatNumber(points)} điểm` : "Chưa đúng · mất 1 tim";
  let detail;
  if (correct) {
    detail = bonusHeart
      ? `Đủ ${study.speedRules.extra_heart_streak} câu đúng liên tiếp: nhận thêm 1 tim.`
      : `Lần ôn tiếp theo sau ${word.progress.srs_label}.`;
  } else {
    detail = `Đáp án là “${word.english}”${word.phonetic ? ` ${word.phonetic}` : ""}. Lịch được đặt lại; ôn tiếp sau 4 giờ.`;
  }
  zone.innerHTML = `
    <div class="feedback-content">
      <span class="feedback-mark">${correct ? "✓" : "×"}</span>
      <div class="feedback-copy"><strong>${escapeHtml(headline)}</strong><span>${escapeHtml(detail)}</span></div>
    </div>`;
}

function showFeedback(correct, word, scheduleReset) {
  const study = state.study;
  study.showingFeedback = true;
  const zone = el("feedbackZone");
  zone.className = `feedback-zone ${correct ? "correct" : "incorrect"}`;
  let headline;
  let detail;
  if (study.mode === "review") {
    headline = correct ? "Chính xác" : "Chưa đúng";
    detail = correct
      ? `Lần ôn tiếp theo sau ${word.progress.srs_label}.`
      : "Hãy xem lại đáp án ở trên. Lịch ghi nhớ đã được đặt lại; ôn tiếp sau 4 giờ.";
  } else if (word.progress.state === "learned") {
    headline = "Từ đã được gieo vào trí nhớ";
    detail = "Lần ôn SRS đầu tiên sẽ đến sau 4 giờ.";
  } else {
    headline = correct ? "Chính xác" : "Chưa đúng";
    detail = correct
      ? `Bạn đã hoàn thành ${word.progress.learning_step}/6 lượt đúng.`
      : `Đáp án là “${word.english}”${word.phonetic ? ` ${word.phonetic}` : ""}. Từ này sẽ quay lại sau vài câu khác.`;
  }
  if (scheduleReset) {
    detail = study.mode === "review" && !correct
      ? "Hãy xem lại đáp án ở trên. Lịch ghi nhớ đã được đặt lại; ôn tiếp sau 4 giờ."
      : "Lịch ghi nhớ đã được đặt lại; ôn tiếp sau 4 giờ.";
  }
  zone.innerHTML = `
    <div class="feedback-content">
      <span class="feedback-mark">${correct ? "✓" : "×"}</span>
      <div class="feedback-copy"><strong>${escapeHtml(headline)}</strong><span>${escapeHtml(detail)}</span></div>
      <button class="primary-button compact" id="nextQuestionButton" type="button">Tiếp tục ↵</button>
    </div>`;
  el("nextQuestionButton").addEventListener("click", nextStudyCard);
  el("nextQuestionButton").focus();
}

function finishStudyScreen() {
  const study = state.study;
  stopSpeedTimer();
  updateStudyHeader();
  el("studyProgressBar").style.width = "100%";
  if (study.mode === "speed") {
    updateSpeedTimerDisplay(0, study.speedRules.question_seconds * 1000);
    const title = study.gameOver ? "Hết tim · kết thúc Ôn siêu tốc" : "Đã hoàn tất Ôn siêu tốc";
    const answered = study.correct + study.wrong;
    let description = study.gameOver
      ? `Bạn đã trả lời ${answered}/${study.originalTotal} từ đến hạn. Những từ chưa gặp vẫn giữ nguyên lịch cũ.`
      : `Bạn đã trả lời ${answered} từ đến hạn trong phiên này.`;
    if (study.skipped) {
      description += ` ${study.skipped} từ được giữ nguyên lịch vì thư viện chưa có đủ đáp án nhiễu rõ ràng.`;
    }
    el("questionArea").innerHTML = `
      <div class="completion-content">
        <span class="completion-mark">⚡</span>
        <h2>${escapeHtml(title)}</h2>
        <p>${escapeHtml(description)}</p>
        <div class="completion-stats">
          <div><strong>${formatNumber(study.score)}</strong><span>Tổng điểm</span></div>
          <div><strong>${study.correct}</strong><span>Trả lời đúng</span></div>
          <div><strong>${study.wrong}</strong><span>Sai / hết giờ</span></div>
        </div>
        <button class="primary-button" id="finishStudyButton" type="button">Về trang hôm nay</button>
      </div>`;
    el("feedbackZone").className = "feedback-zone hidden";
    el("finishStudyButton").addEventListener("click", () => closeStudy(false));
    el("finishStudyButton").focus();
    return;
  }
  const title = study.mode === "learn" ? "Đã hoàn tất lượt học mới" : "Lịch ôn đã hoàn thành";
  const description = study.mode === "learn"
    ? `${study.learnedCompleted} từ đã bước vào chu kỳ SRS, với lần ôn đầu tiên sau 4 giờ.`
    : "Mỗi từ đã được đặt lịch theo kết quả vừa trả lời.";
  el("questionArea").innerHTML = `
    <div class="completion-content">
      <span class="completion-mark">✓</span>
      <h2>${escapeHtml(title)}</h2>
      <p>${escapeHtml(description)}</p>
      <div class="completion-stats">
        <div><strong>${study.correct}</strong><span>Trả lời đúng</span></div>
        <div><strong>${study.wrong}</strong><span>Cần củng cố</span></div>
        <div><strong>${study.mode === "learn" ? study.learnedCompleted : study.originalTotal}</strong><span>${study.mode === "learn" ? "Từ đã học" : "Từ đã ôn"}</span></div>
      </div>
      <button class="primary-button" id="finishStudyButton" type="button">Về trang hôm nay</button>
    </div>`;
  el("feedbackZone").className = "feedback-zone hidden";
  el("finishStudyButton").addEventListener("click", () => closeStudy(false));
  el("finishStudyButton").focus();
}

async function closeStudy(ask = true) {
  const study = state.study;
  if (ask && study?.queue.length) {
    const approved = await askConfirm({
      title: "Kết thúc phiên học?",
      message: "Mọi kết quả đã trả lời đều được lưu. Bạn có thể tiếp tục phần còn lại vào lần sau.",
      confirmText: "Kết thúc phiên",
    });
    if (!approved) return;
  }
  stopSpeedTimer();
  window.speechSynthesis?.cancel();
  state.study = null;
  document.body.style.overflow = "";
  el("studyView").classList.add("hidden");
  el("studyView").classList.remove("speed-mode");
  el("speedHud").classList.add("hidden");
  el("studyVoiceButton").classList.remove("hidden");
  el("appShell").classList.remove("hidden");
  setRoute("dashboard");
}

function handleStudyKeyboard(event) {
  if (!state.study || el("studyView").classList.contains("hidden")) return;
  if (event.key.toLowerCase() === "r" && state.study.mode !== "speed" && document.activeElement?.tagName !== "INPUT") {
    event.preventDefault();
    const word = state.study.current?.word;
    if (word) speak(word.english);
    return;
  }
  if (state.study.showingFeedback && state.study.mode !== "speed" && event.key === "Enter") {
    event.preventDefault();
    nextStudyCard();
    return;
  }
  if (/^[1-4]$/.test(event.key) && !state.study.showingFeedback) {
    const button = document.querySelector(`.answer-option[data-option-index="${Number(event.key) - 1}"]`);
    if (button && !button.disabled) {
      event.preventDefault();
      button.click();
    }
  }
}

function bindEvents() {
  document.querySelectorAll("[data-route]").forEach((button) => {
    button.addEventListener("click", () => setRoute(button.dataset.route));
  });

  el("startReviewButton").addEventListener("click", () => startStudy("review"));
  el("startSpeedReviewButton").addEventListener("click", () => startStudy("speed"));
  el("startLearnButton").addEventListener("click", () => startStudy("learn"));
  el("exitStudyButton").addEventListener("click", () => closeStudy(true));
  el("studyVoiceButton").addEventListener("click", () => {
    const word = state.study?.current?.word;
    if (word) speak(word.english);
  });

  const searchLibrary = debounce(() => {
    state.library.q = el("librarySearch").value.trim();
    state.library.page = 1;
    loadLibrary(1);
  });
  el("librarySearch").addEventListener("input", searchLibrary);
  el("statusFilter").addEventListener("change", () => {
    state.library.status = el("statusFilter").value;
    state.library.page = 1;
    loadLibrary(1);
  });
  el("posFilter").addEventListener("change", () => {
    state.library.partOfSpeech = el("posFilter").value;
    state.library.page = 1;
    loadLibrary(1);
  });

  el("formulaForm")?.addEventListener("submit", saveFormula);
  el("formulaCancelEditButton")?.addEventListener("click", () => {
    setFormulaEditorMode();
    el("formulaContent").focus();
  });
  el("retryFormulasButton")?.addEventListener("click", loadFormulas);

  el("singleTab").addEventListener("click", () => switchAddTab("single"));
  el("bulkTab").addEventListener("click", () => switchAddTab("bulk"));
  el("singleWordForm").addEventListener("submit", submitSingleWord);
  el("singleWordForm").addEventListener("input", debounce(saveSingleDraft, 300));
  el("previewSingleVoice").addEventListener("click", () => speak(el("singleEnglish").value.trim()));

  el("bulkInput").addEventListener("keydown", insertTabIntoBulkInput);
  el("bulkInput").addEventListener("input", refreshBulkPosSuggestions);
  el("bulkInput").addEventListener("input", debounce(parseBulkInput, 160));
  el("bulkInput").addEventListener("click", refreshBulkPosSuggestions);
  el("bulkInput").addEventListener("focus", refreshBulkPosSuggestions);
  el("bulkInput").addEventListener("scroll", positionBulkPosSuggestions);
  el("bulkInput").addEventListener("blur", () => {
    window.setTimeout(closeBulkPosSuggestions, 80);
  });
  el("clearBulkButton").addEventListener("click", () => {
    closeBulkPosSuggestions();
    el("bulkInput").value = "";
    state.bulkRows = [];
    renderBulkPreview();
    el("bulkInput").focus();
  });
  el("importBulkButton").addEventListener("click", importBulkWords);

  el("editWordForm").addEventListener("submit", saveEditedWord);
  const wordDialog = el("wordDialog");
  el("closeWordDialogButton")?.addEventListener("click", () => wordDialog.close("cancel"));
  el("cancelEditButton")?.addEventListener("click", () => wordDialog.close("cancel"));
  wordDialog.addEventListener("click", (event) => {
    if (event.target !== wordDialog) return;
    const bounds = wordDialog.getBoundingClientRect();
    const clickedBackdrop = event.clientX < bounds.left
      || event.clientX > bounds.right
      || event.clientY < bounds.top
      || event.clientY > bounds.bottom;
    if (clickedBackdrop && wordDialog.open) wordDialog.close("cancel");
  });
  el("deleteWordButton").addEventListener("click", deleteSelectedWord);
  el("resetWordButton").addEventListener("click", resetSelectedWord);

  el("voiceSelectTop").addEventListener("change", (event) => selectVoice(event.target.value));
  el("testVoiceTop").addEventListener("click", () => speak("A little progress every day adds up to big results."));
  document.querySelectorAll('input[name="voice"]').forEach((radio) => {
    radio.addEventListener("change", () => selectVoice(radio.value));
  });
  document.querySelectorAll("[data-test-voice]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      speak("Consistency is the key to lasting progress.", button.dataset.testVoice);
    });
  });

  document.addEventListener("keydown", handleStudyKeyboard);
  window.addEventListener("beforeunload", () => window.speechSynthesis?.cancel());
}

async function init() {
  const today = new Intl.DateTimeFormat("vi-VN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date());
  el("todayLabel").textContent = today;
  bindEvents();
  restoreSingleDraft();
  renderBulkPreview();
  if ("speechSynthesis" in window) {
    window.speechSynthesis.addEventListener?.("voiceschanged", refreshVoiceAvailability);
    refreshVoiceAvailability();
  }
  await Promise.all([loadSettings(), loadStats()]);
}

document.addEventListener("DOMContentLoaded", init);
