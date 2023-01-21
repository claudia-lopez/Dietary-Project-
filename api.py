import requests

def getRecipes(args):
    url = "https://api.spoonacular.com/recipes/complexSearch?apiKey=6bc813462a6845c9a07de5093bf2bca4"
    for key, value in args.items():
        url += "&" + key + "=" + value
    res = requests.get(url)
    data = res.json()['results']
    return data

# To unpack:
# args = {'diet': '', 'cuisine': 'italian', 'intolerances': ''}
#
# data = getRecipes(args)
# for item in data:
#      for i in item:
#          print(i, " : ", item[i])


def getRecipeInfo(recipe_id):
    url = "https://api.spoonacular.com/recipes/" + recipe_id + "/information?apiKey=6bc813462a6845c9a07de5093bf2bca4&includeNutrition=false"
    res = requests.get(url)
    data = res.json()
    data2 = {}
    ingredients = []
    info = []
    for i in data:
        if data[i] == True:
            info.append(i)
    h = data.get('extendedIngredients')
    for i in h:
        ingredients.append(i.get("original"))
    data2['instructions'] = data.get('instructions')
    data2['ingredients'] = ingredients
    data2['info'] = info
    data2['summary'] = data.get('summary')
    data2['title'] = data.get('title')
    data2['image'] = data.get('image')
    data2['id'] = data.get('id')
    return(data2)
