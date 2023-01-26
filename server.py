from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
#from model import connect_to_db, db
import model
import crud
import api

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dnsajkcnjksdncj"

app.jinja_env.undefined = StrictUndefined
# app.config['JWT_TOKEN_LOCATION'] = ['query_string']
jwt = JWTManager(app)
SECRET_KEY = "fg4ois345jfg9898osig346jo2fg"
# app.config["JWT_QUERY_STRING_NAME"] = "jwt"
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=10)

@jwt.invalid_token_loader
def handle_invalid_token(invalid_token):
    return "Your session has expired. Please login again.", 401


# @app.route("/index", methods=["GET", "POST"])
# def index():
#     jwt = request.args.get("jwt")
#     if jwt:
#         return render_template("indexloggedin.html")
#     else:
#         return render_template("index.html")
#sofia
@app.route("/")
def main():
    return render_template("index.html")
    
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         data = request.get_json()
#         return {"endpoint" : url_for("login")}
#     elif request.method == "GET":
#         return render_template("signup.html")
#sofia
@app.route("/signup", methods=["GET"])
def signup():
    # user=model.User(email)
    return render_template("signup.html") #showing that the Db works, impiment this one signup.html
#sofia
@app.route("/signup", methods=["POST"])
def signup2():
    email = request.form.get("email") #! get this info from signup.html
    password= request.form.get("password")
    in_db = crud.get_user_by_email(email)
    print(in_db," IN DB\n\n\n\n\n")
    if in_db:
        flash("Email already exist, please try to log in")#! NEEDS TO ADD FLASH MESSAGES IN HTML
        return redirect("/")
    user = model.User(email = email, password = password)
    model.db.session.add(user)
    model.db.session.commit()
    # password1= request.form.get("passwordconf")
    print(email,password, "THIS IS IT")
    return render_template("indexloggedin.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         data = request.get_json()
#         access_token = create_access_token(identity=data.get('email'))
#         vs = crud.verify_user(data.get('email'), data.get('password'))
#         print(vs)
#         if (vs == False):
#             return "fail"
#         else:
#             return {"jwt" : access_token, "endpoint" : url_for("index")}
#     elif request.method == "GET":
#         return render_template("login.html")
#sofia
@app.route("/login", methods=["GET"])
def loginGet():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    session['email'] = request.form.get("email")
    password= request.form.get("password")
    user = crud.get_user_by_email(session['email'])
    if user:
        if user.password == password:
            return render_template("indexloggedin.html")
    flash("Incorrect email or Password")
    return redirect("/login")

@app.route("/profile", methods=["GET", "POST"])
@jwt_required()
def userpage():
    current_user = get_jwt_identity()
    favorites = []
    if request.method == "POST":
        return (url_for("homepage"))
    elif request.method == "GET":
        return render_template("userpage.html", favorites=favorites)


# @app.route("/menu", methods=["POST"])
# @jwt_required()
# def menu():
#     args = request.get_json()
#     print(args)
#     recipes = api.getRecipes(args)
#     print(recipes)
#     return (render_template("menu.html", recipes=recipes))

@app.route("/menu", methods=["POST"])
def menu():
    json = request.get_json()
    diet = json.get('diet')
    cuisine = json.get('cuisine')
    intolerances = json.get('intolerances')

    # print(recipe_id)
    
    recipes = api.getRecipes(diet = diet, cuisine=cuisine, intolerances=intolerances )

    return (render_template("menu.html", recipes=recipes))

@app.route("/recipeinfo", methods=["POST"])
def recipeinfo():
    json = request.get_json()
    recipe_id = json.get('id')
    recipe = api.getRecipeInfo(recipe_id)
    return render_template("recipeinfo.html", recipe=recipe)


@app.route("/like", methods=["POST"])
def like():
    json = request.get_json()
    recipe_id = json.get('id')
    recipe_api=api.getRecipeInfo(recipe_id)
    # print(recipe_api['title'])
    recipe=model.Recipe(recipe_id =recipe_id ,title=recipe_api['title'], summary=recipe_api['summary'], info=recipe_api['info'],  instructions=recipe_api['instructions'], ingredients=recipe_api['ingredients'], image=recipe_api['image'])
    print(recipe_api)
    model.db.session.add(recipe)
    model.db.session.commit()
    user_likes=crud.user_likes_recipe(email=session['email'],recipe=int(recipe_id))
    model.db.session.add(user_likes)
    model.db.session.commit()
    # current_user = get_jwt_identity()
    return redirect("/favorites")

@app.route("/favorites")
def favorites():
    recipes =crud.get_recipe_by_user1(1)

    return render_template("userpage.html", recipes=recipes)


# @app.route("/rate", methods=["POST"])
# def rate():
#     json = request.get_json()
#     recipe_id = json.get('id')
#     rating = json.get('rating')
#     current_user = get_jwt_identity()
#     pass


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
