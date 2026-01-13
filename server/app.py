from flask import Flask, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_restful import Api, Resource



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superhero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class HeroResource(Resource):
# GET /heroes
# Returns a list of all heroes with limited fields
   def get(self):
    heroes = Hero.query.all()

    return [
        hero.to_dict(
            only=("id", "name", "super_name")  # exclude relationships
        )
        for hero in heroes
    ], 200


class HeroByIdResource(Resource):
    # GET /heroes/<id>
    # Returns a single hero with nested hero_powers
    def get(self, id):
        hero = Hero.query.get(id)

        # Handle hero not found
        if not hero:
            return {"error": "Hero not found"}, 404

        # Serialize hero while preventing infinite recursion
        return hero.to_dict(
            rules=(
                "-hero_powers.hero",               # avoid hero → hero_powers → hero loop
                "-hero_powers.power.hero_powers",  # avoid power → hero_powers loop
            )
        ), 200    


class PowersResource(Resource):
    # GET /powers
    # Returns all powers without relationships
    def get(self):
        powers = Power.query.all()

        return [
            power.to_dict(
                only=("id", "name", "description")  # flat power representation
            )
            for power in powers
        ], 200
    

class PowerByIdResource(Resource):
    # GET /powers/<id>
    # Returns a single power if it exists
    def get(self, id):
        power = Power.query.get(id)

        # Handle power not found
        if not power:
            return {"error": "Power not found"}, 404

        return power.to_dict(only=("id", "name", "description")), 200
    
    # PATCH /powers/<id>
    # Updates the description of an existing power
    def patch(self, id):
        power = Power.query.get(id)

        # Handle power not found
        if not power:
            return {"error": "Power not found"}, 404
        
        data = request.get_json()

        try:
            # Update description (validated at model level)
            if "description" in data:
                power.description = data["description"]

            db.session.commit()

            # Successful update response
            return power.to_dict( only=("id", "name", "description")), 200
        
        except ValueError as e:
            # Roll back transaction on validation failure
            db.session.rollback()
            return {"errors": [str(e)]}, 400
        
class HeroPowersResource(Resource):
    def post(self):

        data = request.get_json()
        # Create a new HeroPower with request data
        try:
            hero_power = HeroPower(
                strength = data.get("strength"),
                hero_id = data.get("hero_id"),
                power_id = data.get("power_id")
            )
            db.session.add(hero_power)
            db.session.commit()

            return hero_power.to_dict(
                rules=(
                    "-hero.hero_powers",
                    "-powers.hero_powers",
                )
            ), 201

        except ValueError as e:
            # Validation errors from models i.e (stregnth, name, id etc)
            db.session.rollback()
            return {"errors": [str(e)]}, 400
    
api.add_resource(HeroResource, "/heroes")
api.add_resource(HeroByIdResource, "/heroes/<int:id>")    

api.add_resource(PowersResource, "/powers")
api.add_resource(PowerByIdResource, "/powers/<int:id>")

api.add_resource(HeroPowersResource, "/hero_powers")

         



if __name__ == "__main__":
    app.run(port=5555, debug=True)