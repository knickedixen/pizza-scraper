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

    output_file_path = scraperconfig.get("ProductsOutputFile")
    restaurantsDirPath = scraperconfig.get("RestaurantsDir")
    
    resautrantsDir = os.listdir(restaurantsDirPath)
    products = []
    for f in resautrantsDir:
        restaurantPath = os.path.join(restaurantsDirPath, f)
        if os.path.isfile(restaurantPath):
            with open(restaurantPath, 'r') as restaurantFile:
                restaurantData = json.load(restaurantFile)['data']
                product = findproduct(restaurantData['menus'], productName)
                if product:
                    product["restaurant"] = restaurantData['name'] 
                    product["postcode"] = restaurantData['post_code'].replace(" ",'') 
                    product["latitude"] = restaurantData['latitude']
                    product["longitude"] = restaurantData['longitude']
                    product["code"] = restaurantData['code']
                    product["city"] = restaurantData['city']['name']
                    products.append(product)

    with open(output_file_path, "w") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)
        ic("Created file: ", output_file_path)

if __name__ == "__main__":
    main()
