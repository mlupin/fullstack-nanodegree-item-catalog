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
             picture='https://pbs.twimg.com/profile_imageURLs/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.jpg')

user2 = User(name="Archer",
             email="archer@example.com",
             picture='https://pbs.twimg.com/profile_imageURLs/2671170543'
                   '/18debd694829ed78203a5a36dd364160_400x400.jpg')

users = [user1, user2]

category1 = Category(name="breakfast",
                     picture="/static/images/chia-seed-pudding-small.jpg")
category2 = Category(name="entrees",
                     picture="/static/images/burger-small.jpg")
category3 = Category(name="sides",
                     picture="/static/images/brussels-sprouts-small.jpg")
category4 = Category(name="snacks",
                     picture="/static/images/toast-small.jpg")
category5 = Category(name="sweets",
                     picture="/static/images/cheesecake-small.jpg")
category6 = Category(name="beverages",
                     picture="/static/images/smoothie-small.jpg")


categories = [category1, category2, category3, category4,
              category5, category6]
# Breakfast
recipe1 = Recipe(user_id=1,
                 name="Chia Seed Pudding",
                 description="Pudding made with almond milk, chia seeds, cardamom, and blueberries. "
                             "Healthy and filling breakfast to start your day with plenty of fiber.",
                 servings=4,
                 ingredients="- 2 cups almond milk (homemade or natural)\n"
                             "- 1/2 cup Chia Seeds\n"
                             "- 1 tsp honey (optional)\n"
                             "- 1/2 tsp cardamon\n"
                             "- 1 cup kiwi (optional)\n"
                             "- 1 cup strawberries (optional)\n",
                 instructions="1. Blend milk, honey, and cardamom in a blender or with a spoon (including any added flavors, fruits or chocolate).\n"
                              "2. Whisk in chia seeds.\n"
                              "3. Pour mixture into a jar or glass container and place in the refrigerator for at least 4 hours or overnight.",
                 category=category1)

recipe2 = Recipe(user_id=1,
                 name="Oatmeal",
                 description="Easy oatmeal that is great for those in a hurry.",
                 servings=1,
                 ingredients="- 1 cup almond milk (homemade or natural)\n"
                             "- 3 Tbsp oats\n"
                             "- 1 banana\n"
                             "- 1/2 cup blueberries\n"
                             "- 1 Tbsp chia seeds\n"
                             "- 1/4 tsp cinnamon (optional)\n"
                             "- 1 tsp honey or agave syrup (optional)",
                 instructions="1. Pour the milk in a saucepan and bring it to boil.\n"
                              "2. Add the oats, cover the saucepan and cook over medium heat for about 10 or 15 minutes.\n"
                              "3. Place the oats in a bowl and add the rest of the ingredients.",
                 category=category1)

recipe3 = Recipe(user_id=1,
                 name="Berry Acai Bowl",
                 description="Easy oatmeal that is great for those in a hurry.",
                 servings=1,
                 ingredients="Smoothie:\n"
                             "- 2/3 cup fresh or frozen blueberries or blackberries\n"
                             "- 2/3 cup fresh or frozen strawberries or strawberries\n"
                             "- 1/2 banana\n"
                             "- 3/4-1 cup almond milk (homemade or natural)\n"
                             "- 1-3 tsp acai bowder\n"
                             "Toppings (optional):\n"
                             "- 1/2 banana, sliced\n"
                             "- fresh or dried berries\n"
                             "- granola or crushed nuts",
                 instructions="1. Pour the milk in a saucepan and bring it to boil.\n"
                              "2. Add the oats, cover the saucepan and cook over medium heat for about 10 or 15 minutes.\n"
                              "3. Place the oats in a bowl and add the rest of the ingredients.",
                 category=category1)

# Entrees
recipe4 = Recipe(user_id=1,
                 name="Stuffed Bell Peppers",
                 description="Favorite Russian family recipe.",
                 servings=6,
                 ingredients="Stuffing:\n"
                             "- 1 lb (500 g) ground meat (lamb, beef, pork or their mixture, coarse-ground is better than fine-ground)\n"
                             "- 1/4 - 1/2 large finely chopped onion, white or yellow\n"
                             "- 1 tsp salt\n"
                             "- 1/2 tsp black ground pepper\n"
                             "- 1 egg\n"
                             "- 1/4 cup white round rice (medium grain)\n"
                             "- 1-2 tbsp parsley, dill or cilantro finely chopped (optional)\n"
                             "Other Ingredients:\n"
                             "- 6 large meaty bell peppers\n"
                             "- 2 tbsp olive or any other oil\n"
                             "- 6 tbsp sour cream (optional)\n"
                             "- Parsley, dill or cilantro (optional)\n"
                             "- 2 large or 4 medium size carrots, cut in round, squared, or long thin pieces\n"
                             "- 1/2 large white or yellow onion chopped or 1 white chunk of leeks cut in round pieces\n"
                             "- 100-500 g fresh tomatoes (optional)\n"
                             "- Celery (optional), cut in large pieces or chopped\n"
                             "- 1/2 - 1 large bell pepper (optional), chopped or shred\n"
                             "- Mushrooms dry or fresh (optional)\n",
                 instructions="1. In the casserole or a large enough pot to accommodate 6 peppers standing in one row on the bottom of the pot, preheat the oil.\n"
                              "2. Saute (on high/medium heat) carrots, onion (or leeks), and other optional vegetables: celery, mushrooms, pepper, tomatoes.\n"
                              "3. Add in the saut2 1/4 tsp salt, black pepper and other dry or fresh herbs.\n"
                              "4. Mix all ingredients for the stuffing and put the stuffing inside bell peppers.\n"
                              "5. Place stuffed peppers in the casserole above sauteed vegetable, season generously with fresh herbs.\n"
                              "6. Pour a table spoon of sour cream on the top of each pepper (optional).\n"
                              "7. Put the lead on the casserole, make the heat on medium, and cook for an hour.\n"
                              "8. If in an hour the peppers are still too firm, cook for another 20-30 minutes.",
                 category=category2
                 )

recipe5 = Recipe(user_id=1,
                 name="Thai Salad",
                 description="Thai-inspired carrot and cucumber salad with a savory-sweet dressing and cashews.",
                 servings=4,
                 ingredients="Dressing:\n"
                             "- 2 cloves garlix, minced\n"
                             "- 2 Tbsp raw or roasted peanuts\n"
                             "- 1 fresh or dried thai chili (option to substitute with 1 tsp red pepper flake)\n"
                             "- 1 Tbsp coconut sugar (or agave, honey, maple syrup)\n"
                             "- 1/4 cup lime juice\n"
                             "- 1 Tbsp tamari or soy sauce\n"
                             "Salad:\n"
                             "- 1/2 cup cashews\n"
                             "- 1/2 cup peanuts\n"
                             "- 2 tsp sesame oil\n"
                             "- 1/4 cup thinly sliced red onion\n"
                             "- 4 cups finely shredded/grated carrot\n"
                             "- 2-3 cups finely shredded/grated cucumber\n"
                             "- 1 cup green beans, blanched\n"
                             "- 1/2 cup chopped fresh cilantro",
                 instructions="1. Add garlic, nuts and chili to a food processor or a mortar and pestle to make a paste.\n"
                              "2. Add sweetener to taste and mix.\n"
                              "3. Add lime juice and tamari (or soy sauce) and stir to combine.\n"
                              "4. Add onion, cucumber, carrots, green beans, sesame oil, and lime juice to a large mixing bowl. Mix well.\n"
                              "5. Add nuts, cilantro, and dressing. Toss to coat.\n"
                              "3. Serve immediately.",
                 category=category2)


recipe6 = Recipe(user_id=1,
                 name="Miso Soup",
                 description="Simple vegan miso soup with mushrooms and tofu.",
                 servings=3,
                 ingredients="- 40 g soba noodles\n"
                             "- 3 Tbsp miso paste\n"
                             "- 4 cups water\n"
                             "- 1/2 cup thinly sliced green onion\n"
                             "- 100 g soft tofu\n"
                             "- wakame seaweed (optional)\n"
                             "- 100 g fresh mushrooms\n",
                 instructions="1. Cook noodles according to package directions.\n"
                              "2. Heat water in a pot and when it starts to boil, add the dried wakame seaweed and mushrooms. Cook over medium heat for 5 minutes.\n"
                              "3. Place the miso paste into a small bowl, add hot water and whisk until smooth. \n"
                              "4. Add miso mixture to the soup after removing the pot from the heat and stir.\n"
                              "5. Add the tofu and the green onion and stir again.\n"
                              "3. Serve immediately or continue to cook for another 5 minutes.",
                 category=category2)


# Sides
recipe7 = Recipe(user_id=1,
                 name="Roasted Brussel Sprouts",
                 description="Roasted brussel sprouts cut in half and coated in balsamic vinegar.",
                 servings=6,
                 ingredients="- 1 1/2 pounds Brussels sprouts, ends trimmed and yellow leaves removed\n"
                             "- 2-3 Tbsp olive oil\n"
                             "- 1 tsp salt\n"
                             "- 1/2 tsp freshly ground black pepper\n"
                             "- 1 Tbsp balsamic vinegar",
                 instructions="1. Preheat the oven to 400F.\n"
                              "2. Mix brussel sprouts, olive oil, salt, and pepper and place on a baking sheet.\n"
                              "3. Roast the Brussels sprouts for 20 to 30 minutes.\n"
                              "4. Toss once during roasting. Remove from the oven, drizzle with the balsamic vinegar.\n"
                              "5. Serve hot and enjoy!",
                 category=category3)

recipe8 = Recipe(user_id=1,
                 name="Sweet Potato Fries",
                 description="Healthy option to replace your favorite french fries. "
                             "Great side to serve with fish, veggies, or have as a snack.",
                 servings=6,
                 ingredients="- 1 medium size sweet potato\n"
                             "- 2-3 Tbsp olive oil\n"
                             "- 1 tsp salt\n"
                             "- 1 tsp fresh ground black pepper\n"
                             "- 1-2 tsp cumin, paprika, cayenne, or curry, mix and match (optional)",
                 instructions="1. Preheat the oven to 425F.\n"
                              "2. Peel the sweet potatoes and cut them into fry-shaped pieces.\n"
                              "3. Toss the uncooked fries onto your baking sheet, pour in a few tablespoons of olive oil.\n"
                              "4. Season with salt, pepper, and spices.\n"
                              "4. Arrange your fries in a single layer and don't overcrowd.\n"
                              "5. Bake for 15 minutes, then flip the fries.\n"
                              "6. Bake for 10 to 15 more minutes, or until the fries are crispy.\n"
                              "7. Serve hot with your favorite dipping sauce or as a side.",
                 category=category3)

recipe9 = Recipe(user_id=1,
                 name="Hummus",
                 description="Roasted brussel sprouts cut in half and coated in balsamic vinegar.",
                 servings=8,
                 ingredients="- 1 15-ounce can chickpeas, NOT drained (option to cook chickpeas)\n"
                             "- 2-4 cloves garlic\n"
                             "- 1-2 Tbsp extra virgin olive oil\n"
                             "- 1/2 cup tahini\n"
                             "- 3/4-1 tsp sea salt\n"
                             "- 2 Tbsp fresh lemon juice",
                 instructions="1. Add to blender or food processor and process all ingredients, except olive oil until smooth.\n"
                              "2. Add olive oil and mix slowly.\n"
                              "3. Garnish with a little more olive oil, paprika, and sesame seeds.",
                 category=category3)

# Snacks
recipe10 = Recipe(user_id=1,
                 name="Hummus Avocado Toast",
                 description="Simple vegan hummus-avocado toast perfect for breakfast or lunch or a snack. "
                             "Multigrain toast topped with heart-healthy fats and plant proteins.",
                 servings=1,
                 ingredients="- 2 slices sprouted grain bread, toasted\n"
                             "- 2 tbsp hummus\n"
                             "- 6 thin cucumber slices\n"
                             "- 1 small radish, sliced thin\n"
                             "- 1 oz avocado, sliced thin (about 1/4 small haas)\n"
                             "- crushed red pepper flakes, to taste\n"
                             "- 1/4 cup baby arugula or baby spinach\n"
                             "- 1/8 tsp kosher salt",
                 instructions="1. Spread one toast with hummus and the other with avocado.\n"
                              "2. Top each slice with cucumber and radish, sprinkle with red pepper flakes and salt.\n"
                              "3. Finally top each slice with greens.\n"
                              "4. Option to spread the toast with hummus and top with avocado.",
                 category=category4)

recipe11 = Recipe(user_id=1,
                 name="Muesli Bar",
                 description="Healthy, no bake granola bars with a sweet and crunchy texture.",
                 servings=12,
                 ingredients="- 220 g medjool dates, pitted\n"
                             "- 1/4 cup maple syrup, agave nectar, or honey if not vegan\n"
                             "- 1/4 cup creamy unsalted natural almond, cashew, or peanut butter\n"
                             "- 1/4 cup unsalted almonds, loosely chopped\n"
                             "- 1/4 cup unsalted walnuts, loosely chopped\n"
                             "- 1/4 cup unsalted pumpkin seeds\n"
                             "- 1/4 cup unsalted sunflower seeds\n"
                             "- 1 1/2 cups (135 g) rolled oats",
                 instructions="1. Process dates in a food processor to form a dough like consistency.\n"
                              "2. Place oats, nuts, seeds, and dates in a large mixing bowl - set aside.\n"
                              "3. Warm honey and nut butter in a saucepan over low heat.\n"
                              "4. Stir and pour over oat and nut mixture and then mix.\n"
                              "5. Transfer to a baking dish or other small pan lined with parchment paper.\n"
                              "6. Press down firmly until uniformly flattened.\n"
                              "7. Cover with plastic wrap, and let firm up in fridge or freezer for 15-20 minutes.\n"
                              "8. Remove bars and chop into 12 even bars. Store in an airtight container.",
                 category=category4)

recipe12 = Recipe(user_id=1,
                 name="Juice Pulp Muffins",
                 description="Time to reuse your juicer pulp and enjoy there incredibly moist and high in fiber muffins. Perfect as a to-go snacks!",
                 servings=24,
                 ingredients="- 1 banana, mashed\n"
                             "- 2 cups veggie or fruit pulp\n"
                             "- 4 Tbsp honey\n"
                             "- 3 cups almond meal\n"
                             "- 1 Tbsp baking powder\n"
                             "- 1/4 cup flaxseed meal\n"
                             "- 1/2 tsp salt\n"
                             "- 3/4 cup almond milk\n"
                             "- 1 tsp vanilla extract\n"
                             "- 1 tsp nutmeg\n"
                             "- 2 tsp cinnamon\n",
                 instructions="1. Preheat oven to 350F.\n"
                              "2. In a large bowl, combine the almond meal, flaxseed meal, salt, baking powder, cinnamon and nutmeg.\n"
                              "3. Add the pulp followed by the banana, almond milk, honey and vanilla extract. Mix until just combined.\n"
                              "4. Add batter to muffin tins. Bake for 20 to 25 minutes.",
                 category=category4)



# Sweets
recipe13 = Recipe(user_id=1,
                 name="Gingerbread",
                 description="This is my mum's recipe and she often made this gingerbread for Christmas. "
                             "Classic gingerbread with fresh ginger, apples, and brown sugar. Perfect dessert to share with loved ones during fall holidays.",
                 servings=15,
                 ingredients="- 2/3 cup (160 g) whole milk\n"
                            "- 3/4 cup (160 g) dark brown sugar\n"
                            "- 2 tbsp molasses\n"
                            "- 2/3 cup (170 g) unsalted butter\n"
                            "- 1 egg\n"
                            "- 1 5/8 cup (200 g) all purpose flour\n"
                            "- 30-50 g fresh ginger root peeled\n"
                            "- 2 tbsp baking powder\n"
                            "- 1 large apple peeled, chopped and coated with 1 tbsp lemon juice",
                 instructions="1. Preheat the oven to 400F/200C.\n"
                              "2. In a small saucepan, over low heat, melt the butter, sugar and molasses.\n"
                              "3. Grate the ginger finely in a large bowl. Add in the bowl flour, baking powder, the milk and egg. Stir well.\n"
                              "4. Add buttery mixture, stir.\n"
                              "5. Add apples, stir.\n"
                              "6. Grease the baking dish with butter. Pour the mixture in the dish.\n"
                              "7. Bake 35-45 minutes or until brown on the top and done (check with a knife inserted in the center).\n"
                              "8. Serve hot, warm or cold with whipped cream (1 cup of heavy whipped cream whipped with 1/4 cup sugar).",
                 category=category5
                 )

recipe14 = Recipe(user_id=1,
                 name="Clafoutis",
                 description="A traditional French dessert. This clafoutis is moderately sweet despite very sweet cherries and sweetened coconut.",
                 servings=15,
                 ingredients="- 1/2 cup (120 g) whole milk\n"
                             "- 1/2 cup (120 g) heavy cream\n"
                             "- 1/4 cup (50 g) sugar\n"
                             "- a pinch of salt\n"
                             "- 1 vanilla pod (or 1/4 tsp vanilla extract)\n"
                             "- 3 eggs\n"
                             "- 2/3 cup (85 g) all purpose flour\n"
                             "- 1 lb (500 g) large sweet cherries, unpitted\n"
                             "- 50 g unsweetened or sweetened coconut",
                 instructions="1. Preheat the oven to 350F/180C.\n"
                              "2. Place the cherries into the baking dish.\n"
                              "3. In a medium saucepan, heat slightly the cream, salt, and vanilla pod splited in two. Remove from the heat, add milk, and remove vanilla pod.\n"
                              "4. In a large bowl, whisk the eggs with sugar, using the electrical mixer. Add flour and continue mixing with the mixer. Then add the cream and coconuts, mixing constantly.\n"
                              "5. Pour the warm custard over the cherries. Bake for about 35-40 minutes, or until golden on top.\n"
                              "6. Serve warm with whipped heavy cream. Remember about the cherries pits!\n",
                 category=category5
                 )


recipe15 = Recipe(user_id=1,
                 name="Chocolate Chip Cookies",
                 description="Play on traditional chocolate chip cookies but with almond meal. Crispy on the outside, chewy on the inside!",
                 servings=12,
                 ingredients="- 1 1/4 cups almond meal\n"
                             "- 1/4 cup dark chocolate chips or bar, loosely chopped\n"
                             "- 1/2 cup shreddedunsweetened coconut\n"
                             "- 1/2 tsp baking powder\n"
                             "- 1/4 tsp sea salt\n"
                             "- 1/3 cup honey\n"
                             "- 1/4 cup water\n"
                             "- 3 Tbsp  coconut oil, melted\n"
                             "- 1/2 tsp vanilla extract\n",
                 instructions="1. In a large mixing bowl, stir together almond meal, dark chocolate chips, coconut, baking powder, salt, and sugar.\n"
                              "2. Add melted coconut oil and vanilla to dry ingredients and mix.\n"
                              "3. Loosely cover and chill in the refrigerator for at least 30 minutes or overnight.\n"
                              "4. Preheat the oven to 375F/190C.\n"
                              "5. Make and place each cookie on a bare or parchment-lined baking sheet with a 1-inch gap in between each cookie to allow for spreading.\n"
                              "6. Bake for 12-15 minutes or until the edges are golden brown.\n"
                              "7. Serve immediately or let cool.",
                 category=category5
                 )

# Beverages
recipe16 = Recipe(user_id=1,
                 name="Chocolate Banana Smoothie",
                 description="Power charge your day with this velvety smooth smoothie.",
                 servings=1,
                 ingredients="- 1 banana\n"
                             "- 1 Tbsp cocoa powder\n"
                             "- 4 ice cubes (if bananas were not frozen\n"
                             "- 3/4 cup almond milk (homemade or natural)\n",
                 instructions="1. Blend all ingredients until smooth.\n",
                 category=category6)

recipe17 = Recipe(user_id=1,
                 name="Matcha Latte",
                 description="Enjoy this creamy matcha tea drink for an antioxidant and energy boost.",
                 servings=1,
                 ingredients="- 3/4 cup almond milk (homemade or natural)\n"
                             "- 1/4 cup boiling water\n"
                             "- 1 tsp matcha powder\n"
                             "- honey or agave (optional)",
                 instructions="1. Bring almond milk to a simmer in a small pot over medium-high heat.\n"
                              "2. Place matcha powder in a heatproof cup. Slowly whisk in boiling water.\n"
                              "3. Slowly combine with almond milk, tipping cup slightly to create more foam.\n"
                              "4. Sweeten with honey or agave syrup (optional).",
                 category=category6)

recipe18 = Recipe(user_id=1,
                 name="Beet and Carrot Juice",
                 description="Enjoy this creamy matcha tea drink for an antioxidant and energy boost.",
                 servings=1,
                 ingredients="- 1 medium beet, peeled and chopped\n"
                             "- 2 carrots, peeled and chopped\n"
                             "- 1/4 inch piece of ginger root\n"
                             "- 1/2 lemon\n"
                             "- 1/2 cup water",
                 instructions="1. Blend all ingredients in a blender until smooth.\n"
                              "2. Use a fine mesh sieve or a cheesecloth to strain the juice.\n"
                              "3. Serve the juice.\n"
                              "4. Tip: do not discard the pulp. Use to make zucchini bread, add to soups, salads, etc.",
                 category=category6)


recipes = [recipe1, recipe2, recipe3, recipe4, recipe5, recipe6,
           recipe7, recipe8, recipe9, recipe10, recipe11, recipe12,
           recipe13, recipe14, recipe15, recipe16, recipe17, recipe18]


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
