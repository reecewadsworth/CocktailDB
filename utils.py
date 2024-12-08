from fractions import Fraction
import re
from unidecode import unidecode

def convert_oz_to_ml(measurement):
    # Check if the measurement contains "oz"
    if 'oz' in measurement.lower():
        # Regex to match the measurement (whole, fraction, or mixed number) and ignore extra text after "oz"
        match = re.match(r'(\d+\s\d+/\d+|\d+/\d+|\d+)(?=\s*oz)', measurement.strip().lower())
        if match:
            # Extract the number before "oz"
            numeric_part = match.group(1)
            try:
                # Handle Mixed fraction, fractions and integers
                if ' ' in numeric_part:  # Mixed fraction ("1 1/4")
                    whole, fraction = numeric_part.split(' ')
                    quantity_in_oz = float(whole) + float(Fraction(fraction))
                elif '/' in numeric_part:  # Fraction
                    quantity_in_oz = float(Fraction(numeric_part))
                else:  # Integers
                    quantity_in_oz = float(numeric_part)
                
                # Convert the quantity in oz to ml (1 oz = 29.5735 ml) but rounded for nicer results
                quantity_in_ml = quantity_in_oz * 30
                return str(quantity_in_ml)+" ml" #this does remove some flavour text after the measurement but this should be in the ingredients not measurements.
                
            except ValueError as e:
                return measurement
        else:
            # If the regex doesn't match, return the original (this can happen where the conversion is already present e.g. "Vodka - 70ml/2fl oz" but this is out of scope)
            return measurement
    else:
        # If not oz then skip
        return measurement

# Function to clean up Unicode escape sequences
def clean_unicode_escape_sequences(text):
    # Preprocess to remove unwanted characters
    preprocessed_text = re.sub(r'[A-Za-z0-9]+\+-?[A-Za-z0-9]*', '', text)

    # Using unidecode library to convert foreign characters to closest equivalent
    cleaned_text = unidecode(preprocessed_text)
    return cleaned_text