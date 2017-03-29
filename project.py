from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
# from models.base import Base
# from models.user import User
# from models.category import Category
# from models.recipe import Recipe
from models.models import Base, User, Category, Recipe
from flask import session as login_session
import random
import string
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    return render_template('login.html')


# Show all recipes
@app.route('/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


# # Create a new category
# @app.route('/recipes/new/', methods=['GET','POST'])
# def newCategory():
#     if request.method == 'POST':
#         newCategory = Category(name=request.form['name'])
#         flash('New Category %s Successfully Created' % newCategory.name)
#         session.commit()
#         return redirect(url_for('showCategories'))
#     else:
#         return render_template('newCategory.html')


# # Edit a category
# @app.route('/recipes/<int:category_id>/edit/')
# def editCategory():
#     return render_template('editCategory.html')


# # Delete a category
# @app.route('/recipes/<int:category_id>/delete/')
# def deleteCategory():
#     return render_template('deleteCategory.html')


# Show all recipes
@app.route('/recipes/')
def showAllRecipes():
    recipes = session.query(Recipe).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


# Show recipes in a category
@app.route('/recipes/<int:category_id>')
def showRecipes():
    return render_template('recipes.html')


# Show a recipe
@app.route('/recipes/<int:recipe_id>/<string:recipe_name>')
def showRecipe():
    return render_template('recipe.html')


# Create a new recipe
@app.route('/recipe/new/', methods=['GET', 'POST'])
def newRecipe():
    if request.method == 'POST':
        if request.form['name'] != "" and request.form['description'] != "" and request.form['category'] != "":
            createNewRecipe = Recipe(name=request.form['name'],
                                     description=request.form['description'],
                                     category_id=request.form['category']
                                     )
            session.add(createNewRecipe)
            session.commit()
            flash('New Recipe %s Successfully Created' % (createNewRecipe.name))
            return redirect(url_for('showAllRecipes'))
        else: 
            flash('Error')
            return render_template('newRecipe.html')
    else:
        return render_template('newRecipe.html')


# Edit a recipe
@app.route('/recipes/<int:category_id>/<int:recipe_id>/<string:recipe_name>/edit/')
def editRecipe():
    return render_template('editRecipe.html')


# Delete a recipe
@app.route('/recipes/<int:recipe_id>/delete/', methods=['GET','POST'])
def deleteRecipe(recipe_id):
    if request.method == 'POST':
        recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
        session.delete(recipeToDelete)
        session.commit()
        flash('Recipe Successfully Deleted')
        return redirect(url_for('showAllRecipes'))
    else:
        return redirect(url_for('showAllRecipes'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
