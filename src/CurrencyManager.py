import csv
from statistics import median, mode, stdev

import requests
from datetime import datetime, timedelta



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

    def get_period_dates(self, period):
        today = datetime.today()
        if period == "1w":
            return today - timedelta(weeks=1), today
        elif period == "2w":
            return today - timedelta(weeks=2), today
        elif period == "1m":
            return today - timedelta(days=30), today
        elif period == "1q":
            return today - timedelta(days=90), today
        elif period == "6m":
            return today - timedelta(days=180), today
        elif period == "1y":
            return today - timedelta(days=365), today
        else:
            raise ValueError("Invalid period")

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

    def session_analysis(self, data):
        trends = {"up": 0, "down": 0, "stable": 0}
        for i in range(1, len(data)):
            diff = round(data[i][1] - data[i-1][1], 4)
            if diff > 0:
                trends["up"] += 1
            elif diff < 0:
                trends["down"] += 1
            else:
                trends["stable"] += 1
        return trends

    def compute_statistics(self, data):
        values = [x[1] for x in data]
        if len(values) < 2:
            return {}
        return {
            "median": median(values),
            "mode": mode(values),
            "std_dev": stdev(values),
            "cv": round(stdev(values) / (sum(values) / len(values)) * 100, 2)
        }