import pymysql
from dotenv import load_dotenv
import os
load_dotenv()
try:
    db = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = os.getenv('PASSWORD'),
        db = os.getenv('DB_NAME')
    )
    print('berhasil konek ke database')

except Exception as err:
    print(f'error: {err}')