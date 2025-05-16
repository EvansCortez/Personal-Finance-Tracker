# Personal Finance Tracker

A command-line tool to track your spending, analyze habits, and get savings tips using Python, SQLite, and Pandas.

## Features

- Add, view, and analyze transactions (income/expense)
- Detect recurring transactions (subscriptions, bills)
- Set and check budgets per category
- Export/import transactions as CSV
- Visualize spending and net savings with charts
- Get automated savings tips

## Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Run the tracker:**
   ```
   python data_manangement.py
   ```

## Example Usage

- Add a transaction:  
  `1` → Enter date, amount, category, description, and type (debit/credit)
- View spending report:  
  `2`
- Get savings tips:  
  `3`
- Export transactions:  
  `4`
- Import transactions:  
  `5`
- Detect recurring transactions:  
  `6`
- Show net savings per month:  
  `7`
- Exit:  
  `8`

## Screenshots

![Spending Report Example](screenshots/spending_report.png)

## Data Backup

Regularly back up your `finance.db` and exported CSV files.

## Security

If you add user authentication, **never store passwords in plain text**—use hashing.

## Future Enhancements

- Multi-user support
- GUI or web interface
- Email reports
- Currency selection

---

## 2. Sample `requirements.txt`

```
pandas
matplotlib
numpy
```

---

## 3. Input Validation Example

Add checks for negative amounts and valid types:

````python
# In your main loop, before add_transaction:
if amount < 0:
    print("Amount must be positive.")
    continue
if type_.lower() not in ['debit', 'credit']:
    print("Type must be 'debit' or 'credit'.")
    continue
