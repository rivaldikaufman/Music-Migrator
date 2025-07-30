# Migrating Apple Music Playlists to Spotify
Written by: **Rivaldi**
Last updated: 2025-07-24

---

## 🔥 Purpose

<p align="center">
  <img src="SCREENSHOTS/MIGRATOR.jpeg" alt="Migrator Preview" width="600"/>
</p>

Migrate all songs from Apple Music to Spotify *without third-party tools* like SongShift. Just Python and the Spotify API.

---

## 📦 Tools & Libraries

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Spotipy-Library-green?logo=spotify&logoColor=white" alt="Spotipy" />
  <img src="https://img.shields.io/badge/Apple%20Music-XML-red?logo=apple&logoColor=white" alt="Apple Music" />
  <img src="https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white" alt="Spotify API" />
  <img src="https://img.shields.io/badge/Bash-initpyenv.sh-black?logo=gnubash&logoColor=white" alt="Bash" />
</p>

* Python 3.13 (use virtual environment)
* [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API library)
* Apple Music (manually exported playlists)
* `playlisttotxt.py` to parse Apple Music XML
* `migrator.py` to transfer songs to Spotify

---

## 🧰 Initial Setup with `initpyenv.sh`

Run the following script to automatically set up the environment:

```bash
chmod +x initpyenv.sh
./initpyenv.sh
```

This script will:

* Create a virtual environment
* Install dependencies: `spotipy`, `requests`
* Automatically activate the environment

---

## 🧠 Migration Workflow

1. **Export Apple Music Playlist (Mac):**

   * Open `Music.app`
   * Click playlist → File > Library > Export Playlist → choose XML

2. **Run `playlisttotxt.py`:**

   ```bash
   python3 playlisttotxt.py path/to/exported_playlist.xml
   ```

   Output: `playlist.txt`

3. **Run `migrator.py` to transfer songs to Spotify**

   ```bash
   python3 migrator.py
   ```

   The script will:

   * Add songs to "Liked Songs"
   * Skip songs that are already added
   * Log failed songs in `gagal.txt`
   * Log existing songs in `skipped.txt`

---

## 🎫 About Spotify Client ID & Secret

To use this script, you **must have access to the Spotify Developer Console** to use their API.

Steps:

1. Visit: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **Create App** → enter name and description
4. Once created, you’ll get:

   * **Client ID**
   * **Client Secret**

⚠️ **Insert both values manually into `migrator.py`**:

```python
auth = SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public user-library-read user-library-modify"
)
```

Without this, the script won’t be able to access your Spotify account.

---

## 📂 File Structure

```
Music-Migrator/
├── initpyenv.sh
├── playlisttotxt.py        # parses XML to txt
├── migrator.py             # reads playlist.txt and transfers the songs to Spotify
├── playlist.txt            # output from playlisttotxt.py
├── gagal.txt               # songs that failed to transfer
└── skipped.txt             # songs already in your Spotify library
```

---

## 🛠️ Script Features

* Fuzzy search (matches based on similarity or typos)
* Auto-skip if song already exists
* Retry request on timeout
* Logging to txt files
* Auto-opens Spotify "Liked Songs" after migration

---

## 🪲 Bugs & Solutions

### 1. **403: Insufficient client scope**

**Issue:**

```
403 Client Error: Forbidden for url: https://api.spotify.com/v1/me/tracks/contains
```

**Solution:**
Ensure full scope is set:

```python
scope="playlist-modify-public user-library-read user-library-modify"
```

Then remove `.cache*` to re-login:

```bash
rm .cache*
```

---

### 2. **Request timeout (ReadTimeoutError)**

**Issue:**

```
Read timed out. (read timeout=5)
```

**Solution:**

* Set `requests_timeout=15`
* Add `time.sleep(0.5)` between requests
* Retry song search up to 3 times if failed

---

### 3. **Playlist appears empty on Spotify**

**Issue:** Playlist seems empty even though it was processed successfully  
**Solution:** Ensure `migrator.py` uses:

```python
sp.current_user_saved_tracks_add([track_id])
```

The script doesn't create a new playlist, it adds songs directly to "Liked Songs"

---

## ✅ Final Output

* Songs from Apple Music successfully added to "Liked Songs" in Spotify
* Failed songs → `gagal.txt`
* Skipped songs → `skipped.txt`
* Spotify "Liked Songs" opens automatically in browser

---

## ✨ Development Roadmap

* Auto-parse XML without manual export
* GUI with drag-and-drop playlist
* Export logs to CSV
* Preview/dry-run mode before transfer

---

## 🤝 Contribution

Since I'm the type of person who often switches between music streaming services and gets tired of transferring songs manually one by one, I finally created my own automation solution. The process is designed to be flexible and reusable anytime, with three main components:

* `initpyenv.sh`
* `playlisttotxt.py`
* `migrator.py`