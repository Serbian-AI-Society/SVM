import argparse
import json

from llm.langchain_llm import get_completion_from_messages


def cli():
    parser = argparse.ArgumentParser(description="LLM Evaluation")
    parser.add_argument(
        "--examples", type=str, required=True, help="Path to the JSON file with examples"
    )
    parser.add_argument(
        "--output-path", type=str, required=True, help="Path to the output JSON file"
    )
    args = parser.parse_args()
    return args


def main():
    args = cli()

    # Load queries from JSON file
    with open(args.examples, "r") as file:
        queries = json.load(file)

    results = []

    # Process each query
    for query in queries:
        try:
            user_message = query["query"]
            response = get_completion_from_messages(user_message)
            results.append(response)
        except Exception as e:
            results.append({"error": str(e)})

    with open(args.output_path, "w") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
