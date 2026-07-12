import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "object-oriented"))

from drink import Drink
from main import load_seed, SEED_PATH
from vending_machine import VendingMachine


class DrinkAvailabilityTests(unittest.TestCase):
    # (가격, 재고, 잔액) -> 구매 가능 여부
    def test_availability_table(self):
        cases = [
            (500, 0, 1000, False),  # 재고 없음
            (500, 1, 400, False),   # 잔액 부족
            (500, 1, 500, True),    # 잔액 일치
            (500, 1, 700, True),    # 잔액 초과
        ]
        for price, quantity, balance, expected in cases:
            with self.subTest(price=price, quantity=quantity, balance=balance):
                drink = Drink("테스트", price, quantity)
                self.assertEqual(drink.is_available(balance), expected)


class ChangeReturnTests(unittest.TestCase):
    # (현금 재고, 잔액) -> 반환 내역 { 액면가: 개수 }
    def test_return_change_table(self):
        cases = [
            ({1: [100, 5], 2: [500, 2], 3: [1000, 1]}, 1600, {1000: 1, 500: 1, 100: 1}),
            ({1: [100, 3], 2: [500, 1], 3: [1000, 2]}, 800, {500: 1, 100: 3}),
            ({1: [100, 1], 2: [500, 0], 3: [1000, 0]}, 700, {100: 1}),  # 재고 부족: 600원 미반환
            ({1: [100, 5], 2: [500, 5], 3: [1000, 5]}, 0, {}),
        ]
        for init_cash, balance, expected in cases:
            with self.subTest(init_cash=init_cash, balance=balance):
                vm = VendingMachine({1: ["테스트", 600, 1]}, init_cash)
                with redirect_stdout(io.StringIO()):
                    plan = vm.return_change(balance)
                self.assertEqual(plan, expected)

    def test_pay_updates_balance_and_stock(self):
        vm = VendingMachine({1: ["테스트", 600, 2]}, {1: [100, 100]})
        with redirect_stdout(io.StringIO()):
            balance = vm.pay(1, 1000)
        self.assertEqual(balance, 400)
        self.assertEqual(vm._VendingMachine__drink_dic[1].get_quantity(), 1)


class SeedTests(unittest.TestCase):
    def test_load_seed(self):
        init_drink, init_cash = load_seed(SEED_PATH)
        self.assertEqual(init_drink[1], ["레쓰비 마일드 커피", 600, 10])
        self.assertEqual(init_cash[3], [1000, 100])


if __name__ == "__main__":
    unittest.main()
