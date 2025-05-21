from src.CurrencyManager import CurrencyManager
from datetime import datetime, timedelta
from datetime import datetime

def get_valid_date(prompt: str) -> str:
    while True:
        date_input = input(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format or date. Please use YYYY-MM-DD.")

def get_valid_currency(cm) -> str:
    while True:
        currency = input("Currency (e.g. USD): ").strip().upper()
        if currency in cm.currencies:
            return currency
        print("Invalid currency.")
        print("Available currencies:")
        cm.show_available_currencies()


def main():
    cm = CurrencyManager()
    while True:
        command = input("Enter command: ").strip()

        if command == "exit":
            print("Exiting application.")
            break

        elif command == "list-currencies":
            cm.show_available_currencies()


        elif command == "fetch-data":
            currency = get_valid_currency(cm)
            start_date = get_valid_date("Start date")
            end_date = get_valid_date("End date")

            try:
                data = cm.fetch_data(currency, start_date, end_date)
                for row in data:
                    print(row)
            except ValueError as e:
                print(f"Error fetching data: {e}")

        elif command == "session-analysis":
            currency = input("Currency (e.g. EUR): ").strip().upper()
            period = input("Period (1w, 2w, 1m, 1q, 6m, 1y): ").strip()
            start, end = cm.get_period_dates(period)
            data = cm.fetch_data(currency, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            trends = cm.session_analysis(data)
            print(f"Up: {trends['up']}, Down: {trends['down']}, Stable: {trends['stable']}")

        elif command == "statistics":
            currency = input("Currency (e.g. CHF): ").strip().upper()
            period = input("Period (1w, 2w, 1m, 1q, 6m, 1y): ").strip()
            start, end = cm.get_period_dates(period)
            data = cm.fetch_data(currency, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            stats = cm.compute_statistics(data)
            for k, v in stats.items():
                print(f"{k}: {v}")

        elif command == "export":
            format_type = input("Export format (csv): ").strip()
            if format_type == "csv":
                currency = input("Currency (e.g. USD): ").strip().upper()
                start = input("Start date (YYYY-MM-DD): ").strip()
                end = input("End date (YYYY-MM-DD): ").strip()
                data = cm.fetch_data(currency, start, end)
                cm.export_to_csv(data)
            else:
                print("Unsupported export format.")

        elif command == "change-histogram":
            pair = input("Currency pair (e.g. USD/EUR): ").strip().upper()
            if '/' not in pair:
                print("Invalid format. Use USD/EUR.")
                continue
            base, quote = pair.split('/')
            period = input("Period (1m or 1q): ").strip()
            start_str = input("Start date (YYYY-MM-DD): ").strip()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                continue
            end = start_date + timedelta(days=30 if period == "1m" else 90)
            base_data = cm.fetch_data(base, start_date.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            quote_data = cm.fetch_data(quote, start_date.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            if len(base_data) != len(quote_data):
                print("Mismatch in data length. Cannot build histogram.")
                continue
            rel_data = []
            for i in range(len(base_data)):
                date = base_data[i][0]
                rate = base_data[i][1] / quote_data[i][1]
                rel_data.append((date, rate))
            cm.generate_histogram(rel_data, f"{base}/{quote} Histogram")

        elif command == "help":
            cm.show_help()

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()