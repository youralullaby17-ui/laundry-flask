import os

# Buat folder templates
os.makedirs("templates", exist_ok=True)

# HTML sederhana
index_html = "<html><body><h2>Form Laundry</h2><form action='/simpan' method='post'>Nama: <input name='nama'><br><button type='submit'>Simpan</button></form><a href='/transaksi'>Lihat Transaksi</a></body></html>"
transaksi_html = "<html><body><h2>Transaksi</h2>{% for t in belum %}<p>{{ t.nama }} - Rp {{ t.total }}</p>{% endfor %}<a href='/'>Kembali</a></body></html>"
update_html = "<html><body><h2>Update Status</h2><form action='/update' method='post'>ID: <input name='id'><button type='submit'>Update</button></form><a href='/transaksi'>Kembali</a></body></html>"

# Simpan file HTML
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
with open("templates/transaksi.html", "w", encoding="utf-8") as f:
    f.write(transaksi_html)
with open("templates/update.html", "w", encoding="utf-8") as f:
    f.write(update_html)

print("✅ Semua file HTML berhasil dibuat di folder 'templates'")
