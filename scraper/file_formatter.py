from datetime import datetime
from dataclasses import dataclass
import json
from dataclasses import dataclass, field, asdict
from typing import Optional
import os

RELEVANT_KEYS = ["place_id", "business_status", "delivery", "dine_in", "formatted_address", "formatted_phone_number",
                 "geometry", "name", "opening_hours", "place_id", "price_level", "rating", "reservable", "reviews",
                 "serves_beer", "serves_breakfast", "serves_brunch", "serves_dinner", "serves_lunch", "serves_wine",
                 "takeout", "types", "user_ratings_total", "website", "wheelchair_accessible_entrance"]


@dataclass
class Place:
    place_id: str = ""
    business_status: str = ""
    delivery: bool = False
    dine_in: bool = False
    formatted_address: str = ""
    formatted_phone_number: str = ""
    geometry: str = ""
    name: str = ""
    opening_hours: str = ""
    price_level: int = 0
    rating: float = 0.0
    reservable: bool = False
    reviews: str = ""
    serves_beer: bool = False
    serves_breakfast: bool = False
    serves_brunch: bool = False
    serves_dinner: bool = False
    serves_lunch: bool = False
    serves_wine: bool = False
    takeout: bool = False
    types: str = ""
    user_ratings_total: int = 0
    website: str = ""
    wheelchair_accessible_entrance: bool = False


def format_place_details(place_data: dict) -> dict:
    formatted_place = {k: v for k, v in place_data.items() if k in RELEVANT_KEYS}
    if (geometry := formatted_place.get("geometry")) and (location := geometry.get("location")):
        formatted_place["geometry"] = f"Latitude: {location.get('lat')}, Longitude: {location.get('lng')}"
    if (opening_hours := formatted_place.get("opening_hours")) and (weekdays := opening_hours.get("weekday_text")):
        formatted_place["opening_hours"] = ", ".join(weekdays)
    if reviews := formatted_place.get("reviews"):
        serialized_review = ""
        for review in reviews:
            rating, text, time = review.get('rating'), review.get('text'), review.get('time')
            if not isinstance(time, str):
                time = datetime.fromtimestamp(time).isoformat()
            if text:
                serialized_review += f"{rating = }, {text = }, time = {time};"

        formatted_place["reviews"] = serialized_review
    if types := formatted_place.get("types"):
        formatted_place["types"] = ", ".join(types)
    formatted_place = asdict(Place(**formatted_place))
    return formatted_place


def format_all_places(all_places: dict) -> list:
    return [{**{'place_id': k}, **format_place_details(v)} for k, v in all_places.items()]


if __name__ == "__main__":
    dir_path = 'scraper/data/details/'
    data_path = 'scraper/data/'
    entries = os.listdir(dir_path)
    places = {}
    for entry in entries:
        with open(dir_path + entry, 'r') as fp:
            tmp = json.load(fp)
            places[tmp['place_id']] = tmp

    final_final = format_all_places(places)
    with open(data_path + 'final_restaurants_and_bars.json', 'w') as fp:
        json.dump(final_final, fp)
