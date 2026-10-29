#Task 2 :- Stock Portfolio Tracker
from __future__ import annotations

import csv
import sys
from pathlib import Path 
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Hardcoded stock prices (USD per share).
#
# These are example prices for learning / demonstration purposes and are
# NOT live market data. To track a different set of stocks, edit this
# dictionary -- no other code changes are needed.
# ---------------------------------------------------------------------------
STOCK_PRICES: Dict[str, float] = {
    "AAPL": 180.00,   # Apple Inc.
    "TSLA": 250.00,   # Tesla, Inc.
    "MSFT": 420.00,   # Microsoft Corporation
    "GOOGL": 140.00,  # Alphabet Inc. (Class A)
    "AMZN": 145.00,   # Amazon.com, Inc.
    "NVDA": 450.00,   # NVIDIA Corporation
    "META": 320.00,   # Meta Platforms, Inc.
    "NFLX": 450.00,   # Netflix, Inc.
}

DEFAULT_CSV_FILE = "portfolio_summary.csv"
DEFAULT_TXT_FILE = "portfolio_summary.txt"


class Portfolio:
    """A collection of stock holdings: ticker symbol -> quantity owned."""

    def __init__(self) -> None:
        self.holdings: Dict[str, int] = {}

    def add_stock(self, symbol: str, quantity: int) -> None:
        """Add ``quantity`` shares of ``symbol`` to the portfolio.

        Raises
        ------
        ValueError
            If the symbol is not in :data:`STOCK_PRICES` or the quantity
            is not a positive integer.
        """
        symbol = symbol.strip().upper()
        if symbol not in STOCK_PRICES:
            available = ", ".join(sorted(STOCK_PRICES))
            raise ValueError(
                f"Unknown stock symbol: {symbol!r}. "
                f"Available symbols: {available}."
            )
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number.")
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

    def remove_stock(self, symbol: str, quantity: int | None = None) -> None:
        """Remove shares of ``symbol``.

        If ``quantity`` is ``None`` (the default), the whole holding is
        removed. Otherwise that many shares are removed.

        Raises
        ------
        ValueError
            If the symbol is not held, or the quantity is invalid or
            larger than the holding.
        KeyError
            If the symbol is not in the portfolio.
        """
        symbol = symbol.strip().upper()
        if symbol not in self.holdings:
            raise KeyError(f"{symbol} is not in your portfolio.")
        if quantity is None:
            del self.holdings[symbol]
            return
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number.")
        if quantity > self.holdings[symbol]:
            raise ValueError(
                f"Cannot remove {quantity} shares of {symbol}: "
                f"you only hold {self.holdings[symbol]}."
            )
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]

    def rows(self) -> List[Tuple[str, int, float, float]]:
        """Return one ``(symbol, quantity, price, value)`` row per holding."""
        return [
            (symbol, quantity, STOCK_PRICES[symbol], quantity * STOCK_PRICES[symbol])
            for symbol, quantity in sorted(self.holdings.items())
        ]

    def total_value(self) -> float:
        """Return the total investment value of the portfolio in USD."""
        return sum(value for _, _, _, value in self.rows())

    def is_empty(self) -> bool:
        """Return True if the portfolio holds no stocks."""
        return not self.holdings

    # -- Saving ---------------------------------------------------------
    def save_to_csv(self, path: str | Path = DEFAULT_CSV_FILE) -> Path:
        """Save the portfolio summary to a CSV file and return its path."""
        path = Path(path)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Quantity", "Price per Share (USD)", "Total Value (USD)"])
            for symbol, quantity, price, value in self.rows():
                writer.writerow([symbol, quantity, f"{price:.2f}", f"{value:.2f}"])
            writer.writerow(["TOTAL", "", "", f"{self.total_value():.2f}"])
        return path

    def save_to_txt(self, path: str | Path = DEFAULT_TXT_FILE) -> Path:
        """Save a human-readable portfolio summary to a text file."""
        path = Path(path)
        lines = ["Stock Portfolio Summary", "=" * 25, ""]
        if self.is_empty():
            lines.append("Your portfolio is empty.")
        else:
            for symbol, quantity, price, value in self.rows():
                lines.append(
                    f"{symbol}: {quantity} shares x ${price:.2f} = ${value:.2f}"
                )
            lines.append("")
            lines.append(f"Total Investment Value: ${self.total_value():.2f}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def display_stock_prices() -> None:
    """Print the hardcoded stock prices."""
    print("\nAvailable Stocks (hardcoded prices):")
    print("-" * 38)
    for symbol, price in sorted(STOCK_PRICES.items()):
        print(f"  {symbol:<8} ${price:>10.2f}")
    print("-" * 38)


def display_portfolio(portfolio: Portfolio) -> None:
    """Print the portfolio holdings and the total investment value."""
    if portfolio.is_empty():
        print("\nYour portfolio is empty. Add a stock to get started.")
        return

    print("\nYour Portfolio:")
    print("-" * 52)
    print(f"{'Symbol':<10} {'Qty':>6} {'Price':>12} {'Value':>14}")
    print("-" * 52)
    for symbol, quantity, price, value in portfolio.rows():
        print(f"{symbol:<10} {quantity:>6} ${price:>11.2f} ${value:>13.2f}")
    print("-" * 52)
    print(f"Total Investment Value: ${portfolio.total_value():,.2f}")


def _read_quantity(prompt: str) -> int:
    """Prompt until the user enters a positive whole number."""
    while True:
        raw = input(prompt).strip()
        try:
            quantity = int(raw)
        except ValueError:
            print("Please enter a whole number (e.g. 10).")
            continue
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue
        return quantity


def _handle_add(portfolio: Portfolio) -> None:
    symbol = input("Enter stock symbol (e.g. AAPL): ").strip().upper()
    quantity = _read_quantity("Enter quantity: ")
    try:
        portfolio.add_stock(symbol, quantity)
    except ValueError as exc:
        print(f"Error: {exc}")
    else:
        print(f"Added {quantity} share(s) of {symbol} to your portfolio.")


def _handle_remove(portfolio: Portfolio) -> None:
    if portfolio.is_empty():
        print("\nYour portfolio is empty -- nothing to remove.")
        return
    symbol = input("Enter stock symbol to remove: ").strip().upper()
    raw = input("Quantity to remove (press Enter to remove the whole holding): ").strip()
    try:
        if raw == "":
            portfolio.remove_stock(symbol)
            print(f"Removed all shares of {symbol}.")
        else:
            quantity = int(raw)
            portfolio.remove_stock(symbol, quantity)
            print(f"Removed {quantity} share(s) of {symbol}.")
    except (KeyError, ValueError) as exc:
        print(f"Error: {exc}")


def _handle_save(portfolio: Portfolio) -> None:
    if portfolio.is_empty():
        print("\nYour portfolio is empty -- nothing to save.")
        return
    print("\nSave format:")
    print("  1. CSV (.csv)")
    print("  2. Text (.txt)")
    choice = input("Choose a format (1/2): ").strip()
    if choice == "1":
        filename = input(f"Filename [{DEFAULT_CSV_FILE}]: ").strip() or DEFAULT_CSV_FILE
        path = portfolio.save_to_csv(filename)
    elif choice == "2":
        filename = input(f"Filename [{DEFAULT_TXT_FILE}]: ").strip() or DEFAULT_TXT_FILE
        path = portfolio.save_to_txt(filename)
    else:
        print("Invalid choice. Nothing was saved.")
        return
    print(f"Portfolio saved to {path}.")


def print_menu() -> None:
    """Print the main menu."""
    print("\n=== Stock Portfolio Manager ===")
    print("  1. Add stock")
    print("  2. Remove stock")
    print("  3. View portfolio")
    print("  4. View available stock prices")
    print("  5. Save portfolio to file")
    print("  6. Exit")


def main() -> int:
    """Run the interactive portfolio manager."""
    portfolio = Portfolio()
    print("Welcome to the Stock Portfolio Manager!")
    print("Note: prices are hardcoded examples, not live market data.")

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            _handle_add(portfolio)
        elif choice == "2":
            _handle_remove(portfolio)
        elif choice == "3":
            display_portfolio(portfolio)
        elif choice == "4":
            display_stock_prices()
        elif choice == "5":
            _handle_save(portfolio)
        elif choice == "6":
            print("\nFinal portfolio:")
            display_portfolio(portfolio)
            print("\nThank you for using the Stock Portfolio Manager. Goodbye!")
            return 0
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
