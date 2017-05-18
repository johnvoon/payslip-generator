import os

from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from resources.payslip import Payslip

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
api = Api(app)

api.add_resource(Payslip, '/api/generate_payslip_csv')


@app.route('/')
def home():
    """
    Home
    """
    return render_template('base.html')


@app.route('/payslip-generator')
def payslip_generator():
    """
    Payslip Generator
    """
    return render_template('base.html')


@app.route('/instructions')
def instructions():
    """
    Instructions
    """
    return render_template('base.html')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
