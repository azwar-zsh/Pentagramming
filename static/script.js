// script.js
// Menghubungkan form Fact Base ke endpoint /api/recommend, lalu me-render
// Reasoning Trace (Conflict Set setelah Conflict Resolution) dan Output
// (rekomendasi + penjelasan) secara animasi bertahap.

const form = document.getElementById("fact-form");
const tipeToggle = document.getElementById("tipe_media_toggle");
const tipeInput = document.getElementById("tipe_media");
const durasiLabel = document.getElementById("durasi_label");
const traceList = document.getElementById("trace-list");
const outputList = document.getElementById("output-list");

// Toggle tipe media (film/buku) + ubah label durasi
tipeToggle.addEventListener("click", (e) => {
  const btn = e.target.closest(".seg-btn");
  if (!btn) return;
  [...tipeToggle.children].forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  tipeInput.value = btn.dataset.value;
  durasiLabel.textContent = btn.dataset.value === "film" ? "Durasi (menit)" : "Durasi (halaman)";
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    tipe_media: tipeInput.value,
    genre: document.getElementById("genre").value,
    mood: document.getElementById("mood").value,
    durasi: document.getElementById("durasi").value,
    rating_min: document.getElementById("rating_min").value,
    era: document.getElementById("era").value,
    bahasa: document.getElementById("bahasa").value,
  };

  traceList.innerHTML = `<p class="empty-state">Menjalankan forward chaining...</p>`;
  outputList.innerHTML = `<p class="empty-state">Menyusun rekomendasi...</p>`;

  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    renderTrace(data.conflict_set);
    renderOutput(data.rekomendasi);
  } catch (err) {
    traceList.innerHTML = `<p class="empty-state">Gagal menghubungi mesin inferensi: ${err}</p>`;
    outputList.innerHTML = "";
  }
});

function renderTrace(conflictSet) {
  if (!conflictSet || conflictSet.length === 0) {
    traceList.innerHTML = `<p class="empty-state">Tidak ada rule yang aktif (kurang dari 2 kondisi cocok). Coba lengkapi lebih banyak preferensi.</p>`;
    return;
  }

  traceList.innerHTML = "";
  conflictSet.forEach((rule, i) => {
    const div = document.createElement("div");
    div.className = "trace-item" + (i === 0 ? " top" : "");
    div.style.animationDelay = `${i * 70}ms`;

    const matchedChips = rule.matched_fields
      .map((f) => `<span class="chip matched">${f}</span>`)
      .join("");
    const unmatchedCount = rule.total_conditions - rule.matched_count;
    const extraChip = unmatchedCount > 0
      ? `<span class="chip">${unmatchedCount} kondisi lain tidak diperiksa</span>`
      : "";

    div.innerHTML = `
      <div class="trace-head">
        <span class="trace-id">${rule.id} ${i === 0 ? "&#9679; prioritas tertinggi" : ""}</span>
        <span class="trace-score">skor ${rule.skor.toFixed(2)} &middot; conf ${rule.confidence}</span>
      </div>
      <div class="trace-desc">${rule.keterangan}</div>
      <div class="trace-meta">${matchedChips}${extraChip}</div>
    `;
    traceList.appendChild(div);
  });
}

function renderOutput(recs) {
  if (!recs || recs.length === 0) {
    outputList.innerHTML = `<p class="empty-state">Tidak ada media yang memenuhi batasan (tipe media / bahasa / rating). Coba longgarkan preferensi.</p>`;
    return;
  }

  outputList.innerHTML = "";
  recs.forEach((rec, i) => {
    const card = document.createElement("div");
    card.className = "rec-card";
    card.style.animationDelay = `${i * 90}ms`;

    const tags = [...rec.genre, ...rec.mood]
      .map((t) => `<span class="chip">${t}</span>`)
      .join("");

    card.innerHTML = `
      <span class="rec-rank">${i + 1}</span>
      <p class="rec-title">${rec.judul}</p>
      <p class="rec-sub">${rec.tipe.toUpperCase()} &middot; ${rec.era} &middot; ${rec.bahasa} &middot; &#9733; ${rec.rating} &middot; ${rec.durasi} ${rec.tipe === "film" ? "menit" : "hal"}</p>
      <div class="rec-explain">${rec.penjelasan}</div>
      <div class="rec-tags">${tags}</div>
    `;
    outputList.appendChild(card);
  });
}
