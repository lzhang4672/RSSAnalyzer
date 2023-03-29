class CSV:
    def csv_reader(csv: str) -> dict[str, Ticker]:
        """Return a mapping of ticker symbols to the Ticker object"""
        with open(csv) as csv_file:
            next(f)
            reader = {ticker[0]: Ticker(ticker[0], ticker[1], ticker[2], int(ticker[3])) for ticker in csv_file}
            return reader

    def csv_add_ticker(csv: str, tickers: dict[str, Ticker]):
        with open(csv, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for symbol, ticker in tickers.items():
                writer.writerow([symbol, ticker])
        return csv

    def csv_modify_ticker(csv: str):

