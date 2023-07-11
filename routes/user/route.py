from flask import render_template, request, session, Blueprint, abort, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from connection_db.data_base import db
from uuid import uuid4


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/update_data/<uid>')
def update_data(uid):
    if 'loggedin' in session and session['role'] == 'user':
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota WHERE uuid = %s', (uid))
            data = cur.fetchall()
            if not data:
                flash('Data Not Found', 'danger')
                return redirect(url_for('admin_bp.dashboard'))
            return(render_template('edit_user.html', datas=data))

        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:

            if cur:
                cur.close()
    abort(401)

@user_bp.route('/edit_user', methods=['POST'])
def edit_user():
    if 'loggedin' in session and session['role'] == 'user':
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        cur = None
        if nama and email and alamat and no_tlp:
            try:
                cur = db.cursor()
                cur.execute('UPDATE anggota SET nama = %s, email = %s, alamat = %s, no_tlp = %s WHERE uuid = %s', (nama,email,alamat,no_tlp,session['uuid'],))
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
        flash('Data Tidak Boleh Kosong', 'danger')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)    



@user_bp.route('/update_password/<uid>')
def update_password(uid):
    if 'loggedin' in session and session['role'] == 'user':
            cur = None
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE uuid = %s', (uid,))
                data = cur.fetchone()
                return render_template('password_user.html', datas = data)
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close() 
    abort(401)

@user_bp.route('/edit_password', methods=['POST'])
def edit_password():
    if 'loggedin' in session and session['role'] == 'user':
        password_lama = request.form['password_lama']
        password_baru = request.form['password_baru']
        uid = request.form['uid']
        cur = None
        if password_baru and password_lama: 
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE uuid = %s', (uid,))
                data = cur.fetchone()
                if data:
                    if check_password_hash(data[3], password_lama):
                        cur.execute('UPDATE anggota SET password = %s WHERE uuid = %s', (generate_password_hash(password_baru),uid))
                        db.commit()
                        flash('Password Berhasil Di Update', 'primary')
                        return redirect(url_for('admin_bp.dashboard'))
                flash('Password Salah', 'danger')
                return redirect(url_for('user_bp.update_password', uid=uid))
            except Exception as err:
                print(f'Error: {err}')
                abort(500)
            finally:
                if cur:
                    cur.close() 
        flash('Password Tidak Boleh Kosong', 'danger')
        return redirect(url_for('user_bp.update_password', uid=uid))
    abort(401)


@user_bp.route('/pinjamAktif')
def pinjam_aktif():
    if 'loggedin' in session and session['role'] == 'user':
        cur = None
        status = 'dipinjam'
        try:
            cur = db.cursor()
            cur.execute('''SELECT judul_buku,tgl_pinjam,tgl_batas_pinjam,denda 
                        FROM pinjam_kembali where nim_anggota = %s and status = %s''', (session['nim'],status,))
            data = cur.fetchall()
            return render_template('pinjam_user.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)

@user_bp.route('/history_peminjaman')
def history():
    if 'loggedin' in session and session['role'] == 'user':
        cur = None
        status = 'dikembalikan'
        try:
            cur = db.cursor()
            cur.execute('''SELECT judul_buku,tgl_pinjam,tgl_batas_pinjam,tgl_kembali,denda 
                        FROM pinjam_kembali where nim_anggota = %s and status = %s''', (session['nim'],status,))
            data = cur.fetchall()
            return render_template('riwayat_pinjam.html', datas=data)
        except Exception as err:
            print(f'Error: {err}')
            abort(500)
        finally:
            if cur:
                cur.close()
    abort(401)



