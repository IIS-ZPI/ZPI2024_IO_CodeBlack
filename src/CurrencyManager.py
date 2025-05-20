import csv
import requests


class CurrencyManager:
    def __init__(self):
        self.currencies = ["USD", "EUR", "CHF", "GBP", "JPY", "NOK", "SEK"]

    def show_help(self):
        print("""
        Available commands:
        - fetch-data <currency> <start-date> <end-date>
        - list-currencies
        - help
        - export csv
        """)

    def show_available_currencies(self):
        print("Available currencies:")
        for c in self.currencies:
            print("-", c)

    def fetch_data(self, currency: str, start_date: str, end_date: str):
        url = f"https://api.nbp.pl//api//exchangerates//rates//A//{currency}//{start_date}//{end_date}//?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['rates']
            return [(entry['effectiveDate'], entry['mid']) for entry in data]
        else:
            print("Error fetching data:", response.status_code)
            return []

    def export_to_csv(self, data, filename="output.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Exchange Rate"])
            writer.writerows(data)
        print(f"Data exported to {filename}")
