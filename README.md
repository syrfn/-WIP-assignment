# Vegan or Non-Vegan Products?
This script consists of two parts. The first script to extract data with the URL (https://www.tokopedia.com/p/makanan-minuman). The goal is to get food and beverages data (items, links). The second script to classify whether each item is suitable for vegan or not.

## How to Collect The Data
This is dynamic web and use JavaScript to load the content. This website require a different approach to collect the data. So, the method to collect the data is scrape a webpage rendered by JavaScript using Selenium module with a headless Chrome.

**Why Selenium?**\
Selenium allows to open a web browser, navigate a webpage, return the page's inner HTML (scrape the data needed) using Python.\
\
**Why headless Chrome?**\
Headless Chrome doesn't launch user interface (no browser visibly launched). Headless browsers are faster and running headless tests is quicker for developers.\

## How it works?
Following steps describe how `final.py` actually works to collect the data from link above. \
**Step 1**\
Scrape this page https://www.tokopedia.com/p/makanan-minuman to get category URL, save the result to array list.
```
['https://www.tokopedia.com/p/makanan-minuman/biskuit-kue',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-beku',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-manis',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-kering',
 'https://www.tokopedia.com/p/makanan-minuman/minuman',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-minuman-kesehatan',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-siap-saji',
 'https://www.tokopedia.com/p/makanan-minuman/bumbu-bahan-dasar',
 'https://www.tokopedia.com/p/makanan-minuman/lainnya']
```

**Step 2**\
Each category has pages. From the result above, generate manually to get specific url (each category with pages) and save to an array list.
Following are the result.
```
['https://www.tokopedia.com/p/makanan-minuman/biskuit-kue?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-beku?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-manis?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-kering?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/minuman?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-minuman-kesehatan?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-siap-saji?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/bumbu-bahan-dasar?page=1',
 'https://www.tokopedia.com/p/makanan-minuman/lainnya?page=1',
 '...',
 '...',
 '...',
 '...',
 'https://www.tokopedia.com/p/makanan-minuman/biskuit-kue?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-beku?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-manis?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-kering?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/minuman?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-minuman-kesehatan?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/makanan-siap-saji?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/bumbu-bahan-dasar?page=90',
 'https://www.tokopedia.com/p/makanan-minuman/lainnya?page=90'
 ]
```

**Step 3**\
After that iterate over the array list to extract item name and shop URL and save the data to a file.

## How to Classify The Product
This is just a simple classification. There's no algorithm nor machine learning model on it as given only item name and shop URL. The question is "can vegan eat this item?". The assumption applies here is a vegan only can eat food with no animal content in it. So, in the script `analysis.py`, every item_name is checked by `str.contains()` function to see whether it contains non-vegan words or not. And the rest of it is vegan item. 
