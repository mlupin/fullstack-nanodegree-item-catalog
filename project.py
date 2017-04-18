import os

from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import session as login_session
from flask import make_response, send_from_directory, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, Category, Recipe

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from werkzeug import secure_filename

import requests
import random
import string
import httplib2
import json


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Recipe App"
UPLOAD_FOLDER = "/static/images/uploads/"

# limit the size of the content to ~ 5 MB (for the picture upload)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Connect to Database and create database session
engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']


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
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
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
    output += ' " style = "width: 300px; height: 300px;'
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
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


# JSON APIs to view Restaurant Information
@app.route('/categories/<int:category_id>/recipes/JSON')
def categoryRecipesJSON(category_id):
    recipes = session.query(Recipe).filter_by(
              category_id=category_id).order_by(asc(Recipe.name))
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


@app.route('/')
@app.route('/categories/')
def showCategories():
    """ Show home page and list of categories """
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


@app.route('/recipes/')
def showAllRecipes():
    """ Show all recipes """
    recipes = session.query(Recipe).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


@app.route('/categories/<int:category_id>/recipes')
def showRecipes(category_id):
    """ Show recipes in a category """
    recipes = session.query(Recipe).filter_by(
              category_id=category_id).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/<int:user_id>')
def showUsersRecipes(user_id):
    """ Show recipes in a category """
    recipes = session.query(Recipe).filter_by(
              user_id=user_id).order_by(asc(Recipe.name))
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/<int:recipe_id>/')
def showRecipe(recipe_id):
    """ Show a recipe """
    recipeToShow = session.query(Recipe).filter_by(id=recipe_id).one()
    return render_template('recipe.html', recipe=recipeToShow)


@app.route('/recipes/<int:recipe_id>/picture/')
def recipePicture(recipe_id):
    """ Show recipe picture """
    recipe = session.query(Recipe).get(recipe_id)

    file_extension = recipe.picture.rsplit('.', 1)[1].lower()

    if file_extension == "jpg" or file_extension == "jpeg":
        content_type = "image/jpeg"
    else:
        content_type = "image/png"

    return recipe.picture_data, 200, {'Content-Type': content_type,
                                      'Content-Disposition':
                                      "filename='%s'" % recipe.picture}


@app.route('/recipe/new/', methods=['GET', 'POST'])
# @login_required
def createRecipe():
    """ Create a new recipe """
    categories = session.query(Category).all()
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash("Please enter a name.", "danger")
            return render_template('createRecipe.html', categories=categories)

        category_name = request.form['category'].strip()
        if not category_name:
            flash("Please choose a category")
            return render_template('createRecipe.html', categories=categories)
        try:
            category = session.query(Category).filter_by(
                       name=category_name).one()
        except Exception, e:
            flash("Please choose a valid category.")
            return render_template('createRecipe.html', categories=categories)

        description = request.form['description'].strip()
        servings = request.form['servings'].strip()
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        picture = request.files['picture']
        picture_data = None

        if picture:
            if not allowed_file(picture.filename):
                flash("The picture must be a JPEG or PNG file.")
                return render_template('createRecipe.html',
                                       categories=categories)

            picture_data = picture.read()

        recipeToCreate = Recipe(name=name,
                                description=description,
                                servings=servings,
                                ingredients=ingredients,
                                instructions=instructions,
                                category=category,
                                # image_url=filename,
                                user_id=login_session['user_id']
                                # creation_date=datetime.utcnow()
                                )

        if picture_data:
            recipeToCreate.picture = picture.filename
            recipeToCreate.picture_data = picture_data

        session.add(recipeToCreate)
        session.commit()
        flash('New Recipe %s Successfully Created' % (recipeToCreate.name))
        return redirect(url_for('showAllRecipes'))

    if request.method == 'GET':
        return render_template('createRecipe.html', categories=categories)


@app.route('/recipes/<int:recipe_id>/edit/', methods=['GET', 'POST'])
@login_required
def editRecipe(recipe_id):
    """ Edit a recipe if the signed in user is the author of the recipe """
    categories = session.query(Category).all()
    recipeToEdit = session.query(Recipe).filter_by(id=recipe_id).one()

    if recipeToEdit.user_id != login_session['user_id']:
        flash('You are not authorized to edit %s recipe' % recipeToEdit.name)
        return redirect(url_for('showAllRecipes'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash("Please enter a name.")
            return render_template('editRecipe.html',
                                   categories=categories,
                                   recipe=recipeToEdit)

        category_name = request.form['category'].strip()
        if not category_name:
            flash("Please choose a category")
            return render_template('editRecipe.html',
                                   categories=categories,
                                   recipe=recipeToEdit)
        try:
            category = session.query(Category).filter_by(
                       name=category_name).one()
        except Exception, e:
            flash("Please choose a valid category")
            return render_template('editRecipe.html',
                                   categories=categories,
                                   recipe=recipeToEdit)

        removeExistingPicture = request.form['removeExistingPicture']
        removeExistingPicture = removeExistingPicture.strip().lower()

        if removeExistingPicture == "true":
            recipeToEdit.picture = None
            recipeToEdit.picture_data = None

        picture = request.files['picture']
        picture_data = None

        if picture:
            if not allowed_file(picture.filename):
                flash("The picture must be a JPEG or PNG file.")
                return render_template('editRecipe.html',
                                       categories=categories,
                                       recipe=recipeToEdit)

            picture_data = picture.read()
            print "Content-Length: %s" % picture.content_length

        if picture_data:
            recipeToEdit.picture = picture.filename
            recipeToEdit.picture_data = picture_data

        description = request.form['description'].strip()
        servings = request.form['servings'].strip()
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        recipeToEdit.name = name
        recipeToEdit.description = description
        recipeToEdit.servings = servings
        recipeToEdit.ingredients = ingredients
        recipeToEdit.instructions = instructions
        recipeToEdit.category = category

        session.add(recipeToEdit)
        session.commit()
        flash('Recipe %s Successfully Edited' % recipeToEdit.name)
        return redirect(url_for('showAllRecipes'))
    if request.method == 'GET':
        return render_template('editRecipe.html',
                               recipe=recipeToEdit,
                               categories=categories)


@app.route('/recipes/<int:recipe_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteRecipe(recipe_id):
    """ Delete a recipe if the signed in user is the author of the recipe """
    recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
    if recipeToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete %s recipe'
              % recipeToDelete.name)
        return redirect(url_for('showAllRecipes'))
    if request.method == 'POST':
        session.delete(recipeToDelete)
        session.commit()
        flash('Recipe Successfully Deleted')
        return redirect(url_for('showAllRecipes'))
    else:
        return render_template('deleteRecipe.html', recipe=recipeToDelete)


@app.route('/disconnect')
@login_required
def disconnect():
    """ Disconnect based on provider """
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


@app.route('/static/images/uploads/<filename>')
def uploaded_file(filename):
    """ Returns url for a file in the uploads folder """
    return send_from_directory('/static/images/uploads/', filename)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
