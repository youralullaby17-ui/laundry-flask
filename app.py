
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inisialisasi database
def init_db():
    conn = sqlite3.connect('laundry.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    layanan TEXT,
                    berat REAL,
                    total REAL,
                    status TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simpan', methods=['POST'])
def simpan():
    nama = request.form['nama']
    layanan = request.form['layanan']
    berat = float(request.form['berat'])
    harga_per_kg = 7000 if layanan == 'Cuci Kering' else 10000
    total = berat * harga_per_kg
    status = 'Belum Dicuci'

    conn = sqlite3.connect('laundry.db')
    c = conn.cursor()
    c.execute("INSERT INTO transaksi (nama, layanan, berat, total, status) VALUES (?, ?, ?, ?, ?)",
              (nama, layanan, berat, total, status))
    conn.commit()
    conn.close()
    return redirect(url_for('transaksi'))

@app.route('/transaksi')
def transaksi():
    conn = sqlite3.connect('laundry.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transaksi")
    data = c.fetchall()
    conn.close()
    return render_template('transaksi.html', data=data)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        status = request.form['status']
        conn = sqlite3.connect('laundry.db')
        c = conn.cursor()
        c.execute("UPDATE transaksi SET status=? WHERE id=?", (status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('transaksi'))
    else:
        conn = sqlite3.connect('laundry.db')
        c = conn.cursor()
        c.execute("SELECT * FROM transaksi WHERE id=?", (id,))
        data = c.fetchone()
        conn.close()
        return render_template('update.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
