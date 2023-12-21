import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import utils as ut


class Scraper:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __str__(self):
        return "Web Scraper for Yahoo Finance"
    
    def get_exchange_rate(self, from_symbol: str, to_symbol: str) -> Decimal:
        URL = f"https://finance.yahoo.com/quote/{from_symbol}{to_symbol}=X/"
        source = requests.get(url=URL, headers=self.headers).text
        soup = BeautifulSoup(source, "lxml")

        if from_symbol == "USD": 
            from_symbol = ""

        element = soup.find(
            attrs={
                "data-field": "regularMarketPrice",
                "data-symbol": f"{from_symbol}{to_symbol}=X"
            }
        )

        return Decimal(element.get("value"))
    
    def perform_exchange(self, from_symbol: str, to_symbol: str, amount: float) -> Decimal:
        exc_rate = self.get_exchange_rate(from_symbol, to_symbol)
        return (amount * exc_rate).quantize(Decimal('0.01'))
    

    def scrape_currencies(self) -> dict:
        URL = "https://finance.yahoo.com/currencies/"
        source = requests.get(url=URL, headers=self.headers).text
        soup = BeautifulSoup(source, "lxml")

        curr_data = {}

        section_container = soup.find("section", attrs={'id': 'yfin-list'})
        if section_container:
            for row in section_container.find("tbody").findAll("tr"):
                name = row.find("td", attrs={"aria-label": "Name"}).text
                from_curr, to_curr = name.split("/")
                last_price = ut.float_formatter(
                    row.find("td", attrs={"aria-label": "Last Price"}).text
                )

                if from_curr in curr_data:
                    curr_data[from_curr][to_curr] = last_price

                else:
                    curr_data[from_curr] = {to_curr: last_price}

        return curr_data
    
    def scrape_world_indices(self):
        URL = "https://finance.yahoo.com/world-indices/"
        source = requests.get(url=URL, headers=self.headers).text
        soup = BeautifulSoup(source, "lxml")

        indices_data = {}

        section_container = soup.find("section", attrs={'id': 'yfin-list'})
        if section_container:
            for row in section_container.find("tbody").findAll("tr"):

                symbol = row.find("td", attrs={"aria-label": "Symbol"}).text
                name = row.find("td", attrs={"aria-label": "Name"}).text

                last_price = ut.float_formatter(
                    row.find("td", attrs={"aria-label": "Last Price"}).text
                )

                change = row.find("td", attrs={"aria-label": "Change"}).text
                change_type = "positive" if  "+" in change else "negative"
                change = ut.float_formatter(change)

                perc_change = ut.float_formatter(
                    row.find("td", attrs={"aria-label": "% Change"}).text
                )

                indices_data[symbol] ={
                    "name": name,
                    "last_price": last_price,
                    "change": change,
                    "perc_change": perc_change,
                    "change_type": change_type
                }


        return indices_data
    



    