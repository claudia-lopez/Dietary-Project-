"""Models for dietary app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///diet", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_diet = db.Column(db.String)
    user_allergy = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="user")
    liked_recipe = db.relationship("UserLikes", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Recipe(db.Model):

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    summary = db.Column(db.Text)
    info = db.Column(db.Text)
    instructions = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    image = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="recipe")
    liked_recipe = db.relationship("UserLikes", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe recipe_id={self.recipe_id} title={self.title}>"


class Rating(db.Model):

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    recipe = db.relationship("Recipe", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")


    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"


class UserLikes(db.Model):

    __tablename__ = "liked_recipe"

    liked_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    liked = db.Column(db.Boolean, default = True, nullable = False)

    recipe = db.relationship("Recipe", back_populates="liked_recipe")
    user = db.relationship("User", back_populates="liked_recipe")




if __name__ == "__main__":
    from server import app
    with app.app_context():
        connect_to_db(app)
        db.create_all()