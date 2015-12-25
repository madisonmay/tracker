from balance_sheet import BalanceSheet, add_expense, deposit

sheet = BalanceSheet()
deposit(sheet, 100)
print sheet.balance

for snapshot in sheet.replay():
    print snapshot
