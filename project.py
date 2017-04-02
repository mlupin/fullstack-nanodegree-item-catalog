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
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Recipe App"


# Connect to Database and create database session
engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
#JSON APIs to view Restaurant Information
@app.route('/categories/<int:category_id>/recipes/JSON')
def categoryRecipesJSON(category_id):
    recipes = session.query(Recipe).filter_by(category_id=category_id).order_by(asc(Recipe.name))
    return jsonify(recipes=[r.serialize for r in recipes])


@app.route('/recipes/<int:recipe_id>/JSON')
def recipeJSON(recipe_id):
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    return jsonify(recipe=recipe.serialize)

@app.route('/recipes/JSON')
def recipesJSON():
    recipes = session.query(Recipe).order_by(asc(Recipe.name))
    return jsonify(recipes=[r.serialize for r in recipes])

@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# Show all recipes
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


# Show all recipes
@app.route('/recipes/')
def showAllRecipes():
    recipes = session.query(Recipe).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


# Show recipes in a category
@app.route('/categories/<int:category_id>/recipes')
def showRecipes(category_id):
    recipes = session.query(Recipe).filter_by(category_id=category_id).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


# Show a recipe
@app.route('/recipes/<int:recipe_id>/')
def showRecipe(recipe_id):
    recipeToShow = session.query(Recipe).filter_by(id=recipe_id).one()
    return render_template('recipe.html', recipe=recipeToShow)


# Create a new recipe
@app.route('/recipe/new/', methods=['GET', 'POST'])
def newRecipe():
    if 'username' not in login_session:
        return redirect('/login')
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
@app.route('/recipes/<int:recipe_id>/edit/', methods=['GET','POST'])
def editRecipe(recipe_id):
    recipeToEdit = session.query(Recipe).filter_by(id=recipe_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if recipeToEdit.user_id != login_session['user_id']:
        flash('You are not authorized to edit %s recipe' % recipeToEdit.name)
        return redirect(url_for('showAllRecipes'))
    if request.method == 'POST':
        if request.form['name'] != "" and request.form['description'] != "" and request.form['category'] != "":
            if request.form['name']:
                recipeToEdit.name = request.form['name']
            if request.form['description']:
                recipeToEdit.description = request.form['description']
            if request.form['ingredients']:
                recipeToEdit.ingredients = request.form['ingredients']
            if request.form['instructions']:
                recipeToEdit.instructions = request.form['instructions']
            if request.form['category']:
                recipeToEdit.category_id = request.form['category']
            session.add(recipeToEdit)
            session.commit()
            flash('Recipe %s Successfully Edited' % recipeToEdit.name)
            return redirect(url_for('showAllRecipes'))
        else:
            flash('Name and Description cannot be blank')
            return render_template('editRecipe.html', recipe=recipeToEdit)
    else:
        return render_template('editRecipe.html', recipe=recipeToEdit)


# Delete a recipe
@app.route('/recipes/<int:recipe_id>/delete/', methods=['GET','POST'])
def deleteRecipe(recipe_id):
    recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if recipeToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete %s recipe' % recipeToDelete.name)
        return redirect(url_for('showAllRecipes'))
    if request.method == 'POST':
        session.delete(recipeToDelete)
        session.commit()
        flash('Recipe Successfully Deleted')
        return redirect(url_for('showAllRecipes'))
    else:
        return render_template('deleteRecipe.html', recipe=recipeToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
