


from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder="templates")

def get_db():
    conn = sqlite3.connect("laundry.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/simpan', methods=['POST'])
def simpan():
    conn = get_db()
    cursor = conn.cursor()

    nama = request.form['nama']
    nomor = request.form.get('nomor', '')
    berat = float(request.form.get('berat', 0))
    layanan = request.form.get('layanan', 'Cuci kering 3 hari')
    harga = int(request.form.get('harga', 7000))
    diskon = float(request.form.get('diskon', 0))
    status_bayar = request.form.get('status_bayar', 'Belum Lunas')
    status_ambil = request.form.get('status_ambil', 'Belum Diambil')

    subtotal = harga * berat
    diskon_rp = subtotal * (diskon / 100)
    total = subtotal - diskon_rp
    kasbon = 0 if status_bayar == "Sudah Lunas" else total
    tanggal_pesan = datetime.now().strftime("%d-%m-%Y %H:%M")
    tanggal_dibayar = tanggal_pesan if status_bayar == "Sudah Lunas" else "-"
    tanggal_diambil = tanggal_pesan if status_ambil == "Sudah Diambil" else "-"

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            nomor TEXT,
            berat REAL,
            layanan TEXT,
            harga_per_kg INTEGER,
            diskon_persen REAL,
            total REAL,
            kasbon REAL,
            status_pembayaran TEXT,
            status_pengambilan TEXT,
            tanggal_pesan TEXT,
            tanggal_dibayar TEXT,
            tanggal_diambil TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO transaksi (
            nama, nomor, berat, layanan, harga_per_kg, diskon_persen, total, kasbon,
            status_pembayaran, status_pengambilan, tanggal_pesan, tanggal_dibayar, tanggal_diambil
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nama, nomor, berat, layanan, harga, diskon, total, kasbon,
          status_bayar, status_ambil, tanggal_pesan, tanggal_dibayar, tanggal_diambil))
    conn.commit()
    return redirect('/transaksi')

@app.route('/transaksi')
def transaksi():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transaksi")
    data = cursor.fetchall()

    hari_ini = datetime.now().strftime("%d-%m-%Y")
    belum_lunas = []
    lunas_hari_ini = []
    lunas_lama = []

    for row in data:
        if row['status_pembayaran'] == "Belum Lunas":
            belum_lunas.append(row)
        elif row['status_pembayaran'] == "Sudah Lunas":
            if row['tanggal_dibayar'].startswith(hari_ini):
                lunas_hari_ini.append(row)
            else:
                lunas_lama.append(row)

    return render_template("transaksi.html", belum=belum_lunas, hari_ini=lunas_hari_ini, lama=lunas_lama)

@app.route('/update', methods=['POST'])
def update():
    id_transaksi = request.form['id']
    tanggal_bayar = datetime.now().strftime("%d-%m-%Y %H:%M")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transaksi
        SET status_pembayaran = 'Sudah Lunas',
            tanggal_dibayar = ?
        WHERE id = ?
    """, (tanggal_bayar, id_transaksi))
    conn.commit()
    return redirect('/transaksi')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def index():
    return "<h1>Halo dari Flask!</h1>"
