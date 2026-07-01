# -*- coding: utf-8 -*-
"""
facts.py
Fact Extraction: memvalidasi input pengguna dan mengonversinya menjadi
Fact Base (dictionary) yang siap diproses mesin inferensi.
"""

# Batas kategori durasi. Film dihitung dalam menit, buku dalam halaman.
DURASI_KATEGORI_FILM = {"pendek": (0, 95), "sedang": (96, 120), "panjang": (121, 10_000)}
DURASI_KATEGORI_BUKU = {"pendek": (0, 250), "sedang": (251, 380), "panjang": (381, 100_000)}


def _kategori_durasi(tipe_media: str, durasi):
    if durasi is None:
        return None
    table = DURASI_KATEGORI_FILM if tipe_media == "film" else DURASI_KATEGORI_BUKU
    for kategori, (lo, hi) in table.items():
        if lo <= durasi <= hi:
            return kategori
    return None


def build_fact_base(user_input: dict) -> dict:
    """
    Mengubah input mentah pengguna menjadi Fact Base yang ternormalisasi
    (lowercase, tervalidasi). Field yang tidak diisi akan bernilai None
    dan tidak akan dicocokkan oleh rule manapun (rule butuh nilai eksplisit).
    """
    tipe_media = (user_input.get("tipe_media") or "film").strip().lower()
    genre = (user_input.get("genre") or "").strip().lower() or None
    mood = (user_input.get("mood") or "").strip().lower() or None
    era = (user_input.get("era") or "").strip().lower() or None
    bahasa = (user_input.get("bahasa") or "").strip().lower() or None

    durasi_raw = user_input.get("durasi")
    try:
        durasi = int(durasi_raw) if durasi_raw not in (None, "",) else None
    except (ValueError, TypeError):
        durasi = None

    rating_min_raw = user_input.get("rating_min")
    try:
        rating_min = float(rating_min_raw) if rating_min_raw not in (None, "",) else None
    except (ValueError, TypeError):
        rating_min = None

    fact_base = {
        "tipe_media": tipe_media if tipe_media in ("film", "buku") else "film",
        "genre": genre,
        "mood": mood,
        "era": era,
        "bahasa": bahasa,
        "durasi": durasi,
        "durasi_kategori": _kategori_durasi(tipe_media, durasi),
        "rating_min": rating_min,
    }
    return fact_base
