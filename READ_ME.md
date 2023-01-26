# Local Host 500
An app that allows you to search for recipes based on specific cuisine, diet, or have food intolerances.

## Summary

**Local Host 500** All YourFavoriteRecipes allows you to search for recipes that fit your preferences, whether it be a specific cuisine, diet, or food intolerance. The website offers a wide range of options to choose from. Furthermore, The features of this platform include the ability to create an account, login and logout, browse through recipes, save recipes for later.

Back End: Python3, Flask framework, SQLAlchemy ORM, Postgresql database
Front End: JavaScript, AJAX, JSON, Jinja2, HTML, CSS
APIs: Spoonacular API

Features:
A user can create an account, login and logout, browse through recipes, and save recipes for later.


## Local Installation
Requirements:
Need to acquire Spoonacular API key.

Clone repository:

$ git clone https://github.com/claudia-lopez/Dietary-Project-.git
Setup Flask:
Create a virtual environment:

$ virtualenv env
Activate the virtual environment:

$ source env/bin/activate
Install dependencies:

$ pip3 install -r requirements.txt
Setup Credentials/Secrets:
Create a secrets.sh file

Setup the database:
Once your API credentials are retrieved, you can create your database.

With PostgreSQL installed, create your database 'Users':

$ createdb Users
Create your database tables:

$ python3 model.py

$ python3 server.py
To start the Flask web server, run:

$ python3 server.py
In your browser, visit http://localhost:5000/

### Connect and learn more about Claudia on LinkedIn.
<a href="www.linkedin.com/in/claudia-lopez-93a48b24a" target="_blank">Claudia's LinkedIn</a>