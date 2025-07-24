# Migrasi Playlist Apple Music ke Spotify: Panduan Lengkap + Solusi Bug

Ditulis oleh: **Rivaldi**
Terakhir diperbarui: 2025-07-24

---

## 🔥 Tujuan

Migrasi semua lagu dari Apple Music ke Spotify *tanpa third-party tool* seperti SongShift. Cukup dengan Python dan API Spotify.

---

## 📦 Tools & Library

* Python 3.13 (pakai virtual environment disarankan)
* [Spotipy](https://spotipy.readthedocs.io/) (Python library untuk Spotify Web API)
* Apple Music (playlist diekspor manual)
* File `playlist.txt` hasil parsing dari Apple Music XML

---

## 🧠 Alur Migrasi

1. Ekspor playlist dari Apple Music → jadi file teks
2. Buka file itu dan baca semua baris lagu (format: `Artist - Title`)
3. Gunakan Spotify API:

   * Cek apakah lagu sudah ada di "Liked Songs"
   * Jika belum, tambahkan
   * Jika gagal cari, coba fuzzy search
   * Jika tetap gagal, log ke `gagal.txt`
   * Jika sudah ada, log ke `skipped.txt`
4. Setelah selesai, buka otomatis halaman Liked Songs di browser

---

## 📂 Struktur File

```
project-folder/
├── migrator.py
├── playlist.txt         # daftar lagu dari Apple Music
├── gagal.txt            # lagu yang tidak ditemukan di Spotify
└── skipped.txt          # lagu yang sudah ada di Liked Songs
```

---

## 🛠️ Script Python (Fitur Lengkap)

* Fuzzy search
* Auto skip jika lagu sudah ada
* Retry jika timeout
* Buka Spotify "Liked Songs" otomatis
* Logging ke file `gagal.txt` & `skipped.txt`

---

## 🪲 Bug & Solusi

### 1. **403: Insufficient client scope**

**Masalah:**

```
403 Client Error: Forbidden for url: https://api.spotify.com/v1/me/tracks/contains
```

**Penyebab:** Scope `user-library-read` dan `user-library-modify` tidak diset.

**Solusi:**

```python
scope="playlist-modify-public user-library-read user-library-modify"
```

Hapus `.cache` file agar login ulang dengan scope baru:

```bash
rm .cache*
```

---

### 2. **Request timeout (ReadTimeoutError)**

**Masalah:**

```
HTTPSConnectionPool(host='api.spotify.com', port=443): Read timed out. (read timeout=5)
```

**Solusi:**
Tambahkan timeout lebih besar di Spotipy:

```python
spotipy.Spotify(auth_manager=auth, requests_timeout=15)
```

Tambahkan `time.sleep(0.5)` antar request + retry 3x:

```python
for attempt in range(3):
    try:
        result = sp.search(...)
        break
    except:
        time.sleep(2)
```

---

### 3. **Playlist kosong di Spotify**

**Masalah:** Playlist berhasil dibuat tapi lagu tidak muncul.
**Penyebab:** Script default menambahkan lagu ke playlist, bukan ke "Liked Songs".

**Solusi:** Ubah script agar langsung tambahkan ke `Liked Songs`:

```python
sp.current_user_saved_tracks_add([track_id])
```

---

## ✅ Output Akhir

* Lagu dari `playlist.txt` ditransfer ke "Liked Songs"
* Lagu yang gagal → `gagal.txt`
* Lagu yang sudah ada → `skipped.txt`
* Browser otomatis buka Spotify "Liked Songs"

---

## ✨ Improvement ke Depan

* Auto parse langsung dari XML Apple Music
* GUI drag-n-drop
* Export hasil ke CSV/Excel
* Mode dry-run

---

## 🤝 Kontribusi

Script & proses ini dikembangkan dari pengalaman langsung oleh Rivaldi selama migrasi 700+ lagu dari Apple Music ke Spotify secara manual.

Kalau kamu ingin script-nya, tinggal DM atau comment di blog ini ya!
