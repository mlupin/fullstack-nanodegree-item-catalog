from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.category import Category


engine = create_engine('sqlite:///recipes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.create_all(engine)

dbSession = sessionmaker(bind=engine)
session = dbSession()

categories = ['Wraps & Burgers',
              'Sides & Salads',
              'Soups & Stews',
              'Pasta & Noodles',
              'Amazing Grains',
              'Breakfast',
              'Condiments & Sauces',
              'Decadent Desserts']


def addCategories():
    for category in categories:
        session.add(Category(name=category))
    session.commit()


if __name__ == '__main__':
    addCategories()
