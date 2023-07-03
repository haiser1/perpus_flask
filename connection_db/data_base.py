import pymysql
from dotenv import load_dotenv
import os
load_dotenv()
try:
    db = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = os.getenv('PASSWORD') #ganti dengan password databases kalian default '',
        db = os.getenv('DB_NAME') #ganti dengan nama database
    )
    print('berhasil konek ke database')

except Exception as err:
    print(f'error: {err}')
