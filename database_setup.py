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
             picture='https://pbs.twimg.com/profile_pictures/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.png')

user2 = User(name="Archer",
             email="archer@example.com",
             picture='https://pbs.twimg.com/profile_pictures/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.png')

users = [user1, user2]

category1 = Category(name="breakfast")
category2 = Category(name="entrees")
category3 = Category(name="sides")
category4 = Category(name="snacks")
category5 = Category(name="sweets")
category6 = Category(name="beverages")


categories = [category1, category2, category3, category4,
              category5, category6]

recipe1 = Recipe(user_id=1,
                 name="Veggie Burger",
                 description="Juicy grilled veggie patty with tomato mayo and lettuce",
                 picture="http://lorempixel.com/100/100/food",
                 servings=3,
                 ingredients="- 1 cup black beans\n- 1/4tsp pink salt",
                 instructions="1. Soak black beans.\n2. Add black beans to hot water.",
                 category=category2)

recipe2 = Recipe(user_id=2,
                 name="Veggie Wrap",
                 description="Juicy grilled tofu with guac and lettuce",
                 picture="http://lorempixel.com/100/100/food",
                 servings=2,
                 ingredients="- 1 tofu\n- 1/4tsp pink salt",
                 instructions="1. Drain salt.\n2. Cook tofu.",
                 category=category2)

recipe3 = Recipe(user_id=1,
                 name="Chia Seed Pudding",
                 description="Pudding made with almond milk, chia seeds, cardamom, and blueberries",
                 picture="http://lorempixel.com/100/100/food",
                 servings=1,
                 ingredients="- ingredient one \n- ingredient two",
                 instructions="1. Step1.\n2. Step2.",
                 category=category1)


recipe4 = Recipe(user_id=2,
                 name="Chocolate Banana Smoothie",
                 description="Banana blended with flax seeds and cocao powder",
                 picture="http://lorempixel.com/100/100/food",
                 servings=1,
                 ingredients="- ingredient one \n- ingredient two",
                 instructions="1. Step1.\n2. Step2.",
                 category=category6)

recipe5 = Recipe(user_id=2,
                 name="Avocado Lime Tart",
                 description="Raw vegan avocado key lime pie with a nut and date crust",
                 picture="http://lorempixel.com/100/100/food",
                 servings=1,
                 ingredients="- ingredient one \n- ingredient two",
                 instructions="1. Step1.\n2. Step2.",
                 category=category5)

recipe6 = Recipe(user_id=2,
                 name="Roasted Brussel Sprouts",
                 description="Roasted brussel sprouts cut in half and coated in balsamic vinegar",
                 picture="http://lorempixel.com/100/100/food",
                 servings=1,
                 ingredients="- ingredient one \n- ingredient two",
                 instructions="1. Step1.\n 2. Step2.",
                 category=category3)


recipes = [recipe1, recipe2, recipe3, recipe4, recipe5, recipe6]


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
