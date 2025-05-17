import sqlite3
from datetime import datetime

DB_NAME = 'finance.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,  -- 'income' or 'expense'
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(t_type, category, amount, date=None):
    if t_type not in ['income', 'expense']:
        raise ValueError("Type must be 'income' or 'expense'")
    date = date or datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (type, category, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (t_type, category, amount, date))
    conn.commit()
    conn.close()
    print(f"{t_type.title()} of ${amount} added under '{category}' on {date}")

def view_summary(month, year):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = '''
        SELECT type, category, SUM(amount)
        FROM transactions
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        GROUP BY type, category
    '''
    cursor.execute(query, (f"{int(month):02}", str(year)))
    rows = cursor.fetchall()
    
    income_total = 0
    expense_total = 0
    print(f"\nSummary for {month}/{year}:")
    for row in rows:
        t_type, category, total = row
        if t_type == 'income':
            income_total += total
        else:
            expense_total += total
        print(f"{t_type.title():7} | {category:12} | ${total:.2f}")
    
    print(f"\nTotal Income : ${income_total:.2f}")
    print(f"Total Expense: ${expense_total:.2f}")
    print(f"Net Balance  : ${income_total - expense_total:.2f}")
    
    conn.close()

def main():
    init_db()
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Monthly Summary")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            category = input("Income category: ")
            amount = float(input("Amount: "))
            add_transaction('income', category, amount)
        elif choice == '2':
            category = input("Expense category: ")
            amount = float(input("Amount: "))
            add_transaction('expense', category, amount)
        elif choice == '3':
            month = input("Enter month (1-12): ")
            year = input("Enter year (e.g., 2025): ")
            view_summary(month, year)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
