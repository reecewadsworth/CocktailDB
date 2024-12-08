### CocktailDB - Documentation
An example of how to pull data from www.thecocktaildb.com. With a useful wrapper to more easily facilitate data handling. This is a short demonstration of how I would typically go about a simple data ETL via a REST API. This example took a little over 2 hours, including documentation.

#### Files:
- _Datapull.py_ - Where the functions related to the data pull and cleanup are housed.
- _DataWrapper.py_ - A useful library of functions that the user would use to interact with the JSON data.
- _utils.py_ - A helper package to aid with data cleanup.
- _main.py_ - The main function that should be run to demonstrate functionality

#### How to run:

1. Simply clone the repo.
2. Run _python main.py_ to run the data pull and cleanse and output some basic examples of how the _DataWrapper.py_ can be used.
3. _cocktail_data.json_ will appear in the root of the project with data for 100 cocktails.
4. (optional) Edit _main.py_ as you wish and have a play with some of the included functions within _DataWrapper.py_.

#### Dependencies:
- [unidecode](https://pypi.org/project/Unidecode/ "unidecode")
- [requests](https://pypi.org/project/requests/ "requests")

#### Rationale: (Question 4)
For this project I chose to clean the data during its ingestion. The reason for this is because we are limited to only 100 cocktails via the REST API; there simply isn't the need to store and batch process data. The entire process takes 30-60 seconds to complete a data pull, including a 10-second pause, which is needed every 60 requests to the REST API, and during this there is no saving of the raw data as it isn't outlined as needed in the requirements nor is it needed for performance reasons. If we needed to pull larger amounts of data, then it would be sensible to batch the data and process it potentially in parallel to greatly decrease the required processing time. The solution I have implemented here is not highly scalable due to being single-threaded in nature and getting exponentially harder to process with added records. I am aware of this but chose to implement it this way due to the size of the data and the time allocated for the task.

#### Shortcomings 
This implementation is not perfect, and I am aware of it and would work on the following if I had more time:
- convert_oz_to_ml() removes all text after the measurement. (Wine 1 oz. white -> Wine 30 ml)
- Unidecode often removes special characters, accents, and special markers and instead maps to the closest English character.


