# -*- coding: utf-8 -*-
"""
inference.py
Mesin Inferensi: Forward Chaining + Conflict Resolution + Output Generation.

Alur (sesuai Bagian 6 proposal):
    1. Rule Matching   -> cocokkan Fact Base dengan tiap rule di Rule Base.
    2. Forward Chaining-> rule yang syaratnya terpenuhi (soft constraint:
                          minimal 2 kondisi terpenuhi) masuk ke Conflict Set.
    3. Conflict Resolution -> urutkan Conflict Set berdasarkan kombinasi
                          confidence tertinggi & specificity (jumlah kondisi
                          yang cocok).
    4. Output Generation-> gunakan rule terpilih untuk menyaring & mem-ranking
                          item di Media Base (dengan Hard Constraint tipe
                          media & bahasa), lalu susun penjelasan logis.
"""

from .rules import RULE_BASE
from .media_db import MEDIA_DB

MIN_CONDITIONS_TO_FIRE = 2


def _match_condition(fact_value, expected_value) -> bool:
    if fact_value is None:
        return False
    return str(fact_value).strip().lower() == str(expected_value).strip().lower()


def forward_chaining(fact_base: dict, rule_base=RULE_BASE):
    """
    Mencocokkan Fact Base terhadap seluruh Rule Base.
    Mengembalikan Conflict Set: list of dict berisi rule + jumlah kondisi
    yang cocok (specificity) + daftar kondisi yang cocok (untuk explainability).
    """
    conflict_set = []
    for rule in rule_base:
        conditions = rule["conditions"]
        matched_fields = []
        for field, expected in conditions.items():
            if _match_condition(fact_base.get(field), expected):
                matched_fields.append(field)

        total_conditions = len(conditions)
        threshold = min(MIN_CONDITIONS_TO_FIRE, total_conditions)
        matched_count = len(matched_fields)

        if matched_count >= threshold and matched_count > 0:
            conflict_set.append({
                "rule": rule,
                "matched_fields": matched_fields,
                "matched_count": matched_count,
                "total_conditions": total_conditions,
            })
    return conflict_set


def conflict_resolution(conflict_set: list):
    """
    Mengurutkan Conflict Set berdasarkan skor gabungan:
        skor = confidence * matched_count
    Rule dengan confidence tinggi DAN kondisi yang lebih spesifik (banyak
    kondisi cocok) diprioritaskan lebih dulu.
    """
    for item in conflict_set:
        item["skor"] = round(item["rule"]["confidence"] * item["matched_count"], 4)
    return sorted(conflict_set, key=lambda x: x["skor"], reverse=True)


def _apply_hard_constraints(fact_base: dict, media_db=MEDIA_DB):
    """Hard Constraint: tipe media wajib sama; bahasa wajib sama jika diisi;
    rating_min wajib terpenuhi jika diisi."""
    candidates = []
    for item in media_db:
        if item["tipe"] != fact_base["tipe_media"]:
            continue
        if fact_base["bahasa"] and item["bahasa"] != fact_base["bahasa"]:
            continue
        if fact_base["rating_min"] is not None and item["rating"] < fact_base["rating_min"]:
            continue
        candidates.append(item)
    return candidates


def generate_output(fact_base: dict, ranked_conflict_set: list, media_db=MEDIA_DB):
    """
    Output Generation: skor tiap kandidat media berdasarkan rule yang
    aktif (semakin banyak tag genre/mood yang cocok dengan conclusion rule
    berbobot tinggi, semakin tinggi skornya), lalu tampilkan semua
    rekomendasi teratas beserta penjelasan (rule mana yang berkontribusi).
    """
    candidates = _apply_hard_constraints(fact_base, media_db)
    
    print(f"[DEBUG] Candidates after hard constraints: {len(candidates)}")
    print(f"[DEBUG] Active rules: {len(ranked_conflict_set)}")
    
    if not candidates:
        print("[DEBUG] No candidates found - hard constraints too strict!")
        return []
    if not ranked_conflict_set:
        fallback = sorted(candidates, key=lambda m: m["rating"], reverse=True)
        return [{
            "media": m,
            "skor": 0.0,
            "rule_kontribusi": [],
            "penjelasan": ("Tidak ada rule spesifik yang aktif untuk preferensi ini; "
                           "item dipilih berdasarkan rating tertinggi yang memenuhi "
                           "batasan tipe media dan bahasa.")
        } for m in fallback]

    scored = []
    for media in candidates:
        total_score = 0.0
        contributing_rules = []
        for entry in ranked_conflict_set:
            rule = entry["rule"]
            genre_hit = bool(set(media["genre"]) & set(rule["conclusion"].get("genre", [])))
            mood_hit = bool(set(media["mood"]) & set(rule["conclusion"].get("mood", [])))
            if genre_hit or mood_hit:
                total_score += entry["skor"]
                contributing_rules.append(entry)

        if fact_base.get("era") and media["era"] == fact_base["era"]:
            total_score += 0.1

        scored.append((total_score, media, contributing_rules))

    scored.sort(key=lambda x: (x[0], x[1]["rating"]), reverse=True)

    results = []
    for total_score, media, contributing_rules in scored:
        rule_ids = [entry["rule"]["id"] for entry in contributing_rules]
        keterangan_list = [entry["rule"]["keterangan"] for entry in contributing_rules]
        if rule_ids:
            penjelasan = (f"Direkomendasikan karena memenuhi {' & '.join(rule_ids)}: "
                           f"{'; '.join(keterangan_list)}.")
        else:
            penjelasan = ("Direkomendasikan berdasarkan rating tinggi dan memenuhi batasan "
                         "tipe media serta bahasa yang Anda pilih.")
        results.append({
            "media": media,
            "skor": round(total_score, 3),
            "rule_kontribusi": rule_ids,
            "penjelasan": penjelasan,
        })
    
    print(f"[DEBUG] Total recommendations generated: {len(results)}")
    return results


def run_pipeline(fact_base: dict):
    """Menjalankan seluruh pipeline: forward chaining -> conflict resolution
    -> output generation. Mengembalikan dict lengkap untuk ditampilkan/di-API-kan."""
    conflict_set = forward_chaining(fact_base)
    ranked = conflict_resolution(conflict_set)
    recommendations = generate_output(fact_base, ranked)

    return {
        "fact_base": fact_base,
        "conflict_set": [
            {
                "id": e["rule"]["id"],
                "keterangan": e["rule"]["keterangan"],
                "confidence": e["rule"]["confidence"],
                "matched_fields": e["matched_fields"],
                "matched_count": e["matched_count"],
                "total_conditions": e["total_conditions"],
                "skor": e["skor"],
            } for e in ranked
        ],
        "rekomendasi": [
            {
                "id": r["media"]["id"],
                "judul": r["media"]["judul"],
                "tipe": r["media"]["tipe"],
                "genre": r["media"]["genre"],
                "mood": r["media"]["mood"],
                "era": r["media"]["era"],
                "bahasa": r["media"]["bahasa"],
                "rating": r["media"]["rating"],
                "durasi": r["media"]["durasi"],
                "skor_rekomendasi": r["skor"],
                "rule_kontribusi": r["rule_kontribusi"],
                "penjelasan": r["penjelasan"],
            } for r in recommendations
        ],
    }
