from flask import Flask

from app import models, resources, schemas

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)
schemas.ma.init_app(app)
resources.api.init_app(app)

@app.before_first_request
def create_tables():
    models.db.create_all()

if __name__ == "__main__":
    app.run(port=5000, debug=True)