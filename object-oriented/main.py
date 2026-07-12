import json
from pathlib import Path

from vending_machine import *

SEED_PATH = Path(__file__).resolve().parent / "data" / "seed.json"

# 시드 데이터 로딩 (JSON의 문자열 키를 정수 키로 변환)
def load_seed(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    init_drink = {int(key): value for key, value in data["drinks"].items()}
    init_cash = {int(key): value for key, value in data["cash"].items()}
    return init_drink, init_cash

# 로그인 함수 (비밀번호: /admin)
def login():
    print_line()
    print_color("< 자판기 시스템 >", 'B')
    print_line()
    password = input("관리자 모드로 진입하려면 '/admin'을 입력하세요 (일반 사용자는 Enter): ")
    print_line()
    return password == "/admin"

if __name__ == "__main__":
    init_drink, init_cash = load_seed(SEED_PATH)
    vm = VendingMachine(init_drink, init_cash)
    vm.start(login())
