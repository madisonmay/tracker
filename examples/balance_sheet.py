from tracker import tracked


@tracked('balance')
class BalanceSheet(object):

    def __init__(self):
        self.balance = 0

    def add_expense(self, value):
        self.balance -= value

    def deposit(self, value):
        self.balance += value


def add_expense(sheet, value):
    sheet.balance -= value
    sheet.add_expense(value)


def deposit(sheet, value):
    sheet.balance += value
    sheet.deposit(value)
