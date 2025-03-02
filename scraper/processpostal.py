import os
import json
from icecream import ic
import scraperconfig

title = "Process postal data"

def main():
    postcode_dir = scraperconfig.get('PostcodeDir')
    output_file_path = scraperconfig.get('PostcodeOutputFile')

    entries = {}
    for postcode_file_name in os.listdir(postcode_dir):
        postcode_path = os.path.join(postcode_dir, postcode_file_name)
        if os.path.isfile(postcode_path):
            with open(postcode_path, 'r') as postcode_file:
                postcode_data = json.load(postcode_file)
                entries[postcode_data['postal_code']] = postcode_data

    with open(output_file_path, 'w') as output_file:
        json.dump(list(entries.values()), output_file, ensure_ascii=False, indent=2)
        ic("Created file: ", output_file_path)

if __name__ == "__main__":
    main()
