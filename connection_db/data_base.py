import pymysql
from dotenv import load_dotenv
import os
load_dotenv()
try:
    db = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        db = 'perpus'
    )
    print('berhasil konek ke database')
except Exception as err:
    print(f'gagal konek ke database, error: {err}')