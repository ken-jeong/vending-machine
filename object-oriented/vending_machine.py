from basic import *
from drink import *
from cash import *

class VendingMachine:
    def __init__(self, init_drink, init_cash): # constructor(생성자)
        # dictionary comprehension(딕셔너리 컴프리헨션), 언패킹 연산자 사용
        self.__drink_dic = {key: Drink(*values) for key, values in init_drink.items()}
        self.__change_dic = {key: Cash(*values) for key, values in init_cash.items()}
        self.__balance = 0
    
    def print_drink(self, cash=None, admin=False):
        print("< 판매 중인 상품의 목록 >")
        print_line()

        for key, drink in self.__drink_dic.items():
            print(f"[{key}번]\t{drink.info_drink(cash, admin)}") # f-string
        print_line()
    
    def print_change(self):
        for cash in self.__change_dic.values():
            if cash.get_quantity() < 10:
                print_color("> 현재 거스름돈이 부족합니다. 상품을 판매할 수 없습니다.", 'R')
                print_line()
                return False
        
        print_color("> 현재 거스름돈이 충분합니다. 상품을 구매할 수 있습니다.", 'G')
        print_line()
    
    def input_cash(self):
        amount = 0
        
        for cash in self.__change_dic.values():
            face_value = cash.get_face_value()
            input_count = input_range(f"투입할 {face_value}원의 개수", start=0, end=10)
            amount += face_value * input_count
            cash.set_quantity(cash.get_quantity()+input_count)

        print_color(f"> 투입된 금액: {amount}원", 'B')
        print_line()

        return amount

    # ==================== 사용자 모드 메서드 ====================

    # 구매할 음료 번호 입력 (구매 가능한 것만 선택 허용)
    def input_key(self, balance):
        while True:
            key = input_range("구매할 음료 번호", start=0, end=len(self.__drink_dic))
            if key == 0:
                return 0  # 잔액 반환 선택
            drink = self.__drink_dic[key]
            if drink.is_available(balance):
                return key
            else:
                print_color("[Error] 해당 음료는 구매할 수 없습니다. 다시 선택해주세요.", 'R')

    # 결제 처리, 재고 감소, 새 잔액 반환
    def pay(self, key, balance):
        drink = self.__drink_dic[key]
        drink.set_quantity(drink.get_quantity() - 1)
        new_balance = balance - drink.get_price()
        print_color(f"> '{drink.get_name()}'을(를) 구매했습니다.", 'G')
        print_color(f"> 남은 잔액: {new_balance}원", 'B')
        print_line()
        return new_balance

    # 고액권부터 잔액 반환, 현금 재고 감소, 반환 내역 { 액면가: 개수 } 반환
    def return_change(self, balance):
        print_color(f"> 잔액 {balance}원을 반환합니다.", 'Y')
        plan = {}
        # 고액권부터 반환 (역순으로 정렬)
        sorted_cash = sorted(self.__change_dic.values(), key=lambda c: c.get_face_value(), reverse=True)
        for cash in sorted_cash:
            face_value = cash.get_face_value()
            count = min(balance // face_value, cash.get_quantity())
            if count > 0:
                cash.set_quantity(cash.get_quantity() - count)
                balance -= face_value * count
                plan[face_value] = count
                print(f"  - {face_value}원 x {count}개")
        print_line()
        return plan

    # 사용자 모드 메인 루프: 상태 테이블 조회가 흐름을 결정 (state machine)
    # 각 상태 메서드는 다음 상태를 반환
    def consumer_loop(self):
        handlers = {
            "IDLE": self.state_idle,
            "INSERT": self.state_insert,
            "SELECT": self.state_select,
            "RETURN": self.state_return,
        }
        state = "IDLE"
        while state != "END":
            state = handlers[state]()

    # IDLE: 상품 목록 출력, 거스름돈 부족 시 판매 종료
    def state_idle(self):
        self.print_drink()
        if self.print_change() == False:
            return "END"
        return "INSERT"

    # INSERT: 현금 투입
    def state_insert(self):
        self.__balance = self.input_cash()
        return "SELECT" if self.__balance > 0 else "IDLE"

    # SELECT: 음료 선택 후 결제, 0번 입력 시 잔액 반환
    def state_select(self):
        self.print_drink(cash=self.__balance)
        print_color(f"> 현재 잔액: {self.__balance}원 (0번 입력 시 잔액 반환)", 'B')
        print_line()

        key = self.input_key(self.__balance)
        if key == 0:
            return "RETURN"
        self.__balance = self.pay(key, self.__balance)
        return "SELECT" if self.__balance > 0 else "IDLE"

    # RETURN: 잔액 반환 후 처음으로
    def state_return(self):
        self.return_change(self.__balance)
        self.__balance = 0
        return "IDLE"

    # ==================== 관리자 모드 메서드 ====================

    # 음료 재고 보충 (최대 10개)
    def edit_stock(self):
        self.print_drink(admin=True)
        key = input_range("재고를 보충할 음료 번호", start=1, end=len(self.__drink_dic))
        drink = self.__drink_dic[key]
        current = drink.get_quantity()
        max_add = 10 - current
        if max_add <= 0:
            print_color("[Error] 해당 음료는 이미 최대 재고(10개)입니다.", 'R')
            print_line()
            return
        add_count = input_range("보충할 개수", start=0, end=max_add)
        drink.set_quantity(current + add_count)
        print_color(f"> '{drink.get_name()}'의 재고를 {add_count}개 보충했습니다. (현재: {drink.get_quantity()}개)", 'G')
        print_line()

    # 음료 이름 수정
    def edit_name(self):
        self.print_drink(admin=True)
        key = input_range("이름을 수정할 음료 번호", start=1, end=len(self.__drink_dic))
        drink = self.__drink_dic[key]
        old_name = drink.get_name()
        new_name = input("새로운 이름 입력: ")
        drink.set_name(new_name)
        print_color(f"> 음료 이름을 '{old_name}'에서 '{new_name}'(으)로 수정했습니다.", 'G')
        print_line()

    # 음료 가격 수정 (100원 단위)
    def edit_price(self):
        self.print_drink(admin=True)
        key = input_range("가격을 수정할 음료 번호", start=1, end=len(self.__drink_dic))
        drink = self.__drink_dic[key]
        old_price = drink.get_price()
        new_price = input_unit("새로운 가격")
        drink.set_price(new_price)
        print_color(f"> '{drink.get_name()}'의 가격을 {old_price}원에서 {new_price}원으로 수정했습니다.", 'G')
        print_line()

    # 보유 현금 출력
    def print_cash_info(self):
        print("< 보유 현금 현황 >")
        print_line()
        total = 0
        for cash in self.__change_dic.values():
            face_value = cash.get_face_value()
            quantity = cash.get_quantity()
            amount = cash.amount()
            total += amount
            print(f"  {face_value}원: {quantity}개 (총 {amount}원)")
        print_line()
        print_color(f"> 보유 현금 총액: {total}원", 'B')
        print_line()

    # 현금 재고 보충 (최대 100개)
    def edit_cash(self):
        self.print_cash_info()
        print("보충할 화폐 단위를 선택하세요:")
        for key, cash in self.__change_dic.items():
            print(f"  [{key}] {cash.get_face_value()}원")
        print_line()
        key = input_range("화폐 단위 번호", start=1, end=len(self.__change_dic))
        cash = self.__change_dic[key]
        current = cash.get_quantity()
        max_add = 100 - current
        if max_add <= 0:
            print_color(f"[Error] 해당 화폐는 이미 최대 재고(100개)입니다.", 'R')
            print_line()
            return
        add_count = input_range("보충할 개수", start=0, end=max_add)
        cash.set_quantity(current + add_count)
        print_color(f"> {cash.get_face_value()}원을 {add_count}개 보충했습니다. (현재: {cash.get_quantity()}개)", 'G')
        print_line()

    # 관리자 모드 메인 루프: 메뉴 테이블 하나가 출력과 실행을 모두 담당
    def admin_loop(self):
        menu_table = { # { 번호: (라벨, 동작) }, 동작이 None이면 종료
            1: ("음료 재고 보충", self.edit_stock),
            2: ("음료 이름 수정", self.edit_name),
            3: ("음료 가격 수정", self.edit_price),
            4: ("보유 현금 확인", self.print_cash_info),
            5: ("현금 재고 보충", self.edit_cash),
            6: ("음료 목록 확인", lambda: self.print_drink(admin=True)),
            7: ("관리자 모드 종료", None),
        }

        while True:
            print_color("< 관리자 콘솔 >", 'Y')
            print_line()
            for key, (label, _) in menu_table.items():
                print(f"[{key}] {label}")
            print_line()

            menu = input_range("메뉴 번호", start=1, end=len(menu_table))
            _, action = menu_table[menu]
            if action is None:
                print_color("> 관리자 모드를 종료합니다.", 'Y')
                print_line()
                break
            action()

    # ==================== 시작 메서드 ====================

    # 로그인 처리 후 적절한 루프 실행
    def start(self, is_admin=False):
        if is_admin:
            self.admin_loop()
        else:
            self.consumer_loop()