import requests

#Base url for the api
recipeUrl = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
#Rapid API host
rapidHost = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"

#Get recipe and parse it out
def getRecipe(apiKey):
    #Get recipe json
    recipe = requests.get(recipeUrl, params={"number":"1"} ,headers={"X-RapidAPI-Key":apiKey, "X-RapidAPI-Host":rapidHost, "useQueryString": "true"}).json()["recipes"][0]["sourceUrl"]

    return(recipe)

#Run the app :)
def runApp(secretData):
    recipe = getRecipe(secretData["recipe"]["api_key"])

    #Parse as string
    recipeString = "Here is your daily recipe: \n" + recipe + "\n"

    return(recipeString)