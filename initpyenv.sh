#!/bin/bash

echo "🚀 Inisialisasi Python project..."

# Buat venv jika belum ada
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment .venv dibuat."
else
    echo "ℹ️ Virtual environment .venv sudah ada."
fi

# Aktifkan venv dan install requirements (kalau ada)
source .venv/bin/activate
if [ -f "requirements.txt" ]; then
    echo "📦 Install requirements..."
    pip install -r requirements.txt
fi

echo "🔥 Project siap digunakan! Environment sudah aktif di $(which python)"
exec $SHELL