# Scraping goods from the site

#### Quick start
Install all dependencies from  ```requirements.txt```
```pip install -r requirements.txt```
Execute ```python main.py``` to run script.
As a result there will be ```.csv``` created and some intermediate files.
#### Project setup
This project uses `venv` for managing dependencies. Follow these steps to install set up the project.
- Clone this repository
- Perform  ```pip install -r requirements.txt```

After this, all required libraries would be installed.

__NOTE:__ you should better use also ```venv``` or ```pipenv``` for managing all dependencies. Create your own environment before loading all content from ```requirements.txt```.

#### Project stack

- aiohttp
- asyncio
- csv
- re
- json
- BeautifulSoup4

All dependencies could be load from ```requirements.txt```

#### Run script
To perform execution simply run ```main.py``` as python file
```python main.py```

#### Project details
If you execute script, all processed data would be saved firstly to intermediate set and after that loaded to ```.csv```. Also note, that links that was used, automaticaly were added to ```progress.json```. It was made to track script progress. If you want test this scripts with the same data, dont forget to leave ```intermediate_data.json``` and ```progress.json``` with empty list []. If you passed this step, script will tell you that that good was already processed. Note, it scrape all goods from site and it take a lot of time, so if you want to see result interrupt to process by ```ctrl + c```.

In ternimal you could see all pages and goods that were processed.
Example:
```
Fetching product URLs from page 1
Successfully scraped https://store.igefa.de/p/clean-and-clever-smartline-muellbeutel-sma-73-460-mm-x-520-mm-18-l/AHgJ4WmdVM7tj6K7eknSSo
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-spezialreiniger-fuer-milchaufschaeumer-pro-136-fuer-milchaufschaeumer/qaXRdcxhmq2eSHAsBGCuR7
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-sanitaergrundreiniger-pro-84-pro84-sanitaergrundreiniger-1l/as6vGdQ2ooJ7hXcYHZRcB3
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-muellbeutel-pro-74-30-l-500-mm-x-600-mm/RkqzsVZDy6yDN6aqEHMzPR
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-muellbeutel-pro-73-30-l-500-mm-x-600-mm/ZEEwXq7SytBU5TNgwPfSck
Successfully scraped https://store.igefa.de/p/clean-and-clever-smartline-muellbeutel-sma-74-500-mm-x-600-mm-30-l/kaZkJWyizg65Xtw84gxWqh
Successfully scraped https://store.igefa.de/p/clean-and-clever-smartline-alkoholreiniger-sma-2-sma2-alkoholreiniger-10l/H6KnHW22UBxrZHKQzCLGZP
Successfully scraped https://store.igefa.de/p/clean-and-clever-smartline-muellbeutel-sma-74-460-mm-x-520-mm-18-l/tUSPHwCgjDx8bs7n7ugZze
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-wischtuchrolle-pro-252-industrie-putztuchrolle-blau/tyW6Q63MdgbaTyoGufoGFW
Successfully scraped https://store.igefa.de/p/clean-and-clever-pro-kuechenrolle-pro-68-pro68-kuechenrolle-hochweiss-3lg/3SSzd4x6skjLP4jbswdxGF
Successfully scraped https://store.igefa.de/p/clean-and-clever-smartline-muellbeutel-sma-73-500-mm-x-600-mm-30-l/5wse8XLBipTfGktnhqbytV

Program interrupted! Flushing intermediate data to CSV...
```
#### Contact information

- Phone: 093 489 3704
- email: tomashuk.oleg2005@gmail.com
- Telegram: @Simbobobka
