import logging

import requests
from nltk.stem import WordNetLemmatizer

from src.configs import CAT_API_KEY

CAT_API_URL = "https://api.thecatapi.com/v1"
CAT_API_HEADER = {"x-api-key": CAT_API_KEY}


class CatAPIHandler:
    """Class to handle TheCatAPI services."""

    def __init__(self):
        self.CATEGORY_IDS = self._get_category_ids()
        self.BREED_IDS = self._get_breed_ids()

    def _get_category_ids(self):
        """
        Sends a request to The Cat API to retrieve all category ids and compile into a dictionary.

        :return: Dict mapping category keyword to category id
        """

        category_ids = {}
        parameter = "/categories"

        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)

        # list of each category
        json_data = response.json()

        lemmatizer = WordNetLemmatizer()

        for category_info in json_data:
            category_name = lemmatizer.lemmatize(category_info["name"])
            category_id = category_info["id"]
            category_ids[category_name] = category_id

        return category_ids

    def _get_breed_ids(self):
        """
        Sends a GET request to The Cat API to retrieve all breed ids and compile into a dictionary.

        :return: Dict mapping breed name to breed id
        """

        breed_ids = {}
        parameter = "/breeds"

        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)

        # list of each breed
        json_data = response.json()

        for breed_info in json_data:
            breed_name = breed_info["name"].lower()
            breed_id = breed_info["id"]
            breed_ids[breed_name] = breed_id

        return breed_ids

    def get_cat_image(self, category=None, breed=None):
        """
        Sends a request to TheCatAPI and retrieves only an image url.

        :param category: Optional parameter to get an image of a cat with a particular category. Valid categories
        include boxes, clothes, hats, sinks, space, sunglasses, and ties.
        :param breed: Optional parameter to get an image of a cat that is a specified breed.
        :return: Tuple containing the image url and text message.
        """

        # Category will get precedence if both category and breed are specified
        if category in self.CATEGORY_IDS:
            parameter = f"/images/search?category_ids={self.CATEGORY_IDS[category]}"

            if category in {"hat", "tie"}:
                message = f"Here is a cat wearing a {category}!"

            elif category in {"box", "sink"}:
                message = f"Here is a cat in a {category}!"

            elif category == "clothes":
                message = f"Here is a cat wearing clothes!"

            elif category == "space":
                message = f"Here is a cat in space!"

            # Default to getting a cat in sunglasses
            else:
                message = f"Here is a cat wearing sunglasses!"

        elif breed in self.BREED_IDS:
            parameter = f"/images/search?breed_ids={self.BREED_IDS[breed]}"
            message = f"Here is a {breed.title()} cat!"

        else:
            parameter = "/images/search"
            message = "Here is a random cat!"

        # Make request to API and get relevant data
        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)
        json_data = response.json()
        image_url = json_data[0]["url"]

        # Log data
        data = (
            f"The Cat API Parameters:\n"
            f"    Category?: {category}\n"
            f"    Breed?: {breed}\n"
            f"    API Parameter: {parameter}\n"
            f"    Response Code: {response.status_code}\n"
        )
        logging.info(data)

        return image_url, message
