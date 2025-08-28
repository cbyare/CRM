from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}@"
        f"{app.config['DB_HOST']}:{app.config['DB_PORT']}/{app.config['DB_NAME']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
