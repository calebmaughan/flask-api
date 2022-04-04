from flask import Flask

from app import models, resources, schemas

#Create and initialize the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)
schemas.ma.init_app(app)
resources.api.init_app(app)

#Create all tables for the demo
@app.before_first_request
def create_tables():
    models.db.create_all()

#Start the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)