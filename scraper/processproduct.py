import os
import json

from icecream import ic
import scraperconfig

title = "Process product data"

def findVariant(variants):
    res = False
    for variant in variants:
        name = variant['name'] if 'name' in variant else "" 
        price = variant['price']
        if 'price_before_discount' in variant:
            price = variant['price_before_discount']

        current = { "price":price, "name":name }
        if not res or res['price'] > price:
            res = current

        if name.lower() in ['standard', 'normal']:
            res = current
            break

    return res

def findproduct(menus, name):
    res = False
    for menu in menus:
        for category in menu['menu_categories']:
            if "barn" in category['name'].lower():
                continue
            for product in category['products']:
                nameLwr = product['name'].lower().replace(" ", '')
                if name in nameLwr and not ("+" in nameLwr or "plus" in nameLwr):
                    variant = findVariant(product['product_variations'])
                    if variant and (not res or res['price'] > variant['price']):
                        res = {
                            "product": product['name'],
                            "price": variant['price'],
                            "variant": variant['name'],
                        }
    return res

def main():
    productName = "vesuvio"

    output_file_path = scraperconfig.get("productsoutputfile")
    restaurantsDirPath = scraperconfig.get("restaurantsdir")
    postcode_dir_path = scraperconfig.get("postcodedir")

    resautrantsDir = os.listdir(restaurantsDirPath)
    products = []
    for f in resautrantsDir:
        restaurantPath = os.path.join(restaurantsDirPath, f)
        if os.path.isfile(restaurantPath):
            with open(restaurantPath, 'r') as restaurantFile:
                restaurantData = json.load(restaurantFile)['data']
                product = findproduct(restaurantData['menus'], productName)
                if product:
                    postcode = restaurantData['post_code'].replace(" ",'');
                    product["restaurant"] = restaurantData['name'] 
                    product["postcode"] =  postcode
                    product["latitude"] = restaurantData['latitude']
                    product["longitude"] = restaurantData['longitude']
                    product["code"] = restaurantData['code']
                    product["city"] = restaurantData['city']['name']
                    product["county_code"] = ""
                    product["county"] = ""
                    product["state_code"] = ""
                    product["state"] = ""
                    postcode_file_path = postcode_dir_path + "/" + postcode + ".json"
                    if os.path.isfile(postcode_file_path):
                        with open(postcode_file_path, 'r') as postcode_file:
                            postcode_data = json.load(postcode_file)
                            product["county_code"] = postcode_data['county_code']
                            product["county"] = postcode_data['county']
                            product["state_code"] = postcode_data['state_code']
                            product["state"] = postcode_data['state']
                    products.append(product)

    with open(output_file_path, "w") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)
        ic("Created file: ", output_file_path)

if __name__ == "__main__":
    main()
