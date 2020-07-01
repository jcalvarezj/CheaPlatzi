# CheaPlatzi
Web application that retrieves the cheapest item among different e-commerce sites

## Requirements

**Python 3.x**, any version of **pip**, and **virtualenv**


## Installation

- Clone into a new directory and navigate inside it

- Create a new virtual environment using **virtualenv**

    For example, `virtualenv venv`

- Activate venv

    For Windows: `.\venv\Scripts\activate` or `.\venv\Scripts\activate.bat` 

    For Unix/Linux: `source venv/bin/activate` or `./venv/bin/activate.sh`

    (Run the `deactivate` command when done with this software's execution)

- Install dependencies

    `pip install -r requirements.txt`


## Execution

At present only the "scraper" module has been implemented (an initial draft/approach). It consumes [MercadoLibre](https://www.mercadolibre.com/)'s API to access Colombia's list of products from the consoles and video games category and shows an example of filtered products (those that match with "Playstation" in their titles).

To run, use `python .\scraper\scraper.py` on Windows and `python3 ./scraper/scraper.py` on Linux/Unix