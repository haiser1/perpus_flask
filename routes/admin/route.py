from flask import render_template, jsonify, request, session, Blueprint, abort, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from connection_db.data_base import db
import uuid


admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = None
        status_pinjam = 'dipinjam'
        status_kembali = 'dikembalikan'
        try:
            cur = db.cursor()
            cur.execute(''' SELECT
                        (SELECT COUNT(*) FROM buku) AS jml_petugas,
                        (SELECT COUNT(*) FROM anggota) AS jml_anggota''')
            data = cur.fetchall()

            cur.execute('SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s', (status_pinjam,))
            dipinjam = cur.fetchall()

            cur.execute('SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s', (status_kembali,))
            dikembalikan = cur.fetchall()
            return render_template('dashboard.html', data = data, pinjam = dipinjam, kembali = dikembalikan)
            
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    if 'loggedin' in session and session['role'] == 'user':
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE nim = %s', (session['nim']))
                data_user = cur.fetchall()
                return render_template('dashboard.html', users = data_user)
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close()
    abort(401)

@admin_bp.route('/petugas')
def petugas():
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas')
            data = cur.fetchall()
            return render_template('petugas.html', datas = data)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/addAkunPetugas', methods=['POST'])
def add_petugas():
    if 'loggedin' in session and session['role'] == 'admin':
        # if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        
        cur = None
        if nama and email and password and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM petugas where email = %s', (email,))
                data = cur.fetchone()
                if data:
                    flash('Email Sudah Terdaftar', 'danger')
                    return redirect(url_for('admin_bp.petugas'))
                cur.execute('INSERT INTO petugas(nama,email,password,alamat,no_tlp) VALUES(%s,%s,%s,%s,%s)', (nama,email,generate_password_hash(password),alamat,no_tlp,))
                db.commit()
                flash('Akun Berhasil Didaftar', 'primary')
                return redirect(url_for('admin_bp.petugas'))
                
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='gagal, terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kososng', 'danger')
        return redirect(url_for('admin_bp.petugas'))
    return jsonify(message='Unauthorized'),401

@admin_bp.route('/update_petugas/<id>')
def update_petugas(id):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute(' select * from petugas where id = %s ', (id,))
            data = cur.fetchall()
            return render_template('edit_petugas.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/edit_petugas',methods=['POST'] )
def edit_petugas():
    if 'loggedin' in session and session['role'] == 'admin':
        id = request.form['id']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        # int(id)
        if nama and email and alamat and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('''UPDATE petugas SET nama = %s, email = %s, alamat = %s, no_tlp = %s WHERE id = %s''', (nama,email,alamat,no_tlp,id,))
                db.commit()
                session['nama'] = nama
                flash('Data Berhasil Diupdate', 'primary')
                return redirect(url_for('admin_bp.petugas'))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='gagal, terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)

@admin_bp.route('/me')
def update_me():
    if 'loggedin' in session and session['role'] == 'admin':
        pass

@admin_bp.route('/change_passwd/<id>')
def password_change(id):
        if 'loggedin' in session and session['role'] == 'admin':
            cur = None
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM petugas WHERE id = %s', (id,))
                data = cur.fetchone()
                return render_template('password_petugas.html', datas = data)
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close() 
        abort(401)
@admin_bp.route('/update_passwd', methods=['POST'])
def password_update():
    if 'loggedin' in session and session['role'] == 'admin':
        old_passwd = request.form['password_lama']
        new_passwd = request.form['password_baru']
        id = request.form['id']
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas WHERE id = %s', (id,))
            data = cur.fetchone()
            if data:
                if check_password_hash(data[3], old_passwd):
                    cur.execute('UPDATE petugas SET password = %s where id = %s', (generate_password_hash(new_passwd), id,))
                    db.commit()
                    flash('Password Berhasil Diupdate', 'primary')
                    return redirect(url_for('admin_bp.petugas'))
            flash('Password Salah', 'danger')
            return redirect(url_for('admin_bp.password_change', id=id))
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close() 
    abort(401)  

@admin_bp.route('/delete_petugas/<id>')
def delete_petugas(id):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM petugas WHERE id = %s', (id,))
            db.commit()
            return redirect(url_for('admin_bp.petugas'))

        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/user')
def user():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota')
            data = cur.fetchall()
            return render_template('users.html', datas = data)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close() 
    abort(401)

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
        if nim and nama and email and password and alamat and no_tlp:

            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE email = %s', (email,))
                data = cur.fetchone()
                if data:
                    return jsonify(message='email sudah tedaftar'),400

                cur.execute('''INSERT INTO anggota(nim,nama,email,password,alamat,no_tlp,id_petugas) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s)''', (nim,nama,email,generate_password_hash(password),alamat,no_tlp,id_petugas,))
                db.commit()
                flash('Akun Berhasil Didaftar', 'primary')
                return redirect(url_for('admin_bp.user'))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.user'))
    return jsonify(message='Unauthorized'),401

@admin_bp.route('/delete_user/<nim>')
def delete_user(nim):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM anggota WHERE nim = %s', (nim,))
            db.commit()
            return redirect(url_for('admin_bp.user'))

        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

        
@admin_bp.route('/books')
def books():
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('SELECT b.*, p.nama FROM buku as b, petugas as p WHERE p.id = b.id_petugas ')
            data = cur.fetchall()

            cur.execute('SELECT SUM(stok_buku) FROM buku')
            stok = cur.fetchone()
            return render_template('books.html', datas = data, stok=stok)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)


@admin_bp.route('/addBook', methods=['POST'])
def add_book():
    if 'loggedin' in session and session['role'] == 'admin':
        judul = request.form['judul']
        uid = str(uuid.uuid4())
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        id_petugas = session['id']
        cur = None
        if judul and penulis and penerbit and tahun_terbit and stok:
            try:
                cur = db.cursor()
                cur.execute('SELECT judul_buku FROM buku WHERE judul_buku = %s', (judul,))
                data = cur.fetchone()
                if data:
                    flash('Judul Buku Sadah Terdaftar', 'danger')
                    return redirect(url_for('admin_bp.books'))
                cur.execute('''INSERT INTO buku(judul_buku,penulis,penerbit,tahun_terbit,stok_buku,id_petugas, uuid)
                VALUES(%s,%s,%s,%s,%s,%s,%s)''', (judul,penulis,penerbit,tahun_terbit,stok,id_petugas,uid,))
                db.commit()
                flash('Data Berhasil Ditambahkan', 'primary')
                return redirect(url_for('admin_bp.books'))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server', Error=err), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.books'))
    abort(401)

@admin_bp.route('/edit_book/<id>')
def edit_book(id):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM buku WHERE uuid = %s', (id,))
            data = cur.fetchall()
            return render_template('edit_books.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/updateBook', methods=['POST'])
def update_book():
    if 'loggedin' in session and session['role'] == 'admin':
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        id_petugas = session['id']
        uid = request.form['id']
        cur = None
        if judul and penulis and penerbit and tahun_terbit and stok:
            try:
                cur = db.cursor()
                cur.execute('''UPDATE buku SET judul_buku = %s, penulis = %s, penerbit = %s, tahun_terbit = %s, stok_buku = %s,
                id_petugas = %s WHERE uuid = %s''', (judul,penulis,penerbit,tahun_terbit,stok,id_petugas,uid,))
                db.commit()
                flash('Data Berhasil DiUpdate', 'primary')
                return redirect(url_for('admin_bp.books'))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.books'))
    abort(401)

@admin_bp.route('/delete_book/<id>')
def delete_book(id):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM buku WHERE uuid = %s', (id,))
            db.commit()
            flash('Data Berhasil Dihapus', 'primary')
            return redirect(url_for('admin_bp.books'))
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/show')
def show():
    if 'loggedin' in session and session['role'] == 'admin':
        status = 'dipinjam'
        try:
            cur = db.cursor()
            cur.execute('''SELECT pk.*, p.nama, a.nama FROM 
                        pinjam_kembali as pk, petugas as p, anggota as a 
                        WHERE p.id = pk.id_petugas and a.nim=pk.nim_anggota and pk.status = %s''', (status))
            data = cur.fetchall()

            cur.execute('SELECT nim FROM anggota')
            result = cur.fetchall()

            cur.execute('SELECT judul_buku FROM buku')
            judul_buku = cur.fetchall() 
            return render_template('pinjam.html', datas=data, result=result, judul_buku=judul_buku)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/pinjam', methods=['POST'])
def pinjam():
    if 'loggedin' in session and session['role'] == 'admin':
        nim_peminjam = request.form['nim']
        judul_buku = request.form['judul']
        tgl_pinjam = datetime.now()
        tgl_batas_pinjam = tgl_pinjam + timedelta(days=7)
        id_petugas = session['id']
        cur = None
        try:
            cur = db.cursor()
            # cur.execute('SELECT * FROM buku WHERE judul_buku = %s', (judul_buku))
            # data = cur.fetchone()
            # if data is None:
            #     return jsonify(message='judul buku tidak ditemukan'),404
            
            # cur.execute('SELECT * FROM anggota WHERE nim = %s', (nim_peminjam))
            # nim = cur.fetchone()
            # if nim is None:
            #     return jsonify(message='nim tidak terdaftar'),404
            db.begin()
            cur.execute('''INSERT INTO pinjam_kembali(nim_anggota,judul_buku,tgl_pinjam,tgl_batas_pinjam,id_petugas) 
                        VALUES(%s,%s,%s,%s,%s)''', (nim_peminjam,judul_buku,tgl_pinjam,tgl_batas_pinjam,id_petugas,))

            cur.execute('UPDATE buku SET stok_buku = stok_buku - 1 WHERE judul_buku = %s', (judul_buku,))
            db.commit()
            flash('Success', 'primary')
            return redirect(url_for('admin_bp.show'))
             
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401

@admin_bp.route('/perpanjang/<id>')
def update_deadline(id):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('SELECT tgl_batas_pinjam FROM pinjam_kembali WHERE id = %s', (id,))
            data = cur.fetchone()
            # day = data[0]
            update_day = data[0] + timedelta(days=7)

            cur.execute('UPDATE pinjam_kembali SET tgl_batas_pinjam = %s WHERE id = %s', (update_day,id,))
            db.commit()
            flash('Batas Pinjam Berhasil Diupdate', 'primary')
            return redirect(url_for('admin_bp.show'))
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
            # return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)


@admin_bp.route('/show_pengembalian')
def show_pengembalian():
    if 'loggedin' in session and session['role'] == 'admin':
        status = 'dikembalikan'
        try:
            cur = db.cursor()
            cur.execute('''SELECT pk.*, p.nama, a.nama FROM 
                        pinjam_kembali as pk, petugas as p, anggota as a 
                        WHERE p.id = pk.id_petugas and a.nim=pk.nim_anggota and pk.status = %s''', (status))
            data = cur.fetchall()

            cur.execute('SELECT nim FROM anggota')
            result = cur.fetchall()

            cur.execute('SELECT judul_buku FROM buku')
            judul_buku = cur.fetchall() 
            return render_template('pengembalian.html', datas=data, result=result, judul_buku=judul_buku)
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='gagal, terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    abort(401)

# admin
@admin_bp.route('/pengembalian', methods=['POST'])
def pengembalian():
    if 'loggedin' in session and session['role'] == 'admin':
        nim = request.form['nim']
        judul_buku = request.form['judul']
        id_petugas = session['id']
        tgl_kembali = datetime.now()
        # tgl_kembali = tgl_kembali + timedelta(days=10)
        status = 'dikembalikan'
        status_pinjam = 'dipinjam'
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM pinjam_kembali WHERE nim_anggota = %s AND judul_buku = %s and status = %s', (nim, judul_buku,status_pinjam))
            data = cur.fetchone()
            if data is None:
                flash('Data Salah', 'danger')
                return redirect(url_for('admin_bp.show_pengembalian'))
            db.begin()
            tgl_batas_pinjam = data[4]
            if tgl_kembali > tgl_batas_pinjam:
                hari_terlambat = (tgl_kembali - tgl_batas_pinjam).days
                denda = hari_terlambat * 1000
                db.begin()
                cur.execute('''UPDATE pinjam_kembali SET denda = %s, status = %s, id_petugas = %s, tgl_kembali = %s 
                            WHERE nim_anggota = %s AND judul_buku = %s''',
                            (denda,status,id_petugas,tgl_kembali,nim,judul_buku,))
                
                cur.execute('''UPDATE buku set stok_buku = stok_buku + 1 WHERE judul_buku = %s''', (judul_buku,))

                flash(f'Buku Terlambat Dikembalikan Selama {hari_terlambat} hari Denda = {denda}', 'primary')
                return redirect(url_for('admin_bp.show_pengembalian'))
            else:
                
                cur.execute('''UPDATE pinjam_kembali SET status = %s, id_petugas = %s,tgl_kembali = %s 
                            WHERE nim_anggota = %s AND judul_buku = %s''',
                            (status,id_petugas,tgl_kembali,nim,judul_buku,))
                
                cur.execute('''UPDATE buku set stok_buku = stok_buku + 1 WHERE judul_buku = %s''', (judul_buku,))
                db.commit()
                flash('Buku Dikembalikan Tepat Waktu denda = 0', 'primary')
                return redirect(url_for('admin_bp.show_pengembalian'))
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            return jsonify(message='Terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'), 401

# admin
@admin_bp.route('/getAllPinjamAktif')
def get_all_riwayat_aktif():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = None
        status = 'dipinjam'
        try:
            cur = db.cursor()
            cur.execute('''SELECT pk.id, a.nama, a.nim,b.judul_buku, p.nama,pk.tgl_pinjam,pk.tgl_batas_pinjam 
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

@admin_bp.route('/getAllriwayat')
def all_riwayat():
    pass



# admin

# admin
@admin_bp.route('/search', methods=['POST'])
def search():
    if 'loggedin' in session and session['role'] == 'admin':
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

    return jsonify(message='Unauthorized'),401
@admin_bp.route('/index')
def index():
    return render_template('search.html')