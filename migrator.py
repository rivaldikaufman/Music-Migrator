#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from difflib import get_close_matches
import webbrowser
import time

# Script ini membaca daftar lagu dari Apple Music (playlist.txt)
# Mencari lagu di Spotify (termasuk fuzzy search)
# Membuat playlist baru dan menambahkan lagu-lagu yang ditemukan
# Lagu yang gagal dicatat di gagal.txt

# AUTHENTIKASI SPOTIFY
auth = SpotifyOAuth(
    client_id="your_client_id_here",
    client_secret="your_secret_here",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public user-library-read user-library-modify"
)
sp = spotipy.Spotify(auth_manager=auth, requests_timeout=15)

def fuzzy_search(track, max_attempts=3):
    # Pisahkan artis dan judul jika memungkinkan
    terms = track.split(" - ")
    if len(terms) != 2:
        return None
    artist, title = terms
    query = f"track:{title} artist:{artist}"
    result = sp.search(q=query, limit=max_attempts, type='track')
    items = result.get("tracks", {}).get("items", [])
    if items:
        return items[0]["uri"]
    return None

# BACA LAGU DARI playlist.txt
with open("playlist.txt", "r") as f:
    tracks = [line.strip() for line in f if line.strip()]

user_id = sp.current_user()["id"]

# Fungsi untuk mengecek apakah lagu sudah di-Liked
def is_track_liked(track_id):
    return sp.current_user_saved_tracks_contains([track_id])[0]

skipped = []
gagal = []
for idx, track in enumerate(tracks, start=1):
    for attempt in range(3):
        try:
            result = sp.search(q=track, limit=1, type='track')
            break
        except Exception as e:
            if attempt == 2:
                print(f"[{idx}/{len(tracks)}] ⚠️ Gagal karena timeout: {track}")
                gagal.append(track)
                result = None
            else:
                time.sleep(2)
                continue
    if result is None:
        continue
    items = result.get("tracks", {}).get("items", [])
    if items:
        uri = items[0]["uri"]
        track_id = items[0]["id"]
        if is_track_liked(track_id):
            print(f"[{idx}/{len(tracks)}] ⏩ Skip (sudah ada): {track}")
            skipped.append(track)
        else:
            sp.current_user_saved_tracks_add([track_id])
            print(f"[{idx}/{len(tracks)}] ✅ Ditambahkan: {track}")
    else:
        fuzzy_uri = fuzzy_search(track)
        if fuzzy_uri:
            fuzzy_id = fuzzy_uri.split(":")[-1]
            if is_track_liked(fuzzy_id):
                print(f"[{idx}/{len(tracks)}] ⏩ Skip (fuzzy & sudah ada): {track}")
                skipped.append(track)
            else:
                sp.current_user_saved_tracks_add([fuzzy_id])
                print(f"[{idx}/{len(tracks)}] 🔍✅ Fuzzy Ditambahkan: {track}")
        else:
            print(f"[{idx}/{len(tracks)}] ❌ Tidak ditemukan: {track}")
            gagal.append(track)
    time.sleep(0.5)

if gagal:
    with open("gagal.txt", "w") as f:
        for lagu in gagal:
            f.write(lagu + "\n")
    print(f"⚠️ {len(gagal)} lagu tidak ditemukan. Disimpan di gagal.txt")

if skipped:
    with open("skipped.txt", "w") as f:
        for lagu in skipped:
            f.write(lagu + "\n")
    print(f"ℹ️ {len(skipped)} lagu sudah ada di Liked Songs. Disimpan di skipped.txt")

print("🎉 Semua lagu berhasil diproses ke Lagu yang Disukai!")
webbrowser.open("https://open.spotify.com/collection/tracks")