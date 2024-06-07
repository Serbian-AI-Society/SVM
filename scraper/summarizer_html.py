from openai import OpenAI


def summarize_html(user_message, model="gpt-4o") -> str:
    system_prompt = """You are a helpful assistant that can provide a summary about the restaurant
    based on it's HTML home page information about restaurants html page. Try to extract
    information such as type of the restaurant, what kind of food they serve etc.
    Write a summary in three sentences on Serbian language."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_message}"},
    ]

    client = OpenAI()

    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content


if __name__ == "__main__":
    # read a txt file content
    with open("scraper/data/restaurant.txt", "r") as file:
        user_message = file.read()
    print(summarize_html(user_message))
