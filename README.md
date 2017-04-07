# Item Catalog

This project is a simple web application that provides a list of recipes within several categories. It uses third party authentication, and logged in users can add, edit, and delete their own recipes. Project is built using Python, Flask, SQL Alchemy, and Twitter Bootstrap.

Initial (Vagrant) config cloned from (https://github.com/udacity/fullstack-nanodegree-vm)

### Basic features

* Non authenticated users can browse the categories and list of recipes, but cannot make any modifications.
* Authenticated users can add, edit, and delete their own recipes.
* All recipes are publicly visible. The home page shows list of categories
* Third party authentication using Google account sign-in.
* JSON endpoints: 
** list of categories
** list of all recipes
** recipes in one category
** single recipe

### Additional features
* View user profile: logged in users can see their own list of items

### TODO List (Basic and Additional Features)
* Allowing the users to determine if their items are visible to public or not.
* Recipes can have an image uploaded. User should be able to upload multiple images.
* Use tokens to prevent cross-site request forgeries (CSRF).
* Create a recipe search option.
* Add additional recipe types (e.g. gluten-free, lactose-free, vegan)

### Current Issues
* Items can have an image uploaded. Currently images are saved but are not retrieved.
* Images are not deleted when a recipe is deleted.

### Requirements

This project includes a Vagrant virtual environment. To use it, install VirtualBox and (Vagrant), and follow the project installation steps bellow.

### Installation

1. Clone the project repository and connect to the virtual machine 
```
$ git clone https://github.com/mlupin/fullstack-nanodegree-item-catalog.git
$ cd fullstack-nanodegree-item-catalog
$ vagrant up
$ vagrant ssh
$ cd /vagrant
```

2. Setup and populate the database to include sample users and recipes.
```
vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant
vagrant@vagrant-ubuntu-trusty-32:/vagrant$ python database_setup.py
vagrant@vagrant-ubuntu-trusty-32:/vagrant$ python project.py
```

3. Configure Google Sign-in
A client ID is not provided. Use your own client ID to test the application.

Create a Google Developers Console project. Then go to the credentials tab and download the client ID as a JSON file. Copy the file to the project folder and rename it client_secrets.json.

4. Point your browser to 'localhost:5000' to run the application.

### Recognition
* Family: Many of sample recipes are family recipes.
* (Pixabay)[https://pixabay.com/en/]: All sample images were downloaded from Pixabay, All images and videos on Pixabay are released free of copyrights under Creative Commons CC0.