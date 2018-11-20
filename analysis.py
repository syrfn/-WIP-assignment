import pandas as pd

item_food = pd.DataFrame(pd.read_csv('item_food.csv'))
item_food = item_food.dropna()
item_food = item_food[['item_name', 'shop_link']].drop_duplicates() 

# suitable for vegetarian or not?
# yes, it is, because it's veggie
buah = ['buah', 'alpukat', 'jeruk', 'apokat', 'duren', 'jambu', 'stroberi', 'kurma', 'korma', 'durian', 'apel']
sayur = ['beras', 'sayur', 'kol', 'vegetables', 'rumput', 'seed', 'seaweed', 'bean', 'edamame', 'tofu', 'asparagus']
plant = ['sambal', 'chia seed', 'kaldu jamur', 'jamur merang', 'totole', 'jamur', 'herb', 'daun', 'coconut', 'multi grain', 'multigrain', 'corn']
vegan = ['veggie', 'vegan', 'vegetarian', 'veg','organic', 'organik', 'dried', 'manisan', 'sari']
drink = ['coffee', 'tea', 'matcha', 'syrup', 'soy milk', 'susu kedelai']
# suitable for vegetarian or not?
# yes, it is, because it doesn't contain meat / animal product
snack = ['chip', 'keripik', 'kerupuk']

# non vegan: food consisted of meat, meat by-products (gelatin, animal), animal by-products
meat = ['daging', 'meat', 'sapi',  'beef', 'kambing', 'dog', 'pork', 'wagyu']
animal_product = ['susu', 'milk', 'cappuccino', 'latte', 'dairy', 'egg', 'honey', 'nugget', 'bakso', 'madu', 'cheese', 'nugget', 'sosis', 'keju', 'gelatin',  'strudel']
brand = ['ovaltine', 'ovomaltine', 'marshmallow']
poultry = ['duck', 'bebek', 'ayam']
fish = ['ikan', 'fish', 'teri', 'tuna',  'seafood', 'anchovies', 'shrimp', 'squid', 'scallops', 'calamari', 'mussels', 'crab', 'lobster']
bee = ['bee pollen', 'royal jelly', 'honey']
olahan = ['brownies', 'yogurt', 'butter', 'cream', 'ice cream', 'cookies', 'cokelat', 'coklat']
bread = ['brownies', 'cake', 'kue']


def newValue(listArray, newString):
    for item in listArray:
        item_food.loc[item_food['item_name'].str.contains(
            item, case=False, na=False), 'label'] = newString

listArray = [
    (buah, 'veg'),
    (sayur, 'veg'),
    (plant, 'veg'),
    (drink, 'veg'),
    (snack, 'veg'),
    (meat, 'non-veg'),
    (animal_product, 'non-veg'),
    (bee, 'non-veg'),
    (poultry, 'non-veg'),
    (brand, 'non-veg'),
    (olahan, 'non-veg'),
    (bread, 'non-veg'),
    (vegan, 'veg')
]
for item in listArray:
    newValue(*item)

item_food['label'] = item_food['label'].fillna(value='veg')

col = ['shop_link', 'item_name', 'label']

item_food[col].to_csv('makanan-minuman.csv', index=False)
