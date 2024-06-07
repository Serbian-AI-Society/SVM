import time
import requests
import json
import numpy as np
import os
from reviews_scraper import GoogleMapsAPIScraper
import re


def get_places(api_key, location, radius, type):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={api_key}"
    restaurants = []

    while url:
        response = requests.get(url)
        results = response.json().get("results", [])
        restaurants.extend(results)

        next_page_token = response.json().get("next_page_token")
        if next_page_token:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"
            time.sleep(2)  # Pause to wait for the next page token to become valid
        else:
            url = None

    return restaurants


def get_place_reviews_and_details(api_key, place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching place details")
        return []

    return response.json().get("result", {})


def get_reviews(place_id, max_reviews=20, language='en', sort_by='most_relevant'):
    place_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'

    # Get the place url
    while True:
        response = requests.get(place_url)
        if response.status_code != 200:
            print("Error fetching place details. Retrying...")
            time.sleep(2)
        else:
            break
    
    # Patern for the feature id extraction
    pattern = r'0[xX][0-9a-fA-F]+:0[xX][0-9a-fA-F]+'
    matches = re.findall(pattern, response.text)
    
    if len(matches) == 0:
        print("No feature id found: ", place_url)
        return

    reviews = []
    with GoogleMapsAPIScraper() as scraper:
        results = scraper.scrape_reviews(
            url_name=restaurant.get("name"),
            n_reviews=max_reviews,
            hl=language,
            feature_id=matches[0],
            sort_by=sort_by
        )
        
        for result in results:
            # Get translated text if available
            result_text = result.get("text")
            if result.get("translated_text"):
                result_text = result.get("translated_text")

            review = {
                "rating": result.get("rating"),
                "text": result_text,
                "time": result.get("text_date")
            }
            reviews.append(review)

    return reviews


def f_bg_pins():
    # Define the bounding box for Belgrade
    lat_min, lat_max = 44.67, 44.91
    lon_min, lon_max = 20.36, 20.63

    # Calculate the number of rows and columns to create around 70 pins
    num_pins = 70
    aspect_ratio = (lat_max - lat_min) / (lon_max - lon_min)
    num_cols = int(np.sqrt(num_pins / aspect_ratio))
    num_rows = int(np.ceil(num_pins / num_cols))

    # Generate the coordinates for each pin
    latitudes = np.linspace(lat_min, lat_max, num_rows)
    longitudes = np.linspace(lon_min, lon_max, num_cols)

    bg_pins = [(lat, lon) for lat in latitudes for lon in longitudes]

    # Make sure we only have 70 pins (if we have more due to rounding, slice the list)
    bg_pins = bg_pins[:num_pins]

    # Calculate the distance between pins
    lat_distance = (lat_max - lat_min) / (num_rows - 1)
    lon_distance = (lon_max - lon_min) / (num_cols - 1)

    return bg_pins, lat_distance, lon_distance


if __name__ == "__main__":
    API_KEY = os.getenv("GMAP_API_KEY")
    if not API_KEY:
        raise ValueError("GMAP_API_KEY environment variable is not set")
    radius = 2400  # Search radius in meters
    max_review = 10
    types = ["restaurant", "bar"]  # Types of places to search for
    bg_pins, lat_distance, lon_distance = f_bg_pins()
    places_g = {}
    redo_w_shift = False

    directory_path = "scraper/data/details/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory {directory_path}")

    # Get places for each pin
    for place_type in types:
        print("=" * 80)
        print("Place type: ", place_type)
        iter = 0
        while iter < len(bg_pins):
            pin = bg_pins[iter]
            if redo_w_shift:
                pin = (pin[0] + lat_distance / 2, pin[1] + lon_distance / 2)
            pin_str = ",".join(map(str, pin))

            restaurants = get_places(API_KEY, pin_str, radius, place_type)
            print(f"{iter}: fetched {len(restaurants)} restaurants for pin {pin_str}, total: {len(places_g)}")

            # Get reviews for each restaurant
            for restaurant in restaurants:
                place_id = restaurant.get("place_id")
                reviews_and_details = get_place_reviews_and_details(API_KEY, place_id)
                if max_review > 5:
                    reviews_and_details["reviews"] = get_reviews(place_id, max_reviews=max_review)
                reviews_and_details["map_url"] = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
                # print(f"Reviews for", restaurant.get("name"))
                # for review in reviews_and_details.get("reviews", []):
                #     author = review.get("author_name")
                #     rating = review.get("rating")
                #     text = review.get("text")
                #     print(f"Author: {author}")
                #     print(f"Rating: {rating}")
                #     print(f"Text: {text}")
                #     print("-" * 40)
                # print("=" * 80)
                with open(directory_path + f"{place_type}_{place_id}.json", "w") as fp:
                    json.dump(reviews_and_details, fp)
                places_g[place_id] = reviews_and_details

            if len(restaurants) == 60 and not redo_w_shift:
                print(" - Shifting pin")
                redo_w_shift = True
            else:
                iter += 1
                redo_w_shift = False
        print("Found ", len(places_g), " places for type ", place_type)

    print(f"Total places: {len(places_g)}")


