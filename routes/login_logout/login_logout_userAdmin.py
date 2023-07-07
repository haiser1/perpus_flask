from flask import render_template, jsonify, request, session, Blueprint, flash, redirect, url_for
from werkzeug.security import check_password_hash
from connection_db.data_base import db


login_logout_bp = Blueprint('login_logout_bp', __name__)

@login_logout_bp.route('/login_admin', methods=['GET','POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM petugas WHERE email = %s', (email,))
            data = cur.fetchone()
            if data is None:
                flash('Email or Password Wrong', 'danger')
                return render_template('login_admin.html')
            if check_password_hash(data[3], password):
                session['loggedin'] = True
                session['id'] = data[0]
                session['nama'] = data[1]
                session['email'] = data[2]
                session['role'] = data[6]
                return redirect(url_for('admin_bp.dashboard'))
            flash('Email or Password Wrong', 'danger')
            return render_template('login_admin.html')
            # return jsonify(message='email or password wrong'), 400        
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        
        finally:
            if cur:
                cur.close()
    return render_template('login_admin.html')
    
@login_logout_bp.route('/login_user', methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = None
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM anggota WHERE email = %s', (email,))
            data = cur.fetchone()
            if data is None:
                flash('Email or Password Wrong', 'danger')
                return render_template('login_user.html')
            if check_password_hash(data[3], password):
                session['loggedin'] = True
                session['nim'] = data[0]
                session['nama'] = data[1]
                session['email'] = data[2]
                session['role'] = data[6]
                return redirect(url_for('admin_bp.dashboard'))
            flash('Email or Password Wrong', 'danger')
            return render_template('login_user.html')
            # return jsonify(message='email or password wrong'), 400        
        except Exception as err:
            print(f'Error: {err}')
            return jsonify(message='terjadi kesalahan di server'), 500
        
        finally:
            if cur:
                cur.close()
    return render_template('login_user.html')

@login_logout_bp.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('login_logout_bp.login_admin'))
    except Exception as err:
        print(f'Error: {err}')
        return jsonify(message='terjadi kesalahan di server'), 500

@login_logout_bp.route('/logout_user')
def logout_user():
    try:
        session.clear()
        return redirect(url_for('login_logout_bp.login_user'))
    except Exception as err:
        print(f'Error: {err}')
        return jsonify(message='terjadi kesalahan di server'), 500
