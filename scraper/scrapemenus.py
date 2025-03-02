import requests
import json
import os
from icecream import ic

title="Scrape menus"

with open("resources/menu-query.json", 'r') as menuQueryFile:
    menuQueryTmpl = json.load(menuQueryFile)

with open("resources/menu-headers.txt", 'r') as headersFile:
    headers = {}
    for line in headersFile:
        split = line.strip().split(':', 1)
        if len(split) > 1:
            header,val = split
            val = val.strip()
            header = header.strip()
            headers[header] = val

def fetchMenu(code, fileName):
    url = f"https://op.fd-api.com/api/v5/vendors/{code}?include=menus"
    ic("fetching", fileName, url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        exit(response.text)

    with open(fileName, "w") as file:
        file.write(response.text)

def main():
    postcodeDirPath = "data/postcode"
    postcodeDir = os.listdir(postcodeDirPath)
    for f in postcodeDir:
        postcodePath = os.path.join(postcodeDirPath, f)
        if os.path.isfile(postcodePath):
            with open(postcodePath, 'r') as postcodeFile:
                postcodeData = json.load(postcodeFile)
                for view in postcodeData['data']['rlp']['organic_listing']['views']:
                    for item in view['items']:
                        code = item['code']
                        restaurantPath = f"data/restaurants/{code}.json"
                        if not os.path.isfile(restaurantPath):
                            fetchMenu(code, restaurantPath)
                        else:
                            ic("Skipping", restaurantPath)

if __name__ == "__main__":
    main()
