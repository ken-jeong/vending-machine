# 자판기 시뮬레이터 — 최소 버전: 딕셔너리 + 함수만으로 동일 기능 구현
# ponytail: 클래스/상태머신/시드 파일 없음. 데이터는 아래 딕셔너리 두 개가 전부.

LINE = "─" * 100
COLORS = {"R": "\033[41m", "G": "\033[42m", "Y": "\033[30m\033[43m", "B": "\033[44m"}

DRINKS = {  # { 번호: [이름, 가격, 재고] }
    1: ["레쓰비 마일드 커피", 600, 10],
    2: ["게토레이 레몬", 800, 10],
    3: ["밀키스", 800, 10],
    4: ["립톤 아이스티 복숭아", 1000, 10],
    5: ["칠성사이다", 1000, 10],
    6: ["트레비 라임", 1000, 10],
    7: ["트로피카나 스파클링 사과", 1000, 10],
    8: ["옥수수수염차", 1300, 10],
    9: ["데일리-C 레몬워터 비타민C 1000", 1500, 10],
    10: ["칸타타 콘트라베이스 콜드브루 블랙", 2000, 0],
}
CASH = {100: 100, 500: 100, 1000: 100}  # { 액면가: 개수 }


def color(msg, c):
    return f"{COLORS[c]}{msg}\033[0m"


def input_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print(color("[Error] 입력한 값이 정수가 아닙니다. 다시 입력해주세요.", "R"))


def input_range(msg, start, end):
    while True:
        num = input_int(f"{msg} ({start} 이상 {end} 이하의 정수로 입력): ")
        if start <= num <= end:
            return num
        print(color(f"[Error] {start} 이상 {end} 이하의 정수가 아닙니다. 다시 입력해주세요.", "R"))


def input_price(msg):
    while True:
        num = input_int(f"{msg} (100원 단위의 정수로 입력): ")
        if num > 0 and num % 100 == 0:
            return num
        print(color("[Error] 100원 단위의 양수가 아닙니다. 다시 입력해주세요.", "R"))


def show_drinks(drinks, balance=None, admin=False):
    print("< 판매 중인 상품의 목록 >")
    print(LINE)
    for key, (name, price, qty) in drinks.items():
        if qty == 0:
            state = color("재고 없음", "R")
        elif balance is not None and balance < price:
            state = color("잔액 부족", "R")
        else:
            state = color("구매 가능", "G")
        stock = f"{qty}개\t" if admin else ""
        print(f"[{key}번]\t{state}\t{stock}{price}원\t{name}")
    print(LINE)


# 고액권부터 잔액 반환, 반환 내역 { 액면가: 개수 } 반환
def return_change(cash, balance):
    print(color(f"> 잔액 {balance}원을 반환합니다.", "Y"))
    plan = {}
    for face in sorted(cash, reverse=True):
        count = min(balance // face, cash[face])
        if count > 0:
            cash[face] -= count
            balance -= face * count
            plan[face] = count
            print(f"  - {face}원 x {count}개")
    print(LINE)
    return plan


def consumer(drinks, cash):
    balance = 0
    while True:
        if balance == 0:
            show_drinks(drinks)
            if any(qty < 10 for qty in cash.values()):
                print(color("> 현재 거스름돈이 부족합니다. 상품을 판매할 수 없습니다.", "R"))
                print(LINE)
                return
            print(color("> 현재 거스름돈이 충분합니다. 상품을 구매할 수 있습니다.", "G"))
            print(LINE)
            for face in cash:
                count = input_range(f"투입할 {face}원의 개수", 0, 10)
                cash[face] += count
                balance += face * count
            print(color(f"> 투입된 금액: {balance}원", "B"))
            print(LINE)
            continue

        show_drinks(drinks, balance)
        print(color(f"> 현재 잔액: {balance}원 (0번 입력 시 잔액 반환)", "B"))
        print(LINE)
        while True:
            key = input_range("구매할 음료 번호", 0, len(drinks))
            if key == 0 or (drinks[key][2] > 0 and drinks[key][1] <= balance):
                break
            print(color("[Error] 해당 음료는 구매할 수 없습니다. 다시 선택해주세요.", "R"))
        if key == 0:
            return_change(cash, balance)
            balance = 0
        else:
            name, price, _ = drinks[key]
            drinks[key][2] -= 1
            balance -= price
            print(color(f"> '{name}'을(를) 구매했습니다.", "G"))
            print(color(f"> 남은 잔액: {balance}원", "B"))
            print(LINE)


def edit_stock(drinks):
    show_drinks(drinks, admin=True)
    key = input_range("재고를 보충할 음료 번호", 1, len(drinks))
    name, _, qty = drinks[key]
    if qty >= 10:
        print(color("[Error] 해당 음료는 이미 최대 재고(10개)입니다.", "R"))
        print(LINE)
        return
    add = input_range("보충할 개수", 0, 10 - qty)
    drinks[key][2] += add
    print(color(f"> '{name}'의 재고를 {add}개 보충했습니다. (현재: {drinks[key][2]}개)", "G"))
    print(LINE)


def edit_name(drinks):
    show_drinks(drinks, admin=True)
    key = input_range("이름을 수정할 음료 번호", 1, len(drinks))
    old_name = drinks[key][0]
    drinks[key][0] = input("새로운 이름 입력: ")
    print(color(f"> 음료 이름을 '{old_name}'에서 '{drinks[key][0]}'(으)로 수정했습니다.", "G"))
    print(LINE)


def edit_price(drinks):
    show_drinks(drinks, admin=True)
    key = input_range("가격을 수정할 음료 번호", 1, len(drinks))
    old_price = drinks[key][1]
    drinks[key][1] = input_price("새로운 가격")
    print(color(f"> '{drinks[key][0]}'의 가격을 {old_price}원에서 {drinks[key][1]}원으로 수정했습니다.", "G"))
    print(LINE)


def show_cash(cash):
    print("< 보유 현금 현황 >")
    print(LINE)
    for face, qty in cash.items():
        print(f"  {face}원: {qty}개 (총 {face * qty}원)")
    print(LINE)
    print(color(f"> 보유 현금 총액: {sum(f * q for f, q in cash.items())}원", "B"))
    print(LINE)


def edit_cash(cash):
    show_cash(cash)
    faces = list(cash)
    print("보충할 화폐 단위를 선택하세요:")
    for i, face in enumerate(faces, 1):
        print(f"  [{i}] {face}원")
    print(LINE)
    face = faces[input_range("화폐 단위 번호", 1, len(faces)) - 1]
    if cash[face] >= 100:
        print(color("[Error] 해당 화폐는 이미 최대 재고(100개)입니다.", "R"))
        print(LINE)
        return
    add = input_range("보충할 개수", 0, 100 - cash[face])
    cash[face] += add
    print(color(f"> {face}원을 {add}개 보충했습니다. (현재: {cash[face]}개)", "G"))
    print(LINE)


def admin(drinks, cash):
    menu = {  # { 번호: (라벨, 동작) }, 동작이 None이면 종료
        1: ("음료 재고 보충", lambda: edit_stock(drinks)),
        2: ("음료 이름 수정", lambda: edit_name(drinks)),
        3: ("음료 가격 수정", lambda: edit_price(drinks)),
        4: ("보유 현금 확인", lambda: show_cash(cash)),
        5: ("현금 재고 보충", lambda: edit_cash(cash)),
        6: ("음료 목록 확인", lambda: show_drinks(drinks, admin=True)),
        7: ("관리자 모드 종료", None),
    }
    while True:
        print(color("< 관리자 콘솔 >", "Y"))
        print(LINE)
        for key, (label, _) in menu.items():
            print(f"[{key}] {label}")
        print(LINE)
        _, action = menu[input_range("메뉴 번호", 1, len(menu))]
        if action is None:
            print(color("> 관리자 모드를 종료합니다.", "Y"))
            print(LINE)
            return
        action()


def main():
    print(LINE)
    print(color("< 자판기 시스템 >", "B"))
    print(LINE)
    is_admin = input("관리자 모드로 진입하려면 '/admin'을 입력하세요 (일반 사용자는 Enter): ") == "/admin"
    print(LINE)
    (admin if is_admin else consumer)(DRINKS, CASH)


if __name__ == "__main__":
    main()
