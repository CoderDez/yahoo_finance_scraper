import requests
from bs4 import BeautifulSoup
from decimal import Decimal


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

        data = {}

        section_container = soup.find("section", attrs={'id': 'yfin-list'})
        if section_container:
            for row in section_container.find("tbody").findAll("tr"):
                name = row.find("td", attrs={"aria-label": "Name"}).text
                from_curr, to_curr = name.split("/")
                last_price = row.find("td", attrs={"aria-label": "Last Price"}).text
                last_price = float(last_price.replace(",", ""))

                if from_curr in data:
                    data[from_curr][to_curr] = last_price

                else:
                    data[from_curr] = {to_curr: last_price}

        return data



    