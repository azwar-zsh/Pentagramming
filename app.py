# -*- coding: utf-8 -*-
"""
app.py
Backend Flask untuk Sistem Rekomendasi Film & Buku berbasis Rule-Based
Reasoning (Symbolic AI - Forward Chaining + Conflict Resolution).

Jalankan:
    pip install flask
    python app.py
lalu buka http://127.0.0.1:5000 di browser.
"""

from flask import Flask, request, jsonify, render_template
from engine.facts import build_fact_base
from engine.inference import run_pipeline
from engine.media_db import MEDIA_DB

app = Flask(__name__)

GENRE_OPTIONS = sorted({g for m in MEDIA_DB for g in m["genre"]})
MOOD_OPTIONS = sorted({mo for m in MEDIA_DB for mo in m["mood"]})
ERA_OPTIONS = sorted({m["era"] for m in MEDIA_DB})


@app.route("/")
def index():
    return render_template(
        "index.html",
        genres=GENRE_OPTIONS,
        moods=MOOD_OPTIONS,
        eras=ERA_OPTIONS,
    )


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """
    Endpoint utama sistem pakar.
    Menerima input preferensi pengguna (JSON), menjalankan pipeline
    Fact Extraction -> Forward Chaining -> Conflict Resolution ->
    Output Generation, lalu mengembalikan rekomendasi + explainability.
    """
    user_input = request.get_json(force=True) or {}

    fact_base = build_fact_base(user_input)
    print("\n" + "="*60)
    print("FACT BASE:", fact_base)
    
    hasil = run_pipeline(fact_base)
    
    print(f"Conflict Set: {len(hasil['conflict_set'])} rules")
    print(f"Rekomendasi: {len(hasil['rekomendasi'])} items")
    print("="*60 + "\n")

    return jsonify(hasil)


if __name__ == "__main__":
    app.run(debug=True)
