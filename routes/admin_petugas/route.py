from flask import render_template, jsonify, request, session, Blueprint, abort, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from connection_db.data_base import db
import uuid


admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        cur = None
        status_pinjam = 'dipinjam'
        status_kembali = 'dikembalikan'
        try:
            cur = db.cursor()
            cur.execute(''' SELECT
                        (SELECT COUNT(*) FROM buku) AS jml_petugas,
                        (SELECT COUNT(*) FROM anggota) AS jml_anggota,
                        (SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s) as jml_buku_dipinjam ,
                        (SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s) as jml_buku_dikembalikan''',
                        (status_pinjam, status_kembali,))
            data = cur.fetchall()

            # cur.execute('SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s', (status_pinjam,))
            # dipinjam = cur.fetchall()

            # cur.execute('SELECT COUNT(*) FROM pinjam_kembali WHERE status = %s', (status_kembali,))
            # dikembalikan = cur.fetchall()
            return render_template('dashboard.html', data = data)
            
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    elif 'loggedin' in session and session['role'] == 'user':
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE uuid = %s', (session['uuid']))
                data_user = cur.fetchall()
                return render_template('dashboard.html', users = data_user)
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close()
    abort(401)

@admin_bp.route('/petugas')
def petugas():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas')
            data = cur.fetchall()
            return render_template('petugas.html', datas = data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/addAkunPetugas', methods=['POST'])
def add_petugas():
    if 'loggedin' in session and session['role'] == 'admin':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        role = request.form['role']
        uid = str(uuid.uuid4())
        nama = nama.title()
        cur = None
        if nama and email and password and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM petugas where email = %s', (email,))
                data = cur.fetchone()
                if data:
                    flash('Email Sudah Terdaftar', 'danger')
                    return redirect(url_for('admin_bp.petugas'))
                cur.execute('''INSERT INTO petugas(nama,email,password,alamat,no_tlp,uuid,role) VALUES(%s,%s,%s,%s,%s,%s,%s)''', 
                            (nama,email,generate_password_hash(password),alamat,no_tlp,uid,role,))
                db.commit()
                flash('Akun Berhasil Didaftar', 'primary')
                return redirect(url_for('admin_bp.petugas'))
                
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kososng', 'danger')
        return redirect(url_for('admin_bp.petugas'))
    abort(401)

@admin_bp.route('/update_petugas/<uid>')
def update_petugas(uid):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute(' select * from petugas where uuid = %s ', (uid,))
            data = cur.fetchall()
            if not data:
                flash('Data Not Found', 'danger')
                return redirect(url_for('admin_bp.petugas'))
            return render_template('edit_petugas.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/edit_petugas',methods=['POST'] )
def edit_petugas():
    if 'loggedin' in session and session['role'] == 'admin':
        uid = request.form['uid']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        role = request.form['role']
        nama = nama.title()
        if nama and email and alamat and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('''UPDATE petugas SET nama = %s, email = %s, alamat = %s, no_tlp = %s, role = %s WHERE uuid = %s''', (nama,email,alamat,no_tlp,role,uid,))
                db.commit()
                session['nama'] = nama
                flash('Data Berhasil Diupdate', 'primary')
                return redirect(url_for('admin_bp.petugas'))
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)

@admin_bp.route('/edit_petugas/me',methods=['POST'] )
def edit_petugas_me():
    if 'loggedin' in session and session['role'] == 'petugas':
        uid = request.form['uid']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        nama = nama.title()
        if nama and email and alamat and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('''UPDATE petugas SET nama = %s, email = %s, alamat = %s, no_tlp = %s WHERE uuid = %s''', (nama,email,alamat,no_tlp,uid,))
                db.commit()
                session['nama'] = nama
                flash('Data Berhasil Diupdate', 'primary')
                return redirect(url_for('admin_bp.dashboard'))
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)

@admin_bp.route('/show_me/<uid>')
def show_me(uid):
    if 'loggedin' in session and session['role'] == 'petugas':
        try:
            cur = db.cursor()
            cur.execute(' select * from petugas where uuid = %s ', (uid,))
            data = cur.fetchall()
            if not data:
                flash('Data Not Found', 'danger')
                return redirect(url_for('admin_bp.dashboard'))
            return render_template('edit_petugas_me.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/change_passwd/<uid>')
def password_change(uid):
        if 'loggedin' in session and session['role'] == 'admin':
            cur = None
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM petugas WHERE uuid = %s', (uid,))
                data = cur.fetchone()
                print(data)
                return render_template('password_petugas.html', datas = data)
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close() 
        abort(401)
@admin_bp.route('/update_passwd/me/<uid>')
def update_pass_me(uid):
    if 'loggedin' in session and session['role'] == 'petugas':
            cur = None
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM petugas WHERE uuid = %s', (uid,))
                data = cur.fetchone()
                return render_template('password_petugas_me.html', datas = data)
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close() 
    abort(401)

@admin_bp.route('/update_passwd', methods=['POST'])
def password_update():
    if 'loggedin' in session and session['role'] == 'admin':
        old_passwd = request.form['password_lama']
        new_passwd = request.form['password_baru']
        uid = request.form['uid']
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas WHERE uuid = %s', (uid,))
            data = cur.fetchone()
            if not data:
                flash('Password Salah', 'danger')
                return redirect(url_for('admin_bp.password_change', uid=uid))
            if not check_password_hash(data[3], old_passwd):
                flash('Password Salah', 'danger')
                return redirect(url_for('admin_bp.password_change', uid=uid))   
            cur.execute('UPDATE petugas SET password = %s where uuid = %s', (generate_password_hash(new_passwd), uid,))
            db.commit()
            flash('Password Berhasil Diupdate', 'primary')
            return redirect(url_for('admin_bp.petugas'))
            
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close() 
    abort(401)  

@admin_bp.route('/update_passwd/me', methods=['POST'])
def password_update_me():
    if 'loggedin' in session and session['role'] == 'petugas':
        old_passwd = request.form['password_lama']
        new_passwd = request.form['password_baru']
        uid = request.form['uid']
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas WHERE uuid = %s', (uid,))
            data = cur.fetchone()
            if not data:
                flash('Password Salah', 'danger')
                return redirect(url_for('admin_bp.update_pass_me', uid=uid))
            if not check_password_hash(data[3], old_passwd):
                flash('Password Salah', 'danger')
                return redirect(url_for('admin_bp.update_pass_me', uid=uid))   
            cur.execute('UPDATE petugas SET password = %s where uuid = %s', (generate_password_hash(new_passwd), uid,))
            db.commit()
            flash('Password Berhasil Diupdate', 'primary')
            return redirect(url_for('admin_bp.dashboard'))
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close() 
    abort(401)  

@admin_bp.route('/delete_petugas/<uid>')
def delete_petugas(uid):
    if 'loggedin' in session and session['role'] == 'admin':
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM petugas WHERE uuid = %s', (uid,))
            db.commit()
            flash('Data Berhasil Dihapus', 'primary')
            return redirect(url_for('admin_bp.petugas'))

        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/user')
def user():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT a.*, p.nama FROM anggota AS a, petugas AS p WHERE a.id_petugas = p.id')
            data = cur.fetchall()
            return render_template('users.html', datas = data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close() 
    abort(401)

@admin_bp.route('/addAnggota', methods=['POST'])
def add_anggota():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        nim = request.form['nim']
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        id_petugas = session['id']
        nama = nama.title()
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
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.user'))
    abort(401)

@admin_bp.route('/show_user/<uid>')
def show_anggota(uid):
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota WHERE uuid = %s', (uid))
            data = cur.fetchall()
            if not data:
                flash('Data Not Found', 'danger')
                return redirect(url_for('admin_bp.dashboard'))
            return(render_template('edit_user_byadmin.html', datas=data))
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)
    
@admin_bp.route('/edit_user/byadmin', methods=['POST'])
def edit_user():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        uid = request.form['uid']
        nama = nama.title()

        cur = None
        if nama and email and alamat and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('UPDATE anggota SET nama = %s, email = %s, alamat = %s, no_tlp = %s, id_petugas = %s WHERE uuid = %s', (nama,email,alamat,no_tlp,session['id'],uid,))
                db.commit()
                session['nama'] = nama
                flash('Data Berhasil Diupdate', 'primary')
                return redirect(url_for('admin_bp.user'))
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)

@admin_bp.route('/delete_user/<nim>')
def delete_user(nim):
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM anggota WHERE nim = %s', (nim,))
            db.commit()
            return redirect(url_for('admin_bp.user'))

        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

        
@admin_bp.route('/books')
def books():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('SELECT b.*, p.nama FROM buku as b, petugas as p WHERE p.id = b.id_petugas')
            data = cur.fetchall()

            cur.execute('SELECT SUM(stok_buku) FROM buku')
            stok = cur.fetchone()
            return render_template('books.html', datas = data, stok=stok)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)


@admin_bp.route('/addBook', methods=['POST'])
def add_book():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        judul = request.form['judul']
        uid = str(uuid.uuid4())
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        id_petugas = session['id']
        judul = judul.title()
        penulis = penulis.title()
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
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.books'))
    abort(401)

@admin_bp.route('/edit_book/<id>')
def edit_book(id):
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM buku WHERE uuid = %s', (id,))
            data = cur.fetchall()
            return render_template('edit_books.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/updateBook', methods=['POST'])
def update_book():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        id_petugas = session['id']
        uid = request.form['id']
        judul = judul.title()
        penulis = penulis.title()
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
                abort(500)
            finally:
                if cur:
                    cur.close()
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.books'))
    abort(401)

@admin_bp.route('/delete_book/<id>')
def delete_book(id):
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('DELETE FROM buku WHERE uuid = %s', (id,))
            db.commit()
            flash('Data Berhasil Dihapus', 'primary')
            return redirect(url_for('admin_bp.books'))
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/show')
def show():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
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
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@admin_bp.route('/pinjam', methods=['POST'])
def pinjam():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        nim_peminjam = request.form['nim']
        judul_buku = request.form['judul']
        tgl_pinjam = datetime.now()
        tgl_batas_pinjam = tgl_pinjam + timedelta(days=7)
        id_petugas = session['id']
        cur = None
        try:
            cur = db.cursor()
            db.begin()
            cur.execute('''INSERT INTO pinjam_kembali(nim_anggota,judul_buku,tgl_pinjam,tgl_batas_pinjam,id_petugas) 
                        VALUES(%s,%s,%s,%s,%s)''', (nim_peminjam,judul_buku,tgl_pinjam,tgl_batas_pinjam,id_petugas,))

            cur.execute('UPDATE buku SET stok_buku = stok_buku - 1 WHERE judul_buku = %s', (judul_buku,))
            db.commit()
            flash('Peminjaman Berhasil', 'primary')
            return redirect(url_for('admin_bp.show'))
             
        except Exception as err:
            print(f'Error: {err}')
            db.rollback()
            abort(500)
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401

@admin_bp.route('/perpanjang/<id>')
def update_deadline(id):
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        try:
            cur = db.cursor()
            cur.execute('SELECT tgl_batas_pinjam FROM pinjam_kembali WHERE id = %s', (id,))
            data = cur.fetchone()
            update_day = data[0] + timedelta(days=7)

            cur.execute('UPDATE pinjam_kembali SET tgl_batas_pinjam = %s WHERE id = %s', (update_day,id,))
            db.commit()
            flash('Batas Pinjam Berhasil Diupdate', 'primary')
            return redirect(url_for('admin_bp.show'))
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)


@admin_bp.route('/show_pengembalian')
def show_pengembalian():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
        status = 'dikembalikan'
        try:
            cur = db.cursor()
            cur.execute('''SELECT pk.*, p.nama, a.nama FROM 
                        pinjam_kembali as pk, petugas as p, anggota as a 
                        WHERE p.id = pk.id_petugas and a.nim=pk.nim_anggota and pk.status = %s''', (status))
            data = cur.fetchall()

            
            return render_template('pengembalian.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

# admin
@admin_bp.route('/pengembalian', methods=['POST'])
def pengembalian():
    if 'loggedin' in session and (session['role'] == 'admin' or session['role'] == 'petugas'):
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
            tgl_batas_pinjam = data[4]
            if tgl_kembali > tgl_batas_pinjam:
                hari_terlambat = (tgl_kembali - tgl_batas_pinjam).days
                denda = hari_terlambat * 1000
                db.begin()
                cur.execute('''UPDATE pinjam_kembali SET denda = %s, status = %s, id_petugas = %s, tgl_kembali = %s 
                            WHERE nim_anggota = %s AND judul_buku = %s''',
                            (denda,status,id_petugas,tgl_kembali,nim,judul_buku,))
                
                cur.execute('''UPDATE buku set stok_buku = stok_buku + 1 WHERE judul_buku = %s''', (judul_buku,))
                db.commit
                flash(f'Buku Terlambat Dikembalikan Selama {hari_terlambat} hari Denda = {denda}', 'primary')
                return redirect(url_for('admin_bp.show_pengembalian'))
            else:
                db.begin()
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
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(500)