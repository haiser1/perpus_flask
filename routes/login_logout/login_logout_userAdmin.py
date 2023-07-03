from flask import render_template, jsonify, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from connection_db.data_base import db

login_logout_bp = Blueprint('login_logout_bp', __name__)

@login_logout_bp.route('/login', methods=['POST'])
def login():
    # if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    cur = None
    try:
        cur = db.cursor()
        cur.execute('SELECT * FROM petugas WHERE email = %s', (email,))
        data = cur.fetchone()
        print(data)
        if data:
            if check_password_hash(data[3], password):
                session['loggedin'] = True
                session['id'] = data[0]
                session['nama'] = data[1]
                session['email'] = data[2]
                session['role'] = data[6]
                return jsonify(message='berhasil login'),200
        
        return jsonify(message='email or password wrong'), 400        
    except Exception as err:
        print(f'Error: {err}')
        return jsonify(message='terjadi kesalahan di server'), 500
    
    finally:
        if cur:
            cur.close()

@login_logout_bp.route('/logout')
def logout():
    try:
        session.clear()
        return jsonify(message='berhasil logout')
    except Exception as err:
        print(f'Error: {err}')
        return jsonify(message='terjadi kesalahan di server'), 500
