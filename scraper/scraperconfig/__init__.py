import configparser

ini_file_name = "config.ini"
section = "DEFAULT"
config_defaults = {
    'PapAPIKey': '',
    'PostcodeDir': 'data/postal/postcode',
    'DigitsDir': 'data/postal/digits',
    'RestaurantsDir': 'data/restaurants',
    'SearchesDir': 'data/searches',
    'PostcodeOutputFile': 'data/postcodes.json',
    'ProductsOutputFile': 'data/products.json',
}

def setup():
    config = getConfig()

    config_changed = False

    if section not in config:
        config[section] = {}
        config_changed = True

    for key,default_value in config_defaults.items():
        if key not in config[section]:
            config[section][key] = default_value
            config_changed = True

    if config_changed:
        with open(ini_file_name, 'w') as configfile:
          config.write(configfile)

def getConfig():
    config = configparser.ConfigParser()
    config.read(ini_file_name)
    return config

def get(key):
    config = getConfig()

    if section not in config:
        exit("Config not setup correctly, make sure to run setup first")

    if key not in config[section] or not config[section][key]:
        exit(f"Key '{key}' missing value in {ini_file_name}")

    return config[section][key]
