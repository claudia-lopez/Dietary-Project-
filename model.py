"""Models for dietary app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    average_cal = db.Column(db.Integer)

    ratings = db.relationship("Rating", back_populates="user")
    userDiet = db.relationship("UserDiet", back_populates="user")
    userAllergy = db.relationship("UserAllergy", back_populates="user")


    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname} email={self.email}>"


class Recipe(db.Model):
    """A recipe."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    img_path = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe recipe_id={self.recipe_id} title={self.title}>"


class Rating(db.Model):
    """A recipe rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    recipe = db.relationship("Recipe", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")


    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

class UserDiet(db.Model):
    """A users diet."""

    __tablename__ = "UserDiets"

    userDiet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey("diets.diet_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    diet = db.relationship("Diet", back_populates="userDiet")
    user = db.relationship("User", back_populates="userDiet")

    def __repr__(self):
        return f"<UserDiet userDiet_id={self.userDiet_id}>"


class Diet(db.Model):
    """Types of diet."""

    __tablename__ = "diets"

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_name = db.Column(db.String)
    diet_overview= db.Column(db.Text)

    userDiet = db.relationship("UserDiet", back_populates="diet")

    def __repr__(self):
        return f"<Diet diet_id={self.diet_id} diet_name={self.diet_name}>"

class UserAllergy(db.Model):
    """A users allergies."""

    __tablename__ = "user_allergy"

    userAllergy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey("allergies.allergy_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    allergy = db.relationship("Allergy", back_populates="userAllergy")
    user = db.relationship("User", back_populates= "userAllergy")


    def __repr__(self):
        return f"<UsersAllergy userAllergy_id={self.userAllergy_id}>"


class Allergy(db.Model):
    """Types of allergies."""

    __tablename__ = "allergies"

    allergy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    allergy_name = db.Column(db.String)

    userAllergy = db.relationship("UserAllergy", back_populates="allergy")

    def __repr__(self):
        return f"<Allergy allergy_id={self.allergy_id} allergy_name={self.allergy_name}>"


def connect_to_db(flask_app, db_uri="postgresql:///diet", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    with app.app_context():
        connect_to_db(app)
