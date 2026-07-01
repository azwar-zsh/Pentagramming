# -*- coding: utf-8 -*-
"""
rules.py
Rule Base: kumpulan aturan IF-THEN.

Struktur setiap rule:
    id          : identifier rule, mis. "R1"
    conditions  : dict {field: nilai_yang_diharapkan}
                  field yang didukung: mood, genre, era, bahasa, durasi_kategori
    conclusion  : dict {"genre": [...], "mood": [...]}  -> tag yang dipakai
                  untuk mencocokkan/menaikkan skor item media
    confidence  : bobot keyakinan rule (0.0 - 1.0)
    keterangan  : deskripsi singkat untuk explainability

Catatan soft-constraint: sebuah rule diaktifkan (masuk Conflict Set) jika
minimal 2 dari kondisinya (atau seluruhnya bila kondisi < 2) terpenuhi oleh
Fact Base pengguna. Lihat engine/inference.py fungsi `forward_chaining`.
"""

RULE_BASE = [
    {"id": "R1", "conditions": {"mood": "tegang", "genre": "sci-fi"},
     "conclusion": {"genre": ["sci-fi", "thriller"], "mood": ["tegang", "penasaran"]},
     "confidence": 0.92, "keterangan": "mood tegang + genre sci-fi terpenuhi"},

    {"id": "R2", "conditions": {"mood": "tegang", "genre": "thriller", "durasi_kategori": "sedang"},
     "conclusion": {"genre": ["thriller"], "mood": ["tegang"]},
     "confidence": 0.9, "keterangan": "mood tegang + genre thriller + durasi sedang"},

    {"id": "R3", "conditions": {"mood": "penasaran", "genre": "misteri"},
     "conclusion": {"genre": ["misteri", "thriller"], "mood": ["penasaran"]},
     "confidence": 0.88, "keterangan": "mood penasaran + genre misteri terpenuhi"},

    {"id": "R4", "conditions": {"mood": "stres", "genre": "komedi"},
     "conclusion": {"genre": ["komedi"], "mood": ["santai", "stres"]},
     "confidence": 0.9, "keterangan": "mood stres + genre komedi (pelepas penat)"},

    {"id": "R5", "conditions": {"mood": "stres", "durasi_kategori": "pendek", "genre": "komedi"},
     "conclusion": {"genre": ["komedi"], "mood": ["santai"]},
     "confidence": 0.85, "keterangan": "mood stres + durasi singkat cocok untuk hiburan ringan"},

    {"id": "R6", "conditions": {"mood": "sedih", "genre": "drama"},
     "conclusion": {"genre": ["drama"], "mood": ["sedih", "reflektif"]},
     "confidence": 0.87, "keterangan": "mood sedih + genre drama terpenuhi"},

    {"id": "R7", "conditions": {"mood": "reflektif", "genre": "drama", "era": "2010s"},
     "conclusion": {"genre": ["drama", "sejarah"], "mood": ["reflektif"]},
     "confidence": 0.8, "keterangan": "mood reflektif + genre drama + era 2010-an"},

    {"id": "R8", "conditions": {"mood": "hangat", "genre": "romantis"},
     "conclusion": {"genre": ["romantis"], "mood": ["hangat"]},
     "confidence": 0.88, "keterangan": "mood hangat + genre romantis terpenuhi"},

    {"id": "R9", "conditions": {"mood": "hangat", "genre": "keluarga"},
     "conclusion": {"genre": ["keluarga", "drama"], "mood": ["hangat", "santai"]},
     "confidence": 0.83, "keterangan": "mood hangat + genre keluarga terpenuhi"},

    {"id": "R10", "conditions": {"mood": "cemas", "genre": "horor"},
     "conclusion": {"genre": ["horor"], "mood": ["tegang", "cemas"]},
     "confidence": 0.9, "keterangan": "mood cemas + genre horor terpenuhi"},

    {"id": "R11", "conditions": {"mood": "cemas", "genre": "horor", "durasi_kategori": "pendek"},
     "conclusion": {"genre": ["horor", "thriller"], "mood": ["cemas"]},
     "confidence": 0.82, "keterangan": "mood cemas + horor + durasi singkat"},

    {"id": "R12", "conditions": {"mood": "semangat", "genre": "aksi"},
     "conclusion": {"genre": ["aksi", "sci-fi"], "mood": ["semangat"]},
     "confidence": 0.86, "keterangan": "mood semangat + genre aksi terpenuhi"},

    {"id": "R13", "conditions": {"mood": "bangga", "genre": "sejarah"},
     "conclusion": {"genre": ["sejarah", "drama"], "mood": ["bangga", "reflektif"]},
     "confidence": 0.84, "keterangan": "mood bangga + genre sejarah terpenuhi"},

    {"id": "R14", "conditions": {"mood": "santai", "genre": "keluarga", "durasi_kategori": "pendek"},
     "conclusion": {"genre": ["keluarga", "komedi"], "mood": ["santai"]},
     "confidence": 0.78, "keterangan": "mood santai + keluarga + durasi singkat"},

    {"id": "R15", "conditions": {"genre": "sci-fi", "era": "2020s"},
     "conclusion": {"genre": ["sci-fi"], "mood": ["penasaran", "semangat"]},
     "confidence": 0.75, "keterangan": "genre sci-fi + era 2020-an terpenuhi"},

    {"id": "R16", "conditions": {"genre": "thriller", "era": "2020s"},
     "conclusion": {"genre": ["thriller", "misteri"], "mood": ["tegang"]},
     "confidence": 0.76, "keterangan": "genre thriller + era 2020-an terpenuhi"},

    {"id": "R17", "conditions": {"bahasa": "indonesia", "genre": "drama"},
     "conclusion": {"genre": ["drama"], "mood": ["reflektif", "sedih"]},
     "confidence": 0.7, "keterangan": "bahasa Indonesia + genre drama terpenuhi"},

    {"id": "R18", "conditions": {"bahasa": "inggris", "genre": "sci-fi"},
     "conclusion": {"genre": ["sci-fi"], "mood": ["penasaran"]},
     "confidence": 0.7, "keterangan": "bahasa Inggris + genre sci-fi terpenuhi"},

    {"id": "R19", "conditions": {"mood": "penasaran", "genre": "thriller", "durasi_kategori": "sedang"},
     "conclusion": {"genre": ["thriller", "misteri"], "mood": ["penasaran", "tegang"]},
     "confidence": 0.89, "keterangan": "mood penasaran + thriller + durasi sedang"},

    {"id": "R20", "conditions": {"mood": "sedih", "genre": "sci-fi"},
     "conclusion": {"genre": ["sci-fi", "drama"], "mood": ["sedih", "reflektif"]},
     "confidence": 0.79, "keterangan": "mood sedih + genre sci-fi (kontemplatif)"},

    {"id": "R21", "conditions": {"mood": "santai", "genre": "romantis", "durasi_kategori": "sedang"},
     "conclusion": {"genre": ["romantis", "komedi"], "mood": ["hangat", "santai"]},
     "confidence": 0.81, "keterangan": "mood santai + romantis + durasi sedang"},

    {"id": "R22", "conditions": {"mood": "penasaran", "genre": "sci-fi", "durasi_kategori": "panjang"},
     "conclusion": {"genre": ["sci-fi"], "mood": ["penasaran", "semangat"]},
     "confidence": 0.83, "keterangan": "mood penasaran + sci-fi + durasi panjang (mendalam)"},

    {"id": "R23", "conditions": {"mood": "tegang", "genre": "misteri", "durasi_kategori": "panjang"},
     "conclusion": {"genre": ["misteri", "thriller"], "mood": ["tegang", "penasaran"]},
     "confidence": 0.85, "keterangan": "mood tegang + misteri + durasi panjang"},

    {"id": "R24", "conditions": {"mood": "hangat", "genre": "komedi", "era": "2020s"},
     "conclusion": {"genre": ["komedi", "romantis"], "mood": ["hangat", "santai"]},
     "confidence": 0.77, "keterangan": "mood hangat + komedi + era 2020-an"},
]
