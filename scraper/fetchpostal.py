import requests
import json
import os
from icecream import ic
import scraperconfig

title = "Fetch postal data"

def request(query, key):
    ic("fetching", query)
    url = f"https://api.papapi.se/lite/?query={query}&format=json&apikey={key}"
    inputRequest = requests.get(url)
    if inputRequest.status_code != 200:
        if inputRequest.status_code == 404:
            ic(query, "Not Found:", inputRequest.status_code, inputRequest.text)
            return "{}"
        ic("ERROR IN CALL TO PAPI:", inputRequest.status_code, inputRequest.text)
        exit()

    return inputRequest.text

def main():

    digits_dir = scraperconfig.get('DigitsDir')
    if not os.path.exists(digits_dir):
        os.makedirs(digits_dir)

    postcode_dir = scraperconfig.get('PostcodeDir')
    if not os.path.exists(postcode_dir):
        os.makedirs(postcode_dir)

    papiKey = scraperconfig.get('PapAPIKey')

    for i in range(100, 996):
        digit_path = f"{digits_dir}/{i}.json"
        if os.path.isfile(digit_path):
            continue

        response = json.loads(request(i, papiKey))

        with open(digit_path, "w") as file:
            json.dump(response, file, ensure_ascii=False, indent=2)

        if 'results' in response:
            for postcode_data in response['results']:
                postcode_path = f"{postcode_dir}/{postcode_data['postal_code']}.json"
                if os.path.isfile(postcode_path):
                    continue

                with open(postcode_path, "w") as file:
                    json.dump(postcode_data, file, ensure_ascii=False, indent=2)
                    ic("Created file", postcode_path)


if __name__ == "__main__":
    main()
