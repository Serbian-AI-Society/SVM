def summary(htm_web) -> str:
    summary = ""
    return summary


import requests
import json
import os
from summarizer import get_completion_from_messages

if __name__ == "__main__":
    # dir_path = 'scraper/data/details/'
    data_path = 'scraper/data/'
    # entries = os.listdir(dir_path)
    # places = {}
    # for entry in entries:
    #     with open(dir_path + entry, 'r') as fp:
    #         tmp = json.load(fp)
    #         places[tmp['place_id']] = tmp
    #
    # final_final = format_all_places(places)
    with open(data_path + 'final_restaurants_and_bars.json', 'r') as fp:
        restaurants_and_bars = json.load(fp)

    wolt_base_url = "https://wolt.com/en/geo/batumi/restaurant/"

    restaurants_with_website = [place for place in restaurants_and_bars if ('restaurant' in place["types"]) and place["website"]]
    selected_restaurants = []
    for i, restaurant in enumerate(restaurants_with_website):
        if i==24:
            continue
        print(f"#{i} working on restaurant {restaurant['website']} ")
        try:
            response = requests.get(restaurant["website"], timeout=10, allow_redirects=False)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.exceptions.TooManyRedirects as e:
            print("Too many redirects")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")

        if response.status_code != 200:
            continue
        print(f'restaurant #{i}, now trying out wolt response')
        wolt_url = wolt_base_url + restaurant["name"].lower().replace(' ', '-')
        wolt_response = requests.get(wolt_url)
        if wolt_response.status_code != 200:
            continue

        # html_content = response.text
        # wolt_content = wolt_response.text
        # restaurant["website_summary"] = get_completion_from_messages(html_content)
        # restaurant["wolt_summary"] = get_completion_from_messages(wolt_content)
        selected_restaurants.append(restaurant)
        # if len(selected_restaurants) > 100:
        #     break



