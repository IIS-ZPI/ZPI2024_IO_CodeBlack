import csv
from statistics import median, mode, stdev

import numpy as np
import requests
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

class CurrencyManager:
    def __init__(self):
        self.currencies = ["USD", "EUR", "CHF", "GBP", "JPY", "NOK", "SEK"]

    def show_help(self):
        print("""
    Available commands:
    - fetch-data
    - list-currencies
    - help
    - export
    - session-analysis
    - statistics
    - change-histogram
    - exit
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
        max_days = 93
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid start date or end date")

        if start > end:
            return []

        all_data = []
        current_start = start

        while current_start <= end:
            current_end = min(current_start + timedelta(days=max_days - 1), end)
            url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/{current_start.strftime('%Y-%m-%d')}/{current_end.strftime('%Y-%m-%d')}?format=json"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json().get('rates', [])
                all_data.extend([(entry['effectiveDate'], entry['mid']) for entry in data])
            else:
                print(f"Error fetching data for {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}: {response.status_code}")

            current_start = current_end + timedelta(days=1)

        return all_data

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

    def generate_histogram(self, data, title="Histogram"):
        x_values = [x[0] for x in data]
        y_values = [x[1] for x in data]

        plt.plot(x_values, y_values, marker='o')
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel(f"Value {title[0:7]}")
        plt.grid(True)

        # Limit x-ticks to 5 evenly spaced values
        num_ticks = 5
        tick_indices = np.linspace(0, len(x_values) - 1, num_ticks, dtype=int)
        plt.xticks([x_values[i] for i in tick_indices])

        plt.tight_layout()
        plt.savefig("line_plot.png")
        plt.show()