import xml.etree.ElementTree as ET

tree = ET.parse("Music.xml")
root = tree.getroot()

songs = []

# Cari node 'dict' yang punya 'Name' dan 'Artist'
for dict_tag in root.iter('dict'):
    keys = list(dict_tag)
    name = None
    artist = None
    for i in range(len(keys)):
        if keys[i].tag == 'key' and keys[i].text == 'Name':
            name = keys[i+1].text
        elif keys[i].tag == 'key' and keys[i].text == 'Artist':
            artist = keys[i+1].text
    if name and artist:
        songs.append(f"{artist} - {name}")

# Simpan ke txt atau langsung push ke Spotify seperti sebelumnya
with open("playlist.txt", "w") as f:
    for song in songs:
        f.write(song + "\n")

print("✅ XML berhasil diparse dan disimpan sebagai playlist.txt")