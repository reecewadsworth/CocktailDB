import requests
import json
import time
from utils import convert_oz_to_ml
from utils import clean_unicode_escape_sequences

class CocktailDataPull:
    def __init__(self):
        self.base_url = "https://www.thecocktaildb.com/api/json/v1/1/"

    #Fetches raw data via simple rest API pull.
    def fetch_cocktail_data(self): 
        all_cocktails_response = requests.get(self.base_url+"filter.php?c=Cocktail") #Gets all cocktails
        if all_cocktails_response.status_code != 200:
            raise Exception("Get request failed")
        
        cocktail_ids = [] #list of all cocktails_ids 
        for drink in all_cocktails_response.json()["drinks"]:
            cocktail_ids.append(drink["idDrink"])
        
        cocktails = []
        counter = 0
        for cocktail_id in cocktail_ids:
            if(counter == 59):
                time.sleep(10) #On 60th request it is required to wait 10 seconds due to API restrictions.

            cocktail_response = requests.get(self.base_url+"lookup.php?i="+cocktail_id)
            if cocktail_response.status_code == 200:
                cocktails.append(cocktail_response.json()["drinks"][0])

            counter = counter + 1

        return cocktails

    #Error handles and formats the data
    def transform_and_clean_data(self, raw_data):
        transformed_data = []
        #Transform step
        for cocktail in raw_data:
            ingredients = []
            for i in range(1, 16):  # Recipe can only have 15 ingredients
                ingredient = cocktail.get("strIngredient"+str(i))
                measure = cocktail.get("strMeasure"+str(i))
                if ingredient == None:
                    break #break so nulls are not processed.
                if measure != None:
                    ingredients.append(ingredient.strip()+" - "+convert_oz_to_ml(measure).strip())
                else:
                    ingredients.append(ingredient.strip()) #Not all ingredients have measurements
            
            # Cleaning step
            if ingredients == None:
                ingredients = ["No ingredients listed"] #Handle no ingredients found
            
            # Standard handling of special common special characters
            name = clean_unicode_escape_sequences(cocktail.get("strDrink", ""))

            date_modified = cocktail.get("dateModified", "Not provided")
            tags = cocktail.get("strTags", "None").split(",") if cocktail.get("strTags") else []
            drink_thumb = cocktail.get("strDrinkThumb", "No image available")

            # Collect instructions in all available languages
            instructions = {}
            for key, value in cocktail.items():
                if key.startswith("strInstructions") and value:
                    language = key.replace("strInstructions", "").lower() or "en"  # Default language is English but does not have signifier
                    instructions[language] = clean_unicode_escape_sequences(value)
            
            transformed_cocktail = {
                "CocktailID": cocktail.get("idDrink"),
                "Name": name,
                "Category": cocktail.get("strCategory"),
                "Alcoholic": cocktail.get("strAlcoholic") == "Alcoholic",
                "GlassType": cocktail.get("strGlass"),
                "Ingredients": ingredients,
                "Instructions": instructions,
                "DateModified": date_modified,
                "Tags": tags,
                "DrinkThumb": drink_thumb
            }
            
            transformed_data.append(transformed_cocktail)
        
        return transformed_data

    def execute(self):
        raw_data = self.fetch_cocktail_data()
        clean_data = self.transform_and_clean_data(raw_data)

        # Save the fetched data to a JSON file
        with open("cocktail_data.json", "w") as file:
            json.dump(clean_data, file, indent=4)
    
        print("Cocktail data successfully pulled and saved to cocktail_data.json.")
