from flask import Flask, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_restful import Api, Resource



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superhero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

class HeroResource(Resource):
    def get(self):
        heroes = Hero.query.all()

        return[
            hero.to_dict(
                only=("id", "name", "super_name")
            )
            for hero in heroes
        ], 200

class HeroByIdResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)

        if not hero:
            return {"error":"Hero not found"}, 404

        return hero.to_dict(
            rules=(
                "-hero_powers.hero",
                "-hero_powers.power.hero_powers",
            )
        ), 200    





if __name__ == "__main__":
    app.run(port=5555, debug=True)