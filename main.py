from src.CurrencyManager import CurrencyManager
from datetime import datetime, timedelta
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
        cm.show_available_currencies()


def get_valid_currency_pair(cm) -> tuple[str, str]:
    while True:
        pair = input("Currency pair (e.g. USD/EUR): ").strip().upper()

        if pair.count('/') != 1:
            print("Invalid format. Use exactly one '/' like USD/EUR.")
            continue

        base, quote = pair.split('/')
        if base in cm.currencies and quote in cm.currencies:
            return base, quote

        print("Invalid currencies. Available currencies:")
        cm.show_available_currencies()

def get_valid_currency_and_period(cm):
    currency = get_valid_currency(cm)

    while True:
        period = input("Period (1w, 2w, 1m, 1q, 6m, 1y): ").strip()
        try:
            start, end = cm.get_period_dates(period)
            return currency, start, end
        except ValueError:
            print("Invalid period. Valid options: 1w, 2w, 1m, 1q, 6m, 1y")


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
            currency, start, end = get_valid_currency_and_period(cm)
            data = cm.fetch_data(currency, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            trends = cm.session_analysis(data)
            print(f"Up: {trends['up']}, Down: {trends['down']}, Stable: {trends['stable']}")

        elif command == "statistics":
            currency, start, end = get_valid_currency_and_period(cm)
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
            base, quote = get_valid_currency_pair(cm)
            while True:
                period = input("Period (1m or 1q): ").strip().lower()
                if period not in ["1m", "1q"]:
                    print("Invalid period. Use '1m' for one month or '1q' for one quarter.")
                    continue
                break

            start_date = get_valid_date("Start date")
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                continue
            end_date = start_date + timedelta(days=30 if period == "1m" else 90)

            try:
                base_data = cm.fetch_data(base, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                quote_data = cm.fetch_data(quote, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            except ValueError as e:
                print(f"Data fetch error: {e}")
                continue

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