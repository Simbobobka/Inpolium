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
#### Manage goods to scrape

In ```main.py``` there is list that stores all links for goods that should be parsed.

```Python
url_list = [
    ... 
    ]
```
There are some links for test, hovewer you should add more links to be parsed.

#### Project stack

- aiohttp
- asyncio
- csv
- re
- json
- sys
- BeautifulSoup4

All dependencies could be load from ```requirements.txt```

#### Run script
To perform execution simply run ```main.py``` as python file
```python main.py```

#### Project details
If you execute script, all processed data would be saved firstly to intermediate set and after that loaded to ```.csv```. Also note, that links that was used, automaticaly were added to ```progress.json```. It was made to track script progress. If you want test this scripts with the same data, dont forget to leave ```intermediate_data.json``` and ```progress.json``` with empty list []. If you passed this step, script will tell you that that good was already processed.
#### Contact information

- Phone: 093 489 3704
- email: tomashuk.oleg2005@gmail.com
- Telegram: @Simbobobka
