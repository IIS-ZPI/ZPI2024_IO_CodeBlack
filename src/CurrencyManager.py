import csv

class CurrencyManager:
    def __init__(self):
        pass

    def display_help(self):
        """Print available commands and their usage"""
        pass

    def show_available_currencies(self):
        """Display a list of supported currency codes"""
        pass

    def fetch_data(self, currency: str, start_date: str, end_date: str):
        """Fetch currency data from API"""
        pass

    def export_to_csv(self, data, filename="output.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Exchange Rate"])
            writer.writerows(data)
        print(f"Data exported to {filename}")