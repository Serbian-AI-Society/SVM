import requests
import json
import os
from summarizer_html import summarize_html
from summarizer_wolt import summarize_wolt
from summarizer_reviews import summarize_reviews
import openai
from bs4 import BeautifulSoup


def remove_html_tags(html_string):
    # Parse the HTML content
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Extract the text without HTML tags
    text = soup.get_text(separator="\n", strip=True)
    
    return text


if __name__ == "__main__":
    data_path = 'scraper/data/'
    with open(data_path + 'final_restaurants_and_bars.json', 'r') as fp:
        restaurants_and_bars = json.load(fp)

    wolt_base_url = "https://wolt.com/en/geo/batumi/restaurant/"

    restaurants_with_website = [place for place in restaurants_and_bars if ('restaurant' in place["types"]) and place["website"]]
    print("Total restaurants with website: ", len(restaurants_with_website))
    selected_restaurants = []
    for i, restaurant in enumerate(restaurants_with_website):
        try:
            # Checking website response
            print(f"#{i} working on restaurant {restaurant['website']} ")
            response = requests.get(restaurant["website"], timeout=10)
            if response.status_code != 200:
                print(f'#{i} website response failed {restaurant["website"]}, response code: {response.status_code}')
                continue

            # Checking wolt response
            wolt_url = wolt_base_url + restaurant["name"].lower().replace(' ', '-')
            print(f'#{i} working on wolt response {wolt_url}')
            wolt_response = requests.get(wolt_url)
            if wolt_response.status_code != 200:
                print(f'#{i} wolt response failed {wolt_url}, response code: {wolt_response.status_code}')
                continue
            
            # Get the summary from the website
            restaurant["website_summary"] = summarize_html(remove_html_tags(response.text))
            restaurant["wolt_summary"] = summarize_wolt(remove_html_tags(wolt_response.text))
            restaurant["reviews"] = summarize_reviews(restaurant["reviews"])
            selected_restaurants.append(restaurant)
            print(f"Restaurant {restaurant['name']} saved successfully, size: {len(selected_restaurants)}")

            # Number of restaurants to be saved
            if len(selected_restaurants) > 100:
                break
        except requests.ConnectionError as e:
            print("Connection unavailable")
            continue
        except requests.Timeout as e:
            print("Connection timed out")
            continue
        except requests.exceptions.TooManyRedirects as e:
            print("Too many redirects")
            continue
        except requests.RequestException as e:
            print("Default request exception occurred")
            continue
        except openai.RateLimitError as e:
            print("Rate limit error occurred: " + str(e))
            continue

    with open(data_path + 'selected_restaurants.json', 'w') as fp:
        json.dump(selected_restaurants, fp, indent=4)
