# pizza-scraper
Python scripts to scrape data from foodora.se

```
python3 scraper
```
Will give you the following options:
```
Available Options:
1. Search restaurants
2. Scrape menus
3. Fetch postal data
4. Process product data
5. Process postal data
0. Exit
```
### See explanations below:
```
Fetch postal data
```
Fetch postcode data from papapi.se. Creates a file in `data/postal/postcode` for each postcode fetched.

```
Process postal data
```
Transforms data in `data/postal/postcode` into a file containing all postcodes `data/postcodes.json`. 

```
Search restaurants
```
Search restaurants from foodora. Fetches restaurants for each postcode found in `data/postal/postcode` using the coordinates for the postcode. Creates a file containing all found restaurants for a postcode in `data/searches`.

```
Scrape menus
```
Scrape menus for restaurants from foodora. Fetches the menu for each restaurant found in `data/searches` and creates a file in `data/restaurants`.

```
Process product data
```
Process data in `data/restaurants`. Finds each restaurant with a specific product in their menu (from `data/restaurants`) and creates a file `data/products.json`.
