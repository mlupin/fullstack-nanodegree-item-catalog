from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.category import Category
from models.recipe import Recipe
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
@app.route('/recipes/')
def showCategories():
    return render_template('categories.html')


# Create a new category
@app.route('/recipes/new/')
def newCategory():
    return render_template('newCategory.html')


# Edit a category
@app.route('/recipes/<int:category_id>/edit/')
def editCategory():
    return render_template('editCategory.html')


# Delete a category
@app.route('/recipes/<int:category_id>/delete/')
def deleteCategory():
    return render_template('deleteCategory.html')


# Show recipes in a category
@app.route('/recipes/<int:category_id>')
def showCatalog():
    return render_template('recipes.html')


# Show a recipe
@app.route('/recipes/<int:recipe_id>/')
def showCatalogItem():
    return render_template('recipe.html')


# Create a new recipe
@app.route('/recipes/new/')
def newCatalogItem():
    return render_template('newRecipe.html')


# Edit a recipe
@app.route('/recipes/<int:category_id>/<int:recipe_id>/edit/')
def editCatalogItem():
    return render_template('editRecipe.html')


# Delete a recipe
@app.route('/recipes/<int:category_id>/<int:recipe_id>/delete/')
def deleteCatalogItem():
    return render_template('deleteRecipe.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
