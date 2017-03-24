from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base
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
APPLICATION_NAME = "Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    return render_template('login.html')


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    return render_template('categories.html')


# Create a new category
@app.route('/catalog/new/')
def newCategory():
    return render_template('newCategory.html')


# Edit a category
@app.route('/catalog/<int:category_id>/edit/')
def editCategory():
    return render_template('editCategory.html')


# Delete a category
@app.route('/catalog/<int:category_id>/delete/')
def deleteCategory():
    return render_template('deleteCategory.html')


# Show a category catalog
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items/')
def showCatalog():
    return render_template('catalog.html')


# Show a catalog item
@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showCatalogItem():
    return render_template('catalogItem.html')


# Create a new catalog item
@app.route('/catalog/<int:category_id>/items/new/')
def newCatalogItem():
    return render_template('newCatalogItem.html')


# Edit a catalog item
@app.route('/catalog/<int:item_id>/edit/')
def editCatalogItem():
    return render_template('editCatalogItem.html')


# Delete a catalog item
@app.route('/catalog/<int:item_id>/delete/')
def deleteCatalogItem():
    return render_template('deleteCatalogItem.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
