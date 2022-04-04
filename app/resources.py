from flask import request, jsonify
from flask_restx import Api, Resource
from app import models, schemas

#Initialize restx
api = Api()

#Create a new user or view all users
@api.route('/user')
class UserRoute(Resource):
    def post(self):
        name = request.json['name']
        address = request.json['address']
        new_user = models.User(name, address)
        models.db.session.add(new_user)
        models.db.session.commit()
        return schemas.user_schema.jsonify(new_user)

    def get(self):
        all_users = models.User.query.all()
        result = schemas.users_schema.dump(all_users)
        return jsonify(result)

#View, update, or delete a specific user
@api.route('/user/<user_id>')
class SingleUserRoute(Resource):
    def get(self, user_id):
        magazine = models.User.query.get(user_id)
        return schemas.user_schema.jsonify(magazine)
    
    def put(self, user_id):
        user = models.User.query.get(user_id)
        user.name = request.json['name']
        user.address = request.json['address']
        models.db.session.commit()
        return schemas.user_schema.jsonify(user)

    def delete(self, user_id):
        user = models.User.query.get(user_id)
        models.db.session.delete(user)
        models.db.session.commit()
        return schemas.user_schema.jsonify(user)

#Create a new magazine or view all magazines
@api.route('/magazine')
class MagazineRoute(Resource):
    def get(self):
        all_magazines = models.Magazine.query.all()
        result = schemas.magazines_schema.dump(all_magazines)
        return jsonify(result)
    
    def post(self):
        name = request.json['name']
        new_magazine = models.Magazine(name)
        models.db.session.add(new_magazine)
        models.db.session.commit()
        return schemas.magazine_schema.jsonify(new_magazine)

#View, update, or delete a specific magazine
@api.route('/magazine/<magazine_id>')
class SingleMagazineRoute(Resource):
    def get(self, magazine_id):
        magazine = models.Magazine.query.get(magazine_id)
        return schemas.magazine_schema.jsonify(magazine)
    
    def put(self, magazine_id):
        magazine = models.Magazine.query.get(magazine_id)
        magazine.name = request.json['name']
        models.db.session.commit()
        return schemas.magazine_schema.jsonify(magazine)

    def delete(self, magazine_id):
        magazine = models.Magazine.query.get(magazine_id)
        models.db.session.delete(magazine)
        models.db.session.commit()
        return schemas.magazine_schema.jsonify(magazine)

#Pass a list of magazine ids to subscribe to for a specific user
@api.route('/user/<user_id>/subscribe')
class SubscribeRoute(Resource):
    def post(self, user_id):
        magazines = request.json['magazine_id']
        for magazine_id in magazines:
            user = models.User.query.get(user_id)
            magazine = models.Magazine.query.get(magazine_id)
            if(magazine not in user.subscriptions):
                user.subscriptions.append(magazine)
        models.db.session.commit()
        magazines = user.subscriptions
        result = schemas.magazines_schema.dump(magazines)
        return jsonify(result)

#Pass a list of magazine ids to unsubscribe from for a specific user
@api.route('/user/<user_id>/unsubscribe')
class UnsubscribeRoute(Resource):
    def post(self, user_id):
        magazines = request.json['magazine_id']
        for magazine_id in magazines:
            user = models.User.query.get(user_id)
            magazine = models.Magazine.query.get(magazine_id)
            if(magazine in user.subscriptions):
                user.subscriptions.remove(magazine)
        models.db.session.commit()
        magazines = user.subscriptions
        result = schemas.magazines_schema.dump(magazines)
        return jsonify(result)

#View a single user's subscriptions
@api.route('/user/<user_id>/subscriptions')
class SubscriptionsRoute(Resource):
    def get(self, user_id):
        user = models.User.query.get(user_id)
        magazines = user.subscriptions
        result = schemas.magazines_schema.dump(magazines)
        return jsonify(result)

#View a single magazine's subscribers
@api.route('/magazine/<magazine_id>/subscribers')
class SubscribersRoute(Resource):
    def get(self, magazine_id):
        magazine = models.Magazine.query.get(magazine_id)
        users = magazine.subscribers
        result = schemas.users_no_subscriptions_schema.dump(users)
        return jsonify(result)