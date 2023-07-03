from flask import render_template, jsonify, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from connection_db.data_base import db
user_bf = Blueprint('user_bf', __name__)