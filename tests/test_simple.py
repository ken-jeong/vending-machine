import importlib.util
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# object-oriented/main.py와 모듈 이름이 겹치지 않도록 경로로 직접 로드
_spec = importlib.util.spec_from_file_location(
    "simple_main", Path(__file__).resolve().parents[1] / "simple" / "main.py"
)
simple = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(simple)


class ReturnChangeTests(unittest.TestCase):
    # (현금 재고, 잔액) -> 반환 내역 { 액면가: 개수 }
    def test_return_change_table(self):
        cases = [
            ({100: 5, 500: 2, 1000: 1}, 1600, {1000: 1, 500: 1, 100: 1}),
            ({100: 3, 500: 1, 1000: 2}, 800, {500: 1, 100: 3}),
            ({100: 1, 500: 0, 1000: 0}, 700, {100: 1}),  # 재고 부족: 600원 미반환
            ({100: 5, 500: 5, 1000: 5}, 0, {}),
        ]
        for cash, balance, expected in cases:
            with self.subTest(cash=dict(cash), balance=balance):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(simple.return_change(cash, balance), expected)


if __name__ == "__main__":
    unittest.main()
