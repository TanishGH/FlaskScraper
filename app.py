from flask import Flask
from models import db
from schema import ma
from config import Config
from view import product_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    
    app.register_blueprint(product_bp, url_prefix='/api')
    

    with app.app_context():
        db.create_all()
        print("Database tables created.")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

