import argparse
import json
import os

EXPENSES_FILE = 'expenses.json'

def english():
    pass

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file)

def generate_expense_id(expenses):
    if not expenses:
        return 1
    else:
        max_id = max(expense['id'] for expense in expenses)
        return max_id + 1

def add_expense(expense_name, expense_amount, expense_month):
    expenses = load_expenses()
    expense_id = generate_expense_id(expenses)
    expense = {
        'id': expense_id,
        'name': expense_name,
        'amount': expense_amount,
        'month': expense_month
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense: {expense_name} - $ {expense_amount} - month-> {expense_month}")

def delete_expense(expense_id):
    expenses = load_expenses()
    try:
        expense_to_delete = next(expense for expense in expenses if expense['id'] == expense_id)
    except StopIteration:
        expense_to_delete = None

    if expense_to_delete:
        expenses.remove(expense_to_delete)
        save_expenses(expenses)
        print(f'Deleted expense: {expense_id}.')
    else:
        print(f'No expense with ID {expense_id} to delete.')

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to show.")
    for expense in expenses:
        print(f"ID: {expense['id']}  Expense: {expense['name']} Amount: {expense['amount']} Month: {expense['month']}")

def summary(month=None):
    expenses = load_expenses()
    if not expenses:
        print('There are no expenses')
        return
    
    total = 0
    if month:
        for expense in expenses:
            if expense.get('month') == month:
                total += expense['amount']
    else:
        total = sum(expense['amount'] for expense in expenses)

    return print(f'Summary of expenses: {total}')

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_expense_parser = subparsers.add_parser('add_expense', help='Add an expense')
    add_expense_parser.add_argument('name', type=str, help='Name of the expense')
    add_expense_parser.add_argument('amount', type=int, help='Amount of the expense')
    add_expense_parser.add_argument('month', type=int, help='Month of the expense')

    show_expenses_parser = subparsers.add_parser('show_expenses', help='Show all expenses')

    delete_expense_parser = subparsers.add_parser('delete_expense', help='Delete an expense')
    delete_expense_parser.add_argument('expense_id', type=int, help='ID of the expense')

    summary_parser = subparsers.add_parser('summary', help='Return expense summary')
    summary_parser.add_argument('--month', type=int, help='Enter month')

    args = parser.parse_args()

    if args.command == 'add_expense':
        add_expense(args.name, args.amount, args.month)
    elif args.command == 'show_expenses':
        list_expenses()
    elif args.command == 'delete_expense':
        delete_expense(args.expense_id)
    elif args.command == 'summary':
        summary(args.month)

if __name__ == '__main__':
    main()
