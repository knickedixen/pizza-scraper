import requests
from copy import deepcopy
import json
import os
from icecream import ic
import time
import scraperconfig

title="Search restaurants"

with open("resources/list-query.json", 'r') as pizzaQueryFile:
    listQueryTmpl = json.load(pizzaQueryFile)

with open("resources/list-headers.txt", 'r') as headersFile:
    headers = {}
    for line in headersFile:
        split = line.strip().split(':', 1)
        if len(split) > 1:
            header,val = split
            val = val.strip()
            header = header.strip()
            headers[header] = val

def search(lat, long):
    url = "https://op.fd-api.com/rlp-service/query"
    query = deepcopy(listQueryTmpl)
    query['variables']['input']['latitude'] = lat
    query['variables']['input']['longitude'] = long

    response = requests.post(url, json.dumps(query), headers=headers)

    if response.status_code != 200:
        ic(response)
        ic(response.text)
        exit()

    return response.text

def main():
    searches_dir = scraperconfig.get("SearchesDir")
    postcode_dir_path = scraperconfig.get("PostcodeDir")

    postcode_files = os.listdir(postcode_dir_path)
    postcodes_length = len(postcode_files)
    calls = 0
    for i, postcode_file in enumerate(postcode_files):
        ic(i, postcodes_length, postcode_file)

        postcode_path = os.path.join(postcode_dir_path, postcode_file)
        if not os.path.isfile(postcode_path):
            continue

        with open(postcode_path, 'r') as file:
            postalInfo = json.load(file)

            search_file_name = f"{searches_dir}/{postalInfo['postal_code']}.json"
            if os.path.isfile(search_file_name):
                continue

            if calls % 5 == 0:
                # Sleeping seems to help against captcha
                ic(time.sleep(5))

            response = search(float(postalInfo['latitude']), float(postalInfo['longitude']))
            calls += 1

            with open(search_file_name, "w") as file:
                file.write(response)

if __name__ == "__main__":
    main()
