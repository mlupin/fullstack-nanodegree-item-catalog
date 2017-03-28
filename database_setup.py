from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
# from models.base import Base
# from models.category import Category
from models.models import Base, User, Category, Recipe

engine = create_engine('sqlite:///recipes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.create_all(engine)

dbSession = sessionmaker(bind=engine)
session = dbSession()

# Create dummy user
user1 = User(name="Marina Lupin",
             email="lupinmarina@gmail.com",
             image='https://pbs.twimg.com/profile_images/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.png')

user2 = User(name="Archer",
             email="archer@example.com",
             image='https://pbs.twimg.com/profile_images/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.png')

users = [user1, user2]

category1 = Category(name="Wraps & Burgers")
category2 = Category(name="Sides & Salads")
category3 = Category(name="Soups & Stews")
category4 = Category(name="Pasta & Noodles")
category5 = Category(name="Amazing Grains")
category6 = Category(name="Breakfast")
category7 = Category(name="Condiments & Sauces")
category8 = Category(name="Decadent Desserts")

categories = [category1, category2, category3, category4,
              category5, category6, category7, category8]

# Wraps & Burgers recipes
recipe1 = Recipe(user_id=1,
                 name="Veggie Burger",
                 description="Juicy grilled veggie patty with tomato mayo and lettuce",
                 image="http://lorempixel.com/200/200/food",
                 category=category1)

recipe2 = Recipe(user_id=1,
                 name="Veggie Wrap",
                 description="Juicy grilled tofu with guac and lettuce",
                 image="http://lorempixel.com/200/200/food",
                 category=category1)

# Breakfast recipes
recipe3 = Recipe(user_id=1,
                 name="Chia Seed Pudding",
                 description="Pudding made with almond milk, chia seeds, cardamom, and blueberries",
                 image="http://lorempixel.com/200/200/food",
                 category=category6)


recipe4 = Recipe(user_id=1,
                 name="Chocolate Banana Smoothie",
                 description="Banana blended with flax seeds and cocao powder",
                 image="http://lorempixel.com/200/200/food",
                 category=category6)

recipe5 = Recipe(user_id=1,
                 name="Avocado Lime Tart",
                 description="Raw vegan avocado key lime pie with a nut and date crust",
                 image="http://lorempixel.com/200/200/food",
                 category=category8)


recipes = [recipe1, recipe2, recipe3, recipe4, recipe5]


def addUsers():
    for user in users:
        session.add(user)
    session.commit()

def addCategories():
    for category in categories:
        session.add(category)
    session.commit()

def addRecipes():
    for recipe in recipes:
        session.add(recipe)
    session.commit()


if __name__ == '__main__':
    addUsers()
    addCategories()
    addRecipes()
