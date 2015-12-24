import unittest

from tracker import tracked
from tracker.tracker import Frame

@tracked('balance')
class BalanceSheet(object):

    def __init__(self):
        self.balance = 0

    def add_expense(self, value):
        self.balance -= value

    def deposit(self, value):
        self.balance += value


class TestTracked(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.balance_sheet = BalanceSheet()
        cls.balance_sheet.add_expense(100)
        cls.balance_sheet.add_expense(200)
        cls.balance_sheet.deposit(400)

    def test_replay(self):
        history = [0, -100, -300, 100]
        for i, snapshot in enumerate(self.balance_sheet.replay()):
            assert snapshot['balance'] == history[i]
            for frame in snapshot.stack:
                assert isinstance(frame, Frame)
