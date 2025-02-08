from basic import *
from drink import *
from cash import *

class VendingMachine:
    def __init__(self, init_drink, init_cash): # constructor(생성자)
        # dictionary comprehension(딕셔너리 컴프리헨션), 언패킹 연산자 사용
        self.__drink_dic = {key: Drink(*values) for key, values in init_drink.items()}
        self.__change_dic = {key: Cash(*values) for key, values in init_cash.items()}
    
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

    # 고액권부터 잔액 반환, 현금 재고 감소
    def return_change(self, balance):
        print_color(f"> 잔액 {balance}원을 반환합니다.", 'Y')
        # 고액권부터 반환 (역순으로 정렬)
        sorted_cash = sorted(self.__change_dic.values(), key=lambda c: c.get_face_value(), reverse=True)
        for cash in sorted_cash:
            face_value = cash.get_face_value()
            count = min(balance // face_value, cash.get_quantity())
            if count > 0:
                cash.set_quantity(cash.get_quantity() - count)
                balance -= face_value * count
                print(f"  - {face_value}원 x {count}개")
        print_line()

    # 사용자 모드 메인 루프
    def consumer_loop(self):
        while True:
            self.print_drink()
            if self.print_change() == False:
                break
            balance = self.input_cash()

            while balance > 0:
                self.print_drink(cash=balance)
                print_color(f"> 현재 잔액: {balance}원 (0번 입력 시 잔액 반환)", 'B')
                print_line()

                key = self.input_key(balance)
                if key == 0:
                    break
                balance = self.pay(key, balance)

            if balance > 0:
                self.return_change(balance)

    # ==================== 관리자 모드 메서드 ====================

    # 콘솔 메뉴 출력
    def print_console(self):
        print_color("< 관리자 콘솔 >", 'Y')
        print_line()
        print("[1] 음료 재고 보충")
        print("[2] 음료 이름 수정")
        print("[3] 음료 가격 수정")
        print("[4] 보유 현금 확인")
        print("[5] 현금 재고 보충")
        print("[6] 음료 목록 확인")
        print("[7] 관리자 모드 종료")
        print_line()

    # 메뉴 번호 입력
    def input_console(self):
        return input_range("메뉴 번호", start=1, end=7)

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

    # 관리자 모드 메인 루프
    def admin_loop(self):
        while True:
            self.print_console()
            menu = self.input_console()

            if menu == 1:
                self.edit_stock()
            elif menu == 2:
                self.edit_name()
            elif menu == 3:
                self.edit_price()
            elif menu == 4:
                self.print_cash_info()
            elif menu == 5:
                self.edit_cash()
            elif menu == 6:
                self.print_drink(admin=True)
            elif menu == 7:
                print_color("> 관리자 모드를 종료합니다.", 'Y')
                print_line()
                break

    # ==================== 시작 메서드 ====================

    # 로그인 처리 후 적절한 루프 실행
    def start(self, is_admin=False):
        if is_admin:
            self.admin_loop()
        else:
            self.consumer_loop()