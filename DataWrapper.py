import json

class CocktailDataWrapper:
    def __init__(self, data_file="cocktail_data.json"):
        # Load the data from the file
        self.cocktail_data = self.load_data_from_file(data_file)

    def load_data_from_file(self, data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception("Cocktails file was not found")
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON from the cocktails file")

    def get_cocktail_by_id(self, cocktail_id):
        # Find cocktail by ID
        for cocktail in self.cocktail_data:
            if cocktail["CocktailID"] == cocktail_id:
                return cocktail
        raise ValueError("Cocktail with ID "+cocktail_id+" not found.")

    def get_cocktails_by_ids(self, cocktail_ids):
        # Find multiple cocktails by a list of IDs
        matching_cocktails = []
        for cocktail in self.cocktail_data:
            if cocktail["CocktailID"] in cocktail_ids:
                matching_cocktails.append(cocktail)
        return matching_cocktails
    
    def get_cocktail_by_name(self, cocktail_name):
        # Find cocktail by Name
        for cocktail in self.cocktail_data:
            if cocktail["Name"].lower() == cocktail_name.lower():
                return cocktail
        raise ValueError("Cocktail with name "+cocktail_name+" not found.")
    
    def get_cocktails_by_names(self, cocktail_names):
        # Find multiple cocktails by a list of Names
        matching_cocktails = []
        for cocktail in self.cocktail_data:
            for name in cocktail_names:
                if cocktail["Name"].lower() == name.lower():
                    matching_cocktails.append(cocktail)
        return matching_cocktails
    
    def get_cocktail_attribute(self, cocktail_id, attribute):
        # Get a specific attribute for a given cocktail ID
        cocktail = self.get_cocktail_by_id(cocktail_id)
        attribute_value = cocktail.get(attribute)
        if attribute_value is None:
            return attribute+" not found in cocktail data."
        return attribute_value
    
    def get_multiple_cocktails_attribute(self, cocktail_ids, attribute):
        # Get specific attribute for multiple cocktails
        attributes = {}
        for cocktail in self.get_cocktails_by_ids(cocktail_ids):
            attribute_value = cocktail.get(attribute)
            if attribute_value is None:
                attributes[cocktail["CocktailID"]] = attribute+" not found in cocktail data."
            else:
                attributes[cocktail["CocktailID"]] = attribute_value
        return attributes

    def get_instructions_by_language(self, cocktail_id, language='en'):
        # Get instructions for a given cocktail in a given language
        cocktail = self.get_cocktail_by_id(cocktail_id)
        
        # Find the instructions for the specified language
        instructions = cocktail["Instructions"]
        if language in instructions:
            return instructions[language]
        
        # If the requested language is not found, return English instructions
        return instructions.get('en', "Instructions not available.")
