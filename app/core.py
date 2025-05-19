# app/core.py

import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

DATA_FILE = 'data/transactions.csv'
INITIAL_BALANCE_FILE = 'data/initial_balance.txt'
DB_FILE = 'finance.db'

def add_transaction(date, category, amount, description):
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

def get_transactions():
    transactions = []
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions

def get_initial_balance():
    try:
        with open(INITIAL_BALANCE_FILE, 'r') as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0

def set_initial_balance(amount):
    with open(INITIAL_BALANCE_FILE, 'w') as f:
        f.write(str(amount))

def calculate_net_savings():
    transactions = get_transactions()
    total = get_initial_balance()
    for row in transactions:
        try:
            total += float(row[2])
        except (ValueError, IndexError):
            continue
    return total

def get_category_totals():
    """Returns a dict of category -> total amount spent."""
    transactions = get_transactions()
    totals = {}
    for row in transactions:
        try:
            category = row[1]
            amount = float(row[2])
            totals[category] = totals.get(category, 0) + amount
        except (IndexError, ValueError):
            continue
    return totals

def delete_transaction(index):
    transactions = get_transactions()
    if 0 <= index < len(transactions):
        del transactions[index]
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transactions)

def edit_transaction(index, date, category, amount, description):
    transactions = get_transactions()
    if 0 <= index < len(transactions):
        transactions[index] = [date, category, amount, description]
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transactions)


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = input("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ")
    amount = float(input("Enter the amount: "))
    category = input("Enter the category: ")
    description = input("Enter the description: ")
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


# --- SQL Database Utilities ---

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows dictionary-style access
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY, 
                      date TEXT, 
                      amount REAL, 
                      category TEXT, 
                      description TEXT,
                      type TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS budgets
                     (category TEXT PRIMARY KEY, 
                      amount REAL)''')

def add_transaction_sql(date, amount, category, description, type_):
    try:
        if not validate_date(date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO transactions (date, amount, category, description, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, amount, category, description, type_))
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- Data Analysis Utilities ---

def analyze_spending(df):
    # Group by category and sum amounts
    spending_by_category = df.groupby('category')['amount'].sum()
    # Calculate monthly trends
    df['date'] = pd.to_datetime(df['date'])
    monthly_spending = df.resample('M', on='date')['amount'].sum()
    return spending_by_category, monthly_spending

# --- Visualization Utilities ---

def plot_spending(spending_by_category, monthly_spending):
    plt.style.use('ggplot')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # Pie chart improvements
    spending_by_category.plot.pie(ax=ax1, autopct='%1.1f%%', 
                                  startangle=90, shadow=True,
                                  explode=[0.1]*len(spending_by_category))
    ax1.set_title('Spending by Category', pad=20)
    # Bar chart improvements
    monthly_spending.plot.bar(ax=ax2, color='skyblue', edgecolor='black')
    ax2.set_title('Monthly Spending', pad=20)
    ax2.set_ylabel('Amount ($)')
    ax2.set_xlabel('Month')
    ax2.tick_params(axis='x', rotation=45)
    plt.suptitle('Personal Finance Analysis', y=1.02, fontsize=16)
    plt.tight_layout()
    plt.savefig('spending_report.png', dpi=300, bbox_inches='tight')
    plt.close()

def spending_trend_analysis(df):
    # Add moving averages, trend lines
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum()
    monthly.plot(title='Spending Trend Over Time')
    plt.show()

# --- Savings Suggestions ---

def generate_savings_tips(df):
    tips = []
    # Identify top spending categories
    top_categories = df.groupby('category')['amount'].sum().nlargest(3)
    for cat, amount in top_categories.items():
        tips.append(f"Consider reducing spending on {cat} (${amount:.2f} monthly)")
    # Identify recurring subscriptions
    subs = df[df['description'].str.contains('subscription', case=False)]
    if not subs.empty:
        tips.append(f"Review {len(subs)} subscriptions totaling ${subs['amount'].sum():.2f}")
    return tips

# --- Budgeting Features ---

def set_budget(category, amount):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    # Add budget table creation in init_db()
    c.execute('''
        CREATE TABLE IF NOT EXISTS budgets (category TEXT PRIMARY KEY, amount REAL)
    ''')
    c.execute('''
        INSERT OR REPLACE INTO budgets (category, amount)
        VALUES (?, ?)
    ''', (category, amount))
    conn.commit()
    conn.close()

def check_budget_vs_spending(df):
    # Compare actual spending vs budgets
    pass

# --- Data Export/Import ---

def load_transactions():
    # Example: Load from the CSV file used by the CSV class
    try:
        df = pd.read_csv(CSV.CSV_FILE)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=CSV.COLUMNS)

def export_to_csv(filename='transactions.csv'):
    df = load_transactions()
    df.to_csv(filename, index=False)

def import_from_csv(filename):
    df = pd.read_csv(filename)
    for _, row in df.iterrows():
        add_transaction_sql(row['date'], row['amount'], 
                            row['category'], row['description'], row['type'])

# --- Date Validation Utility ---

from datetime import datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# --- Interactive Menu System ---

def show_menu():
    print("\nPersonal Finance Tracker")
    print("1. Add Transaction")
    print("2. View Spending Report")
    print("3. Get Savings Tips")
    print("4. Exit")
    return input("Enter your choice: ")

# --- Test Data Generation Example ---

def generate_test_data():
    import numpy as np
    categories = ['Groceries', 'Entertainment', 'Transport', 'Utilities']
    descriptions = ['Weekly shop', 'Movie tickets', 'Bus pass', 'Electric bill']
    for i in range(30):
        date = f'2024-05-{i+1:02d}'
        amount = round(np.random.uniform(5, 100), 2)
        category = np.random.choice(categories)
        desc = np.random.choice(descriptions)
        add_transaction_sql(date, amount, category, desc, 'debit')


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    init_db()  # Initialize the database
    main()

