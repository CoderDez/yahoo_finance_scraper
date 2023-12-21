import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import utils as ut


class YahooFinanceScraper:
    """
    A class for scraping data from various finance-related web pages on Yahoo Finance.

    Methods:
    - __init__: Initializes the Scraper class with default headers for requests.
    - get_exchange_rate: Gets the exchange rate from one currency to another.
    - perform_exchange: Performs an exchange between two currencies.
    - scrape_currencies: Scrapes the Yahoo Finance currency page.
    - scrape_world_indices: Scrapes the Yahoo Finance world indices page.
    - scrape_crypto: Scrapes the Yahoo Finance crypto page.
    - get_soup: Fetches HTML content from a given URL and creates a BeautifulSoup object.
    """
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __str__(self):
        return "Web Scraper for Yahoo Finance"
    
    def get_soup(self, url: str):
        """
        Fetches HTML content from a given URL and creates a BeautifulSoup object.

        Args:
        - url (str): The URL of the web page to fetch.

        Returns:
        - BeautifulSoup: A BeautifulSoup object representing the parsed HTML content of the web page.
        """
        source = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(source, "lxml")
        return soup
    
    def get_exchange_rate(self, from_symbol: str, to_symbol: str) -> Decimal:
        """
        Gets the exchange rate from one currency to another.

        Args:
        - from_symbol (str): The symbol of the currency to convert from.
        - to_symbol (str): The symbol of the currency to convert to.

        Returns:
        - Decimal: The exchange rate in Decimal format.
        """
        try:
            soup = self.get_soup(f"https://finance.yahoo.com/quote/{from_symbol}{to_symbol}=X/")

            if from_symbol == "USD": 
                from_symbol = ""

            element = soup.find(
                attrs={
                    "data-field": "regularMarketPrice",
                    "data-symbol": f"{from_symbol}{to_symbol}=X"
                }
            )

            return Decimal(element.get("value"))
            
        except Exception as e:
            print("ERROR occurred while getting exchange rate: ", e)
    
    def perform_exchange(self, from_symbol: str, to_symbol: str, amount: float) -> Decimal:
        """
        Performs an exchange between two currencies.

        Args:
        - from_symbol (str): The symbol of the currency to convert from.
        - to_symbol (str): The symbol of the currency to convert to.
        - amount (float): The amount of currency to convert.

        Returns:
        - Decimal: The converted amount after performing the exchange.
        """
        try:
            exc_rate = self.get_exchange_rate(from_symbol, to_symbol)
            return (amount * exc_rate).quantize(Decimal('0.01'))
        
        except Exception as e:
            print("ERROR occurred while performing exchange: ", e)
        
    def scrape_currencies(self) -> dict:
        """
        Scrapes the Yahoo Finance currency page.

        Returns a dictionary of currency exchange rates.
        """
        try:
            soup = self.get_soup("https://finance.yahoo.com/currencies/")

            curr_data = {}

            section_container = soup.find("section", attrs={'id': 'yfin-list'})

            if section_container:

                for row in section_container.find("tbody").findAll("tr"):

                    name = row.find("td", attrs={"aria-label": "Name"}).text
                    from_curr, to_curr = name.split("/")
                    last_price = ut.float_formatter(row.find("td", attrs={"aria-label": "Last Price"}).text)

                    if from_curr in curr_data:
                        curr_data[from_curr][to_curr] = last_price

                    else:
                        curr_data[from_curr] = {to_curr: last_price}

            return curr_data
        
        except Exception as e:
            print("ERROR occurred while scraping currencies: ", e)
    
    def scrape_world_indices(self) -> dict:
        """
        Scrapes the Yahoo Finance world indices page.

        Returns:
        - dict: World indices data in the format {symbol: {details}}
        """
        try:
            soup = self.get_soup("https://finance.yahoo.com/world-indices/")
 
            indices_data = {}

            section_container = soup.find("section", attrs={'id': 'yfin-list'})

            if section_container:

                for row in section_container.find("tbody").findAll("tr"):

                    symbol = row.find("td", attrs={"aria-label": "Symbol"}).text
                    name = row.find("td", attrs={"aria-label": "Name"}).text

                    last_price = ut.float_formatter(row.find("td", attrs={"aria-label": "Last Price"}).text)

                    change = row.find("td", attrs={"aria-label": "Change"}).text
                    change_type = "positive" if  "+" in change else "negative"
                    change = ut.float_formatter(change)

                    perc_change = ut.float_formatter(row.find("td", attrs={"aria-label": "% Change"}).text)

                    indices_data[symbol] ={
                        "name": name,
                        "last_price": last_price,
                        "change": change,
                        "perc_change": perc_change,
                        "change_type": change_type
                    }


            return indices_data
    
        except Exception as e:
            print("ERROR ocurred while scraping world indices: ", e)
        
    def scrape_crypto(self):
        """
        Scrapes the Yahoo Finance crypto page.

        Returns a dictionary of cryptocurrency data.
        """
        try:
            soup = self.get_soup("https://finance.yahoo.com/crypto/")

            crypto_data = {}

            section_container = soup.find("section", attrs={'id': 'screener-results'})

            if section_container:

                for row in section_container.find("tbody").findAll("tr"):

                    symbol = row.find("td", attrs={"aria-label": "Symbol"}).text
                    name = row.find("td", attrs={"aria-label": "Name"}).text

                    last_price = ut.float_formatter(row.find("td", attrs={"aria-label": "Price (Intraday)"}).text)

                    change = row.find("td", attrs={"aria-label": "Change"}).text
                    change_type = "positive" if  "+" in change else "negative"
                    change = ut.float_formatter(change)

                    perc_change = ut.float_formatter(row.find("td", attrs={"aria-label": "% Change"}).text)

                    market_cap = row.find("td", attrs={"aria-label": "Market Cap"}).text


                    crypto_data[symbol] ={
                        "name": name,
                        "last_price": last_price,
                        "change": change,
                        "perc_change": perc_change,
                        "change_type": change_type,
                        "market_cap": market_cap
                    }


            return crypto_data
        
        except Exception as e:
            print("ERROR occurred while scraping crypto: ", e)


s = YahooFinanceScraper()
