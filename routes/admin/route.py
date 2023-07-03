from flask import render_template, jsonify, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from connection_db.data_base import db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/addAkunPetugas', methods=['POST'])
def add_akun_petugas():
    # if request.method == 'POST':
    nama = request.form['nama']
    email = request.form['email']
    password = request.form['password']
    alamat = request.form['alamat']
    no_tlp = request.form['no_tlp']
    
    cur = None
    try:
        cur = db.cursor()
        cur.execute('SELECT * FROM petugas where email = %s', (email,))
        data = cur.fetchone()
        if data:
            return jsonify(message='email sudah terdaftar'),400
        cur.execute('INSERT INTO petugas(nama,email,password,alamat,no_tlp) VALUES(%s,%s,%s,%s,%s)', (nama,email,generate_password_hash(password),alamat,no_tlp,))
        db.commit()
        return jsonify(message='akun berhasil ditambahkan'), 201
        
    except Exception as err:
        print(f'Error: {err}')
        return jsonify(message='gagal, terjadi kesalahan di server'), 500
    finally:
        if cur:
            cur.close()

@admin_bp.route('/dashboard')
def dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM buku')
            data = cur.fetchall()
            return jsonify(data),200
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()

@admin_bp.route('/addBook', methods=['POST'])
def add_book():
    if 'loggedin' in session and session['role'] == 'admin':
        # if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        id_petugas = session['id']

        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT judul_buku FROM buku WHERE judul_buku = %s', (judul,))
            data = cur.fetchone()
            if data:
                return jsonify(message='judul buku sudah ada'),400
            cur.execute('''INSERT INTO buku(judul_buku,penulis,penerbit,tahun_terbit,stok_buku,id_petugas)
            VALUES(%s,%s,%s,%s,%s,%s)''', (judul,penulis,penerbit,tahun_terbit,stok,id_petugas,))
            db.commit()
            return jsonify(message='buku berhasil di tambahkan'),201
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401
# admin
@admin_bp.route('/addAnggota', methods=['POST'])
def add_anggota():
    if 'loggedin' in session and session['role'] == 'admin':
        # if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        id_petugas = session['id']

        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota WHERE email = %s', (email,))
            data = cur.fetchone()
            if data:
                return jsonify(message='email sudah tedaftar'),400

            cur.execute('''INSERT INTO anggota(nim,nama,email,password,alamat,no_tlp,id_petugas) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s)''', (nim,nama,email,generate_password_hash(password),alamat,no_tlp,id_petugas,))
            db.commit()
            return jsonify(messgae='akun berhasil daftar'),201
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401

# admin
# peminajaman
@admin_bp.route('/pinjam', methods=['POST'])
def pinjam():
    if 'loggedin' in session and session['role'] == 'admin':
        # if request.method == 'POST':
        nim_peminjam = request.form['nim_peminjam']
        judul_buku = request.form['judul_buku']
        tgl_pinjam = datetime.now()
        tgl_kembali = tgl_pinjam + timedelta(days=7)
        id_petugas = session['id']
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM buku WHERE judul_buku = %s', (judul_buku))
            data = cur.fetchone()
            if data is None:
                return jsonify(message='judul buku tidak ditemukan'),404
            
            cur.execute('SELECT * FROM anggota WHERE nim = %s', (nim_peminjam))
            nim = cur.fetchone()
            if nim is None:
                return jsonify(message='nim tidak terdaftar'),404
            
            db.begin()
            cur.execute('''INSERT INTO pinjam_kembali(nim_anggota,judul_buku,tgl_pinjam,tgl_kembali,id_petugas) 
                        VALUES(%s,%s,%s,%s,%s)''', (nim_peminjam,judul_buku,tgl_pinjam,tgl_kembali,id_petugas,))

            cur.execute('UPDATE buku SET stok_buku = stok_buku - 1 WHERE judul_buku = %s', (judul_buku,))
            db.commit()
            return jsonify(message='berhasil'),201
            
            
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401

# admin
@admin_bp.route('/pengembalian', methods=['POST'])
def pengembalian():
    if 'loggedin' in session and session['role'] == 'admin':
        nim = request.form['nim']
        judul_buku = request.form['judul_buku']
        id_petugas = session['id']
        tgl_kembali = datetime.now()
        status = 'dikembalikan'
        status_pinjam = 'dipinjam'
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM pinjam_kembali WHERE nim_anggota = %s AND judul_buku = %s and status = %s', (nim, judul_buku,status_pinjam))
            data = cur.fetchone()
            if data is None:
                return jsonify(message='Data tidak ditemukan',data = data), 404
            db.begin()
            tgl_kembali_pinjam = data[4]
            if tgl_kembali > tgl_kembali_pinjam:
                hari_terlambat = (tgl_kembali - tgl_kembali_pinjam).days
                denda_per_day = 1000
                denda = hari_terlambat * denda_per_day
                cur.execute('''UPDATE pinjam_kembali SET denda = %s, status = %s, id_petugas = %s, tgl_kemabli = %s 
                            WHERE nim_anggota = %s AND judul_buku = %s''',
                            (denda,status,id_petugas,tgl_kembali,nim,judul_buku,))
                db.commit()
                return jsonify(message='Buku dikembalikan terlambat', denda=denda), 200
            else:
                db.begin()
                cur.execute('''UPDATE pinjam_kembali SET status = %s, id_petugas = %s,tgl_kembali = %s 
                            WHERE nim_anggota = %s AND judul_buku = %s''',
                            (status,id_petugas,tgl_kembali,nim,judul_buku,))
                db.commit()
                return jsonify(message='Buku dikembalikan tepat waktu'), 200
            
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            return jsonify(message='Terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    
    return jsonify(message='Unauthorized'), 401

# admin
@admin_bp.route('/getAllRiwayatAktif')
def get_all_riwayat_aktif():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = None
        status = 'dipinjam'
        try:
            cur = db.cursor()
            cur.execute('''SELECT pk.id, a.nama, a.nim,b.judul_buku, p.nama,pk.tgl_pinjam,pk.tgl_kembali 
                        FROM pinjam_kembali as pk, anggota as a, buku as b, petugas as p 
                        WHERE pk.nim_anggota = a.nim and pk.judul_buku = b.judul_buku and pk.id_petugas = p.id and status = %s''', (status,))
            data = cur.fetchall()
            if data:
                return jsonify(data),200
            return jsonify(message='not found'),404
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401

# admin

# admin
@admin_bp.route('/search', methods=['POST'])
def search():
    # Mendapatkan data pencarian dari permintaan POST
    judul_buku = request.form['searchTerm']

    cur = None
    # Membuat kursor database
    try:
        cursor = db.cursor()

        # Mengeksekusi query untuk mencari data di database
        query = "SELECT * FROM buku WHERE judul_buku LIKE %s"
        cursor.execute(query, (f'%{judul_buku}%',))

        # Mengambil semua hasil pencarian
        results = cursor.fetchall()
        if results:
            # Menyusun hasil pencarian menjadi list
            search_results = [row[0] for row in results]  # Menggunakan indeks kolom yang sesuai dengan kolom "nama_produk"
            # Menyusun hasil pencarian menjadi format JSON
            response = {
                'results': search_results
            }
        # Mengembalikan hasil pencarian dalam format JSON
            return jsonify(response),200
        return jsonify(message='buku tidak ditemukam'),404
    except Exception as err:
        print(f'Eror: {err}')
        return jsonify(message='terjadi kesalahan di server'), 500
    finally:
        if cur:
            cur.close()

@admin_bp.route('/index')
def index():
    return render_template('search.html')