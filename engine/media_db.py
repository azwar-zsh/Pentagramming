"""
media_db.py
Basis pengetahuan (Knowledge Base) berupa daftar media film & buku.
Diperbarui dengan data valid dari dunia nyata (IMDb & Goodreads).

Field:
    id       : identifier unik
    judul    : judul media
    tipe     : "film" atau "buku"
    genre    : list genre (huruf kecil)
    mood     : list mood/vibe yang cocok (huruf kecil)
    durasi   : durasi dalam menit (film) ATAU jumlah halaman (buku)
    era      : dekade rilis, misal "2010s" atau "2020s"
    bahasa   : "indonesia" atau "inggris"
    rating   : rating 0-10 (berdasarkan IMDb/Goodreads)
"""

MEDIA_DB = [
    # ---------------- FILM ----------------
    {"id": "F01", "judul": "Ex Machina", "tipe": "film",
     "genre": ["sci-fi", "thriller"], "mood": ["tegang", "penasaran"],
     "durasi": 108, "era": "2010s", "bahasa": "inggris", "rating": 7.7},
    {"id": "F02", "judul": "Habibie & Ainun", "tipe": "film",
     "genre": ["drama", "romantis"], "mood": ["sedih", "reflektif"],
     "durasi": 118, "era": "2010s", "bahasa": "indonesia", "rating": 7.6},
    {"id": "F03", "judul": "Game Night", "tipe": "film",
     "genre": ["komedi"], "mood": ["stres", "santai"],
     "durasi": 100, "era": "2010s", "bahasa": "inggris", "rating": 6.9},
    {"id": "F04", "judul": "Pengabdi Setan 2: Communion", "tipe": "film",
     "genre": ["horor", "misteri"], "mood": ["tegang", "cemas"],
     "durasi": 119, "era": "2020s", "bahasa": "indonesia", "rating": 6.8},
    {"id": "F05", "judul": "Bumi Manusia", "tipe": "film",
     "genre": ["sejarah", "drama"], "mood": ["reflektif", "bangga"],
     "durasi": 181, "era": "2010s", "bahasa": "indonesia", "rating": 6.9},
    {"id": "F06", "judul": "Dune", "tipe": "film",
     "genre": ["sci-fi", "aksi"], "mood": ["semangat", "penasaran"],
     "durasi": 155, "era": "2020s", "bahasa": "inggris", "rating": 8.0},
    {"id": "F07", "judul": "Keluarga Cemara", "tipe": "film",
     "genre": ["drama", "keluarga"], "mood": ["hangat", "santai"],
     "durasi": 110, "era": "2010s", "bahasa": "indonesia", "rating": 7.8},
    {"id": "F08", "judul": "Glass Onion: A Knives Out Mystery", "tipe": "film",
     "genre": ["thriller", "misteri"], "mood": ["tegang", "penasaran"],
     "durasi": 139, "era": "2020s", "bahasa": "inggris", "rating": 7.1},
    {"id": "F09", "judul": "Ngeri-Ngeri Sedap", "tipe": "film",
     "genre": ["drama", "komedi"], "mood": ["hangat", "santai"],
     "durasi": 114, "era": "2020s", "bahasa": "indonesia", "rating": 8.1},
    {"id": "F10", "judul": "Interstellar", "tipe": "film",
     "genre": ["sci-fi", "drama"], "mood": ["reflektif", "sedih"],
     "durasi": 169, "era": "2010s", "bahasa": "inggris", "rating": 8.7},
    {"id": "F11", "judul": "Pengabdi Setan", "tipe": "film",
     "genre": ["horor", "thriller"], "mood": ["tegang", "cemas"],
     "durasi": 107, "era": "2010s", "bahasa": "indonesia", "rating": 7.6},
    {"id": "F12", "judul": "Anyone But You", "tipe": "film",
     "genre": ["romantis", "komedi"], "mood": ["hangat", "santai"],
     "durasi": 103, "era": "2020s", "bahasa": "inggris", "rating": 6.2},

    # ---------------- BUKU ----------------
    {"id": "B01", "judul": "Dilan: Dia adalah Dilanku Tahun 1990", "tipe": "buku",
     "genre": ["romantis", "drama"], "mood": ["hangat", "reflektif"],
     "durasi": 332, "era": "2010s", "bahasa": "indonesia", "rating": 8.0},
    {"id": "B02", "judul": "Gone Girl", "tipe": "buku",
     "genre": ["thriller", "misteri"], "mood": ["tegang", "penasaran"],
     "durasi": 415, "era": "2010s", "bahasa": "inggris", "rating": 8.1},
    {"id": "B03", "judul": "Laut Bercerita", "tipe": "buku",
     "genre": ["drama", "sejarah"], "mood": ["sedih", "reflektif"],
     "durasi": 379, "era": "2010s", "bahasa": "indonesia", "rating": 8.8},
    {"id": "B04", "judul": "Project Hail Mary", "tipe": "buku",
     "genre": ["sci-fi", "thriller"], "mood": ["penasaran", "semangat"],
     "durasi": 476, "era": "2020s", "bahasa": "inggris", "rating": 8.9},
    {"id": "B05", "judul": "Marmut Merah Jambu", "tipe": "buku",
     "genre": ["komedi", "keluarga"], "mood": ["stres", "santai"],
     "durasi": 222, "era": "2010s", "bahasa": "indonesia", "rating": 7.5},
    {"id": "B06", "judul": "Sewu Dino", "tipe": "buku",
     "genre": ["horor", "misteri"], "mood": ["tegang", "cemas"],
     "durasi": 250, "era": "2010s", "bahasa": "indonesia", "rating": 7.5},
    {"id": "B07", "judul": "All the Light We Cannot See", "tipe": "buku",
     "genre": ["sejarah", "drama"], "mood": ["reflektif", "bangga"],
     "durasi": 531, "era": "2010s", "bahasa": "inggris", "rating": 8.6},
    {"id": "B08", "judul": "Bumi (Serial Dunia Paralel)", "tipe": "buku",
     "genre": ["sci-fi", "aksi"], "mood": ["tegang", "penasaran"],
     "durasi": 440, "era": "2010s", "bahasa": "indonesia", "rating": 7.8},
    {"id": "B09", "judul": "Wonder", "tipe": "buku",
     "genre": ["drama", "keluarga"], "mood": ["hangat", "santai"],
     "durasi": 315, "era": "2010s", "bahasa": "inggris", "rating": 8.8},
    {"id": "B10", "judul": "Orang-Orang Biasa", "tipe": "buku",
     "genre": ["misteri", "drama"], "mood": ["penasaran", "sedih"],
     "durasi": 300, "era": "2010s", "bahasa": "indonesia", "rating": 7.5},
    {"id": "B11", "judul": "Lessons in Chemistry", "tipe": "buku",
     "genre": ["komedi", "drama"], "mood": ["stres", "santai"],
     "durasi": 400, "era": "2020s", "bahasa": "inggris", "rating": 8.7},
    {"id": "B12", "judul": "Selena", "tipe": "buku",
     "genre": ["romantis", "sci-fi"], "mood": ["hangat", "reflektif"],
     "durasi": 368, "era": "2020s", "bahasa": "indonesia", "rating": 8.0},
]