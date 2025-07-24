#!/bin/bash

echo "🚀 Inisialisasi Python project..."

# Buat venv
python3 -m venv .venv
echo "✅ Virtual environment .venv dibuat."

# Aktifkan venv dan install requirements (kalau ada)
source .venv/bin/activate
if [ -f "requirements.txt" ]; then
    echo "📦 Install requirements..."
    pip install -r requirements.txt
fi

echo "🔥 Project siap digunakan!"