"""CRUD (Create, Read, Update, Delete) operations."""

from model import db, User, Recipe, Rating, UserLikes, connect_to_db

#################user##########################


def create_user(email, password, user_diet, user_allergy):
    """Create and return a new user."""

    user = User(email=email, password=password, user_diet=user_diet, user_allergy=user_allergy)
    print('successfully added')
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_email(email):

    return User.query.filter(User.email == email).first()

def get_user_by_password(password):

    return User.query.filter(User.password == password).first()

###################recipe############################

def create_recipe(title, summary , info,  instructions, ingredients, image):
    """Create and return a new recipe."""

    recipe = Recipe(
        title=title,
        summary=summary,
        info=info,
        instructions=instructions,
        ingredients=ingredients,
        image=image,
    )
    db.session.add(recipe)
    db.session.commit()

    return recipe

def search_recipe_id(id):

    return Recipe.query.filter(Recipe.recipe_id == id).first()

#####################rating############################

def create_rating(user_id, recipe_id, score):
    """Create and return a new rating."""

    rating = Rating(user_id=user_id, recipe_id=recipe_id, score=score)
    db.session.add(rating)
    db.session.commit()

    return rating

def view_ratings(recipe_id):
    """view a rating."""
    ratings = db.session.query(Rating).filter(Rating.recipe_id == recipe_id).all()

    return ratings


def get_rating(user, recipe):
    rating = db.session.query(Rating).filter(Rating.user_id == user,Rating.recipe_id == recipe).first()
    return rating



####################liked_recipes############################
def get_recipe_by_user1(user):
    fav = db.session.query(Recipe.title, Recipe.recipe_id, Recipe.image, UserLikes.liked).join(UserLikes).filter(UserLikes.recipe_id==Recipe.recipe_id).join(User).filter(user == UserLikes.user_id).all()

    return fav

def user_likes_recipe(email,recipe):
    user= get_user_by_email(email)
    recipe_id=search_recipe_id(recipe)
    liked=UserLikes(recipe_id=recipe, user_id=user.user_id)
    db.session.add(liked)
    db.session.commit()
    return liked 

def get_by_recipe_user(user, recipe):
    liked_id = db.session.query(UserLikes).filter(UserLikes.user_id == user,UserLikes.liked_id == recipe).first()

    return liked_id

def change_to_dislike(user, recipe):
    liked_id = db.session.query(UserLikes).filter(UserLikes.user_id == user,UserLikes.liked_id == recipe).first()
    liked_id.likes = False
    db.session.commit()
    return liked_id

def change_to_like(user, recipe):
    liked_id= db.session.query(UserLikes).filter(UserLikes.user_id == user,UserLikes.liked_id == recipe).first()
    liked_id.likes = True
    db.session.commit()
    return liked_id




if __name__ == "__main__":
    from server import app

    connect_to_db(app)


