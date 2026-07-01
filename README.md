# Sistem Rekomendasi Film & Buku — Rule-Based Reasoning
Kelompok **Pentagramming (IK24ABC)**
241011053 - Muh. Azwar. R – (IK24B) </br>
241011015 - Gad – (IK24C) </br>
241011078 - Elisa Steven Tandilo – (IK24B) </br>
241011096 - Jeremia Anderson Sipayung – (IK24A) </br>
241011098 - Yosia Mahendra S – (IK24B)

## Struktur Proyek
```
pentagramming/
├── app.py                 # Backend Flask (routing + API)
├── engine/
│   ├── facts.py            # Fact Extraction: input pengguna -> Fact Base
│   ├── rules.py             # Rule Base: 24 aturan IF-THEN (confidence + kondisi)
│   ├── media_db.py           # Knowledge Base: 24 film & buku
│   └── inference.py          # Mesin Inferensi: Forward Chaining, Conflict
│                              # Resolution, Output Generation
├── templates/index.html      # UI form input preferensi
├── static/style.css          # Styling ("reasoning trace" theme)
└── static/script.js          # Fetch API + render trace & rekomendasi
```

## Cara Menjalankan
```bash
pip install flask
python app.py
```
Lalu buka **http://127.0.0.1:5000** di browser.

## Alur Sistem (sesuai Bagian 6 Proposal)
1. **Input** — pengguna mengisi tipe media, genre, mood, durasi/halaman,
   rating minimum, era, dan bahasa lewat form web.
2. **Fact Extraction** (`engine/facts.py`) — input divalidasi & dinormalisasi
   menjadi Fact Base, termasuk kategori durasi otomatis (pendek/sedang/panjang).
3. **Rule Matching + Forward Chaining** (`engine/inference.py`) — setiap rule
   di Rule Base dicek terhadap Fact Base. Rule **aktif** (masuk Conflict Set)
   bila minimal 2 kondisinya cocok (soft constraint).
4. **Conflict Resolution** — Conflict Set diurutkan berdasarkan
   `skor = confidence × jumlah kondisi yang cocok`.
5. **Output Generation** — kandidat media disaring dengan **hard constraint**
   (tipe media & bahasa wajib cocok, rating minimum bila diisi), lalu diberi
   skor berdasarkan rule-rule yang aktif dan diambil maksimal 3 teratas,
   masing-masing dengan penjelasan logis seperti:
   > "Direkomendasikan karena memenuhi R2 & R19: mood tegang + genre thriller
   > + durasi sedang; mood penasaran + thriller + durasi sedang."
