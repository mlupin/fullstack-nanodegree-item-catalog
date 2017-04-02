from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
        }


class Recipe(Base):
    __tablename__ = 'recipe'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    picture = Column(String(250))
    servings = Column(String())
    instructions = Column(String())
    ingredients = Column(String())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    created = Column(DateTime())
    modified = Column(DateTime())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'servings': self.servings,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'id': self.id,
        }


engine = create_engine('sqlite:///recipes.db')

Base.metadata.create_all(engine)
