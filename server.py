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
app.config['JWT_TOKEN_LOCATION'] = ['query_string']
jwt = JWTManager(app)

app.config["JWT_QUERY_STRING_NAME"] = "jwt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=10)

@jwt.invalid_token_loader
def handle_invalid_token(invalid_token):
    return "Your session has expired. Please login again.", 401


@app.route("/index", methods=["GET", "POST"])
def index():
    jwt = request.args.get("jwt")
    if jwt:
        return render_template("indexloggedin.html")
    else:
        return render_template("index.html")
#sofia
# @app.route("/")
# def main():
#     return render_template("index.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        return {"endpoint" : url_for("login")}
    elif request.method == "GET":
        return render_template("signup.html")
#sofia
# @app.route("/signup", methods=["GET"])
# def signup():
#     # user=model.User(email)
#     return render_template("signup1.html") #showing that the Db works, impiment this one signup.html
#sofia
# @app.route("/signup", methods=["POST"])
# def signup2():
#     email = request.form.get("email") #! get this info from signup.html
#     password= request.form.get("password")
#     in_db = crud.get_user_by_email(email)
#     print(in_db)
#     if in_db:
#         flash("No user found with email")#! NEEDS TO ADD FLASH MESSAGES IN HTML
#         return redirect("/")
#     user = model.User(email = email, password = password)
#     model.db.session.add(user)
#     model.db.session.commit()
#     # password1= request.form.get("passwordconf")
#     print(email,password)
#     return render_template("indexloggedin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        access_token = create_access_token(identity=data.get('email'))
        vs = crud.verify_user(data.get('email'), data.get('password'))
        print(vs)
        if (vs == False):
            return "fail"
        else:
            return {"jwt" : access_token, "endpoint" : url_for("index")}
    elif request.method == "GET":
        return render_template("login.html")
#sofia
# @app.route("/login")
# def login():
#     email = request.form.get("email") #how to get this info from frontend
#     password= request.form.get("password")
#     user = crud.get_user_by_email(email)
#     if user:
#         if user.password == password:
#             return render_template("login.html")
#     flash("Incorrect email or Password")
#     return redirect("/")

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
@jwt_required()
def menu():
    args = request.get_json()
    recipes = api.getRecipes(args)
    return (render_template("menu.html", recipes=recipes))

@app.route("/recipeinfo", methods=["POST"])
@jwt_required()
def recipeinfo():
    json = request.get_json()
    recipe_id = json.get('id')
    recipe = api.getRecipeInfo(recipe_id)
    return render_template("recipeinfo.html", recipe=recipe)


@app.route("/like", methods=["POST"])
@jwt_required()
def like():
    json = request.get_json()
    recipe_id = json.get('id')
    current_user = get_jwt_identity()
    pass


@app.route("/rate", methods=["POST"])
@jwt_required()
def rate():
    json = request.get_json()
    recipe_id = json.get('id')
    rating = json.get('rating')
    current_user = get_jwt_identity()
    pass


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
