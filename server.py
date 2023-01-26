from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import datetime
import model
import crud
import api
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dnsajkcnjksdncj"

app.jinja_env.undefined = StrictUndefined
jwt = JWTManager(app)
SECRET_KEY = "fg4ois345jfg9898osig346jo2fg"

@jwt.invalid_token_loader
def handle_invalid_token(invalid_token):
    return "Your session has expired. Please login again.", 401


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup2():
    email = request.form.get("email")
    password= request.form.get("password")
    in_db = crud.get_user_by_email(email)
    if in_db:
        flash("Email already exist, please try to log in")
        return redirect("/")
    user = model.User(email = email, password = password)
    model.db.session.add(user)
    model.db.session.commit()
    return render_template("indexloggedin.html")


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


@app.route("/menu", methods=["POST"])
def menu():
    json = request.get_json()
    diet = json.get('diet')
    cuisine = json.get('cuisine')
    intolerances = json.get('intolerances')
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
    recipe=model.Recipe(recipe_id =recipe_id ,title=recipe_api['title'], summary=recipe_api['summary'], info=recipe_api['info'],  instructions=recipe_api['instructions'], ingredients=recipe_api['ingredients'], image=recipe_api['image'])
    print(recipe_api)
    model.db.session.add(recipe)
    model.db.session.commit()
    user_likes=crud.user_likes_recipe(email=session['email'],recipe=int(recipe_id))
    model.db.session.add(user_likes)
    model.db.session.commit()
    return redirect("/favorites")


@app.route("/favorites")
def favorites():
    recipes =crud.get_recipe_by_user1(1)
    return render_template("userpage.html", recipes=recipes)


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
