class CurrencyManager:
    def __init__(self):
        pass

    def show_help(self):
        print("""
        Available commands:
        - fetch-data <currency> <start-date> <end-date>
        - list-currencies
        - help
        - export csv
        """)

    def show_available_currencies(self):
        """Display a list of supported currency codes"""
        pass

    def fetch_data(self, currency: str, start_date: str, end_date: str):
        """Fetch currency data from API"""
        pass

    def export_to_csv(self, data, filename="output.csv"):
        """Export fetched data to a CSV file"""
        pass