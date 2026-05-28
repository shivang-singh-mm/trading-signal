from flask import Flask
from flask_cors import CORS
from db import db
from routes.signal_routes import signal_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)

app.register_blueprint(signal_bp)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)