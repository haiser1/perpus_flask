from flask import render_template, jsonify, request, session, Blueprint, abort, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from connection_db.data_base import db
from collections import OrderedDict

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/update_data/<nim>')
def update_data(nim):
    if 'loggedin' in session and session['role'] == 'user':
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota WHERE nim = %s', (nim))
            data = cur.fetchall()
            if data is None:
                flash('Data Not Found', 'danger')
                return redirect(url_for('admin_bp.dashboard'))
            return(render_template('edit_user.html', datas=data))

        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
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
                cur.execute('UPDATE anggota SET nama = %s, email = %s, alamat = %s, no_tlp = %s WHERE nim = %s', (nama,email,alamat,no_tlp,session['nim'],))
                db.commit()
                session['nama'] = nama
                flash('Data Berhasil Diupdate', 'primary')
                return redirect(url_for('admin_bp.dashboard'))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server,'), 500
            finally:
                if cur:
                    cur.close()
        flash('Data Invalid', 'danger')
        return redirect(url_for('admin_bp.dashboard'))
    abort(401)    



@user_bp.route('/update_password/<nim>')
def update_password(nim):
    if 'loggedin' in session and session['role'] == 'user':
            cur = None
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE nim = %s', (nim,))
                data = cur.fetchone()
                return render_template('password_user.html', datas = data)
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close() 
    abort(401)

@user_bp.route('/edit_password', methods=['POST'])
def edit_password():
    if 'loggedin' in session and session['role'] == 'user':
        password_lama = request.form['password_lama']
        password_baru = request.form['password_baru']
        nim = request.form['nim']
        cur = None
        if password_baru and password_lama: 
            try:
                cur = db.cursor()
                cur.execute('SELECT * FROM anggota WHERE nim = %s', (nim,))
                data = cur.fetchone()
                if data:
                    if check_password_hash(data[3], password_lama):
                        cur.execute('UPDATE anggota SET password = %s WHERE nim = %s', (generate_password_hash(password_baru),nim))
                        db.commit()
                        flash('Password Berhasil Di Update', 'primary')
                        return redirect(url_for('admin_bp.dashboard'))
                flash('Password Salah', 'danger')
                return redirect(url_for('user_bp.update_password', nim=nim))
            except Exception as err:
                print(f'Error: {err}')
                return jsonify(message='terjadi kesalahan di server'), 500
            finally:
                if cur:
                    cur.close() 
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
            db.rollback()
            return jsonify(message='terjadi kesalahan di server'), 500
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
            return jsonify(message='terjadi kesalahan di server'), 500
        finally:
            if cur:
                cur.close()
    return jsonify(message='Unauthorized'),401



