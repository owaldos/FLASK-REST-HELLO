from flask_sqlalchemy import SQLAlchemy
from requests.api import delete

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user',uselist=True)
    
    def serialize(self):
        return{
            'id':self.id,
            'username':self.username,
            
            'favorites':[favorite.serialize() for favorite in self.favorites]
        }

    @classmethod
    def create(cls,data_new_user):
        new_user= cls(**data_new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
            return({"message":"done"})
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

  

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url= db.Column(db.String(120),nullable= False)
    name_favorite= db.Column(db.String(30),nullable= False)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    __table_args__=(db.UniqueConstraint(
        'user_id',
        'url',
        name='unique_fav_for_user'
        
    ),)

    def serialize(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'name_favorite': self.name_favorite,
            'url':self.url,
        }
    
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback
            return None

    @classmethod
    def create(cls,data_favorite):
        new_favorite= cls(**data_favorite)
        try:
            db.session.add(new_favorite)
            db.session.commit()
            return(new_favorite.serialize())
        except Exception as error:
            db.session.rollback()
            print(error)
            return None
        