from flask import Flask
from routes.admin.route import admin_bp
from routes.user.route import user_bf
from dotenv import load_dotenv
import os
from routes.login_logout.login_logout_userAdmin import login_logout_bp
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(admin_bp)
app.register_blueprint(user_bf)
app.register_blueprint(login_logout_bp)

if __name__ == '__main__':
    app.run(debug=True)