# Stock Portfolio Manager

A simple command-line **Stock Portfolio Tracker** written in Python. Add stocks by ticker symbol and quantity, and it calculates the total value of your investment from a set of predefined stock prices. You can also save your portfolio summary to a `.csv` or `.txt` file.

> **Note:** Stock prices are **hardcoded example prices** (see `portfolio.py` → `STOCK_PRICES`), not live market data. The tracker works fully offline and is intended as a learning project and a starting point you can extend with a live price API later.

## Features

- Add stocks by symbol and quantity (e.g. `AAPL`, `10`)
- Remove a whole holding, or just some of its shares
- View your portfolio with per-stock value and total investment value
- View the list of supported stocks and their prices
- Save the portfolio summary as a CSV or a plain-text file
- Clean, structured code with no third-party dependencies

## Project Structure

```text
StockPortfolio_Project/
├── portfolio.py      # Main program: portfolio logic + command-line interface
├── README.md         # This file
├── requirements.txt  # Dependencies (none beyond the Python standard library)
└── .gitignore        # Files Git should ignore (caches, virtual envs, OS files, outputs)
```

## Requirements

- Python 3.8 or newer (3.10+ recommended; the code uses `X | None` type hints)
- No third-party packages are required

Check your Python version with:

```bash
python --version
```

## Setup

Clone the repository (or download and unzip this project), then move into the project folder:

```bash
git clone <your-repo-url>
cd StockPortfolio_Project
```

There is nothing to install. If you want an isolated environment anyway:

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt # No-op: there are no third-party dependencies
```

## Usage

Run the tracker from inside the project folder:

```bash
python portfolio.py
```

You will see a menu:

```text
=== Stock Portfolio Manager ===
  1. Add stock
  2. Remove stock
  3. View portfolio
  4. View available stock prices
  5. Save portfolio to file
  6. Exit
```

### Example Session

```text
Welcome to the Stock Portfolio Manager!
Note: prices are hardcoded examples, not live market data.

=== Stock Portfolio Manager ===
  1. Add stock
  ...
Enter your choice (1-6): 1
Enter stock symbol (e.g. AAPL): AAPL
Enter quantity: 10
Added 10 share(s) of AAPL to your portfolio.

Enter your choice (1-6): 1
Enter stock symbol (e.g. AAPL): TSLA
Enter quantity: 5
Added 5 share(s) of TSLA to your portfolio.

Enter your choice (1-6): 3

Your Portfolio:
----------------------------------------------------
Symbol        Qty        Price          Value
----------------------------------------------------
AAPL           10 $     180.00 $      1800.00
TSLA            5 $     250.00 $      1250.00
----------------------------------------------------
Total Investment Value: $3,050.00
```

The total is simple arithmetic: `quantity × price per share`, summed across all holdings. In this example: `(10 × $180) + (5 × $250) = $3,050`.

### Saving Your Portfolio

Choose menu option **5**, then pick a format:

- **CSV** (default file: `portfolio_summary.csv`) — opens in Excel, Google Sheets, or any spreadsheet app:

  ```csv
  Symbol,Quantity,Price per Share (USD),Total Value (USD)
  AAPL,10,180.00,1800.00
  TSLA,5,250.00,1250.00
  TOTAL,,,3050.00
  ```

- **Text** (default file: `portfolio_summary.txt`) — a plain, human-readable summary:

  ```text
  Stock Portfolio Summary
  =========================
  AAPL: 10 shares x $180.00 = $1800.00
  TSLA: 5 shares x $250.00 = $1250.00

  Total Investment Value: $3050.00
  ```

You can accept the default filename or type your own when prompted. Generated summary files are listed in `.gitignore`, so they will not be committed to Git by accident.

## Supported Stocks (Hardcoded Prices)

| Symbol | Company | Price (USD) |
|--------|---------|-------------|
| AAPL | Apple Inc. | 180.00 |
| TSLA | Tesla, Inc. | 250.00 |
| MSFT | Microsoft Corporation | 420.00 |
| GOOGL | Alphabet Inc. (Class A) | 140.00 |
| AMZN | Amazon.com, Inc. | 145.00 |
| NVDA | NVIDIA Corporation | 450.00 |
| META | Meta Platforms, Inc. | 320.00 |
| NFLX | Netflix, Inc. | 450.00 |

To add, remove, or update a stock, edit the `STOCK_PRICES` dictionary at the top of `portfolio.py` — no other code changes are needed. Symbols are case-insensitive when you type them (e.g. `aapl` works the same as `AAPL`), and entering an unknown symbol shows the list of available symbols.

## Using the Code in Your Own Script

The portfolio logic is separated from the menu, so you can import it:

```python
from portfolio import Portfolio

portfolio = Portfolio()
portfolio.add_stock("AAPL", 10)
portfolio.add_stock("TSLA", 5)

print(portfolio.total_value())  # 3050.0
portfolio.save_to_csv("my_portfolio.csv")
portfolio.save_to_txt("my_portfolio.txt")
```

`Portfolio.add_stock()` raises a `ValueError` for an unknown symbol or a non-positive quantity, and `Portfolio.remove_stock()` raises `KeyError`/`ValueError` for holdings you do not have — handle those in your own code if you import it.

## How It Works

| Concept | Where it is used |
|---------|------------------|
| Dictionary | `STOCK_PRICES` maps symbols to prices; `Portfolio.holdings` maps symbols to quantities |
| Input / output | The menu loop in `main()` reads choices, symbols, and quantities from the terminal |
| Basic arithmetic | Each holding's value is `quantity × price`; the total is the sum of all holdings |
| File handling | `save_to_csv()` uses the standard-library `csv` module; `save_to_txt()` writes plain text |

## Ideas for Extending It

- Fetch live prices from a market-data API (e.g. Yahoo Finance) instead of the hardcoded dictionary
- Persist the portfolio between runs by loading a saved CSV on startup
- Add per-stock profit/loss by storing the purchase price alongside the quantity
- Add a simple chart of the portfolio's value over time

## Contributing

Contributions are welcome. Fork the repository, make your change on a branch, and open a pull request with a short description of what you changed and why. Please keep the code readable, keep prices clearly marked as examples unless a live source is added, and do not commit generated summary files.

## License

This project is released under the MIT License — free to use, modify, and share.
