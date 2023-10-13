from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.electro_scooter import ElectroScooter
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SWAGGER'] = {
        "title": "Electro Scooter API",
        "version": '0.1',
        "description": "This is a simple server.",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
    Swagger(app)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()