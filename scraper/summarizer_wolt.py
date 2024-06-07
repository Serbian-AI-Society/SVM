from openai import OpenAI


def summarize_wolt(user_message, model="gpt-4o") -> str:
    system_prompt = """You are a helpful assistant that can provide a summary about the
    restaurant's menu based of the HTML page of the website for food delivery.
    Look for typical dishes, drinks, prices, and other relevant information.
    Write a summary in a couple of sentences in Serbian language."""
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
    print(summarize_wolt(user_message))
