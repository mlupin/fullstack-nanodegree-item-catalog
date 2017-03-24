from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.category import Category
from models.recipe import Recipe

engine = create_engine('sqlite:///recipes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista",
             email="tinnyTim@udacity.com",
             image='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Wraps & Burgers recipes
category1 = Category(user_id=1, name="Wraps & Burgers")

session.add(category1)
session.commit()

recipe1 = Recipe(user_id=1,
                 name="Veggie Burger",
                 description="Juicy grilled veggie patty with tomato mayo and lettuce",
                 image="http://lorempixel.com/200/200/food",
                 category=category1)
session.add(recipe1)
session.commit()

recipe2 = Recipe(user_id=1,
                 name="Veggie Wrap",
                 description="Juicy grilled tofu with guac and lettuce",
                 image="http://lorempixel.com/200/200/food",
                 category=category1)

session.add(recipe2)
session.commit()

# Breakfast recipes
category2 = Category(user_id=1, name="Breakfast")

session.add(category1)
session.commit()

recipe1 = Recipe(user_id=1,
                 name="Chia Seed Pudding",
                 description="Pudding made with almond milk, chia seeds, cardamom, and blueberries",
                 image="http://lorempixel.com/200/200/food",
                 category=category2)
session.add(recipe1)
session.commit()

recipe2 = Recipe(user_id=1,
                 name="Chocolate Banana Smoothie",
                 description="Banana blended with flax seeds and cocao powder",
                 image="http://lorempixel.com/200/200/food",
                 category=category2)

session.add(recipe2)
session.commit()


print "added menu items!"