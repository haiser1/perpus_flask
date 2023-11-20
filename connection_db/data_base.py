import pymysql
from dotenv import load_dotenv
import os
load_dotenv()
try:
    db = pymysql.connect(
        host = os.getenv('HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        db = os.getenv('DB_NAME'),
        ssl = {'ca' :os.getenv('SSL')}
    )
    print('berhasil konek ke database')
    print(os.getenv('DB_NAME'))
except Exception as err:
    print(f'gagal konek ke database, error: {err}')