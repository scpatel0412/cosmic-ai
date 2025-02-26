from flask import Flask, jsonify, render_template, Response
import requests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.routes import user_bp, conversations_bp, chats_bp, stripe_bp, user_sub_bp
from app.pre_require import db
# from flask_restplus import Api
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()




def create_app():
    app = Flask(__name__)
    CORS(app)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger/swagger.json'

    # api = Api(app, version='1.0', title='CosmicAI', description='Swagger UI Documentation')
    print(os.getenv('JWT_SECRET'))

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Flask Swagger UI Example"
        }
    )


    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config['JWT_ALGORITHM'] = 'HS256'
    jwt = JWTManager(app)

    print(app.config)

    print(app.config['JWT_SECRET_KEY'] == os.getenv('JWT_SECRET'))

    @jwt.unauthorized_loader
    def missing_authorization_header(error):
        return jsonify({"message": "Unauthorized","status":401,"error":True}), 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        print(error)
        return jsonify({"msg": "Invalid Token"}), 401

    db.init_app(app)

    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        print("Home route accessed")
        return render_template('index.html')
    
    @app.route('/contact')
    def contact():
        print("Home route accessed")
        return render_template('contact.html')
    
    @app.route('/properties')
    def properties():
        print("Home route accessed")
        return render_template('properties.html')
    
    @app.route('/property-details')
    def properties_details():
        print("Home route accessed")
        return render_template('property-details.html')
    
    @app.route('/api/v1/greet')
    def greet():
        print("Home route accessed")
        return jsonify({"message":"Welcome to Cosmic AI"})


    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(user_bp,url_prefix='/api/v1')
    app.register_blueprint(conversations_bp,url_prefix='/api/v1')
    app.register_blueprint(chats_bp,url_prefix='/api/v1')
    app.register_blueprint(stripe_bp,url_prefix='/api/v1')
    app.register_blueprint(user_sub_bp,url_prefix='/api/v1')

    return app
