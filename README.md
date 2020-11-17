# Amazon Scraper
This is a simple scraper for www.amazon.com

## Usage

Make sure you have Python 3.6 or newer installed.

Requires an argument from the CLI (it will be used as a search parameter).

You must pip install both `Selenium` and `xlsxwriter`.

    $ pip install -r requirements.txt

Firefox's `Geckodriver` also needs to be downloaded and added to PATH if running on windows
or installed via CLI on Linux.

To run the script in a docker container you must do the following:

    docker build -t <name> <location of Dockerfile>
    docker run -it <name> <search parameter>

In this case, Firefox must be ran in headless mode.

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
```

### Running the code

    $ python amazon_search.py IPhone

## The Program

Amazon scraper performs a search on www.amazon.com and returns all first page results in both .csv and .xlsx formats.

This requires a CLI argument as parameter which will be used as both the searched product and for naming the files.

The files will be named as InsertInputHere_results.extension and will work for any item, except for special cases such as songs, videos or books(basically anything that Amazon has a specific service for, since the site redirects you elsewhere).
