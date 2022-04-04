from flask_marshmallow import Marshmallow
from app import models

ma = Marshmallow()

#Schema for magazine object
class MagazineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Magazine
        include_fk = True

magazines_schema = MagazineSchema(many=True)
magazine_schema = MagazineSchema()

#Schema for user object
class UserSchema(ma.SQLAlchemyAutoSchema):
    
    subscriptions = ma.Nested(MagazineSchema, many=True)

    class Meta:
        model = models.User
        include_fk = True

users_schema = UserSchema(many=True)
user_schema = UserSchema()
#Schemas to view a user without the subscriptions list
user_no_subscriptions_schema = UserSchema(exclude=['subscriptions'])
users_no_subscriptions_schema = UserSchema(exclude=['subscriptions'], many=True)