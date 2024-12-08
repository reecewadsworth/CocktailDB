import json
from DataWrapper import CocktailDataWrapper
from DataPull import CocktailDataPull

def main():
    # Fetch and save data (this will download everytime for this demo)
    pipeline = CocktailDataPull()
    pipeline.execute()

    # Initialize the wrapper with the saved data from cocktail_data.json
    wrapper = CocktailDataWrapper(data_file="cocktail_data.json")

    # Example: Get cocktail by ID
    try:
        cocktail_by_id = wrapper.get_cocktail_by_id("14029")
        print("Cocktail by ID:", json.dumps(cocktail_by_id, indent=4))
    except ValueError as e:
        print(e)

    # Example: Get cocktails by Name
    try:
        cocktails_by_name = wrapper.get_cocktails_by_names(["A1", "Abbey Martini"])
        print("Cocktails by Name:", json.dumps(cocktails_by_name, indent=4))
    except ValueError as e:
        print(e)

    # Example: Get specific attribute (e.g., Ingredients) for a cocktail by ID
    try:
        ingredients = wrapper.get_cocktail_attribute("14029", "Ingredients")
        print("Ingredients for Cocktail 14029:", ingredients)
    except ValueError as e:
        print(e)

    # Example: Get attribute for multiple cocktails
    try:
        attribute = wrapper.get_multiple_cocktails_attribute(["14029", "178318"], "DrinkThumb")
        print("Attribute for multiple cocktails:", attribute)
    except ValueError as e:
        print(e)

    # Example: Get instructions for a cocktail by ID in French
    try:
        cocktail_id = "14029"
        instructions_in_french = wrapper.get_instructions_by_language(cocktail_id, "fr")
        print("Instructions for Cocktail "+cocktail_id+" in french:", instructions_in_french)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
