# CheaPlatzi
Web application that helps the user compare prices of items among different e-commerce sites, and thus find the cheapest offer.

 * **Website:** https://www.gamecheap.store/


## Requirements

**Python 3.x**, any version of **pip**, and **virtualenv**


## Installation

- Clone into a new directory and navigate inside it

- Create a new virtual environment using **virtualenv**

    For example, `virtualenv venv` or   `python3 -m venv venv`



- Activate venv

    For Windows: `.\venv\Scripts\activate` or `.\venv\Scripts\activate.bat` 

    For Unix/Linux: `source venv/bin/activate` or `./venv/bin/activate.sh`

    (Run the `deactivate` command when done with this software's execution)

- Install dependencies

    `pip install -r requirements.txt`


## Testing

To run unit tests on the scraper module, simply run `pytest` at the project's root. However, notice that only one test case can be run at the time due to the implementation of the Spiders. Additional work is still required to enable the execution of all test cases at the same time.


## Execution


### Scraper module

The scraper consumes [MercadoLibre](https://www.mercadolibre.com/)'s API to access Colombia's list of products from the consoles and video games category and shows an example of filtered products (those that match with "Playstation" in their titles); and it uses **scrapy** and **selenium** to formally scrap products of the same category from [OLX Colombia](https://www.olx.com.co/), [ColombiaGamer](https://www.colombiagamer.com.co/), [GamePlanet](https://gameplanet.com), [Sears](https://www.sears.com.mx), and [MixUp](https://www.mixup.com.mx).

To run, use 

On Windows: `python .\scraper\scraper.py --site=<index> [--verbose] [--store]`

On Linux/Unix: `python3 ./scraper/scraper.py --site=<index> [--verbose] [--store]`

The indexes for the sites are:

0. MercadoLibre
1. OLX
2. ColombiaGamer
3. GamePlanet
4. Sears
5. MixUp

The optional `verbose` flag enables to see detailed information about the response bodies from the performed requests to the APIs, and `store` enables the scraper to automatically send requests to the backend's database API to store the scraped records.

### Cheaplatzi API

1. Creates new migration(s) for apps. 
    * `python3 manage.py makemigrations`
2. Updates database schema. Manages both apps with migrations and those without.
    * `python3 manage.py migrate`
3. Starts a lightweight Web server for development and also serves static files.
    * `python3 manage.py runserver`

#### Enpoints

|METHOD|urls|Actions|
|--|--|--|
|POST|api/product|add new product|
|GET|api/product|get all products|
|GET|api/product/:id|get product by id|
|PUT|api/product/:id|Update product by id / Deactivate product by id|
|GET|api/product/active|find all active products|
|GET|api/product?name=[kw]?id_type_product=[kw]?id_ecommerce=[kw]|find all product which name, id_type_product, id_ecommerce contains 'kw'|
|GET|api/product?page|Pagination|
|GET|api/product?country=[kw]|Find all product by country|




