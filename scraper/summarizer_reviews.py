from openai import OpenAI


def summarize_reviews(user_message, model="gpt-4o") -> str:
    system_prompt = """You are a helpful assistant that can provide a summary about the
    restaurant's reviews on google maps.
    Write a summary of what people say about the restaurant in a couple of sentences
    in Serbian language."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_message}"},
    ]

    client = OpenAI()

    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content


if __name__ == "__main__":
    # read a txt file content
    with open("scraper/data/reviews.txt", "r") as file:
        user_message = file.read()
    print(summarize_reviews(user_message))
