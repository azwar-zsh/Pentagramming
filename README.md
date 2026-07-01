# Sistem Rekomendasi Film & Buku — Rule-Based Reasoning
Kelompok **Pentagramming (IK24ABC)** </br>
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
