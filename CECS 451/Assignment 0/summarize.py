import argparse
from time import sleep
from google.genai import types, Client
import json
from trafilatura import fetch_url
from bs4 import BeautifulSoup

client = Client(api_key='')
retries = 2


def main():
    parser = argparse.ArgumentParser(description="A script to summarize a website given its URL. Uses Gemini 2.5 Flash")
    parser.add_argument("--url", type=str, help="The url of the website to summarize")
    parser.add_argument("--output", type=str, help='Pass in any value except "print" to have text outputted to output.json', default="print")

    url = parser.parse_args().url
    if url is None:  # somebody forgot to enter an argument
        debug_string = "Please enter a --url argument"
        raise AssertionError(debug_string)

    print("Queryring URl")
    website_text = fetch_url(url)
    for i in range(retries):
        if website_text is None:
            sleep(1)
            print("URL failed to return text, retrying")
            website_text = fetch_url(url)

    if website_text is None:
        debug_string = f"Unable to retrieve text from {url} after {retries + 1} attempts"
        raise ConnectionError(debug_string)

    bs4_text = BeautifulSoup(website_text, 'html.parser')

    prompt = (f'''
    You will be given the text content of the website {url}. Please provide a response in the following format, with no additional text, in at most 1024 tokens:
    
    
    Summary:
        (an indented 3-sentence paragraph summarizing the contents of the website)
    
    Keywords: (at least 5 core keywords/phrases from the website)
    References: (the url of the website)
    
    The website text is as follows:
    {bs4_text.get_text()}''')

    print("Text acquired, querying Gemini")

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=types.Part.from_text(text=prompt),
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024,
            top_p=0.9,
            top_k=40,

        ),
    )

    final_string = f"From URL: {url}\n" + response.text
    output = parser.parse_args().output

    if output == "print":
        print(final_string)
    else:
        with open('output.json', 'w') as file:
            json.dump(final_string + "\n", file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

