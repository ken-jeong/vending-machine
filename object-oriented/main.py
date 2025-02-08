from vending_machine import *

INIT_DRINK = { # { key: [name, price, quantity] }
    1:  ["레쓰비 마일드 커피", 600, 10],
    2:  ["게토레이 레몬", 800, 10],
    3:  ["밀키스", 800, 10],
    4:  ["립톤 아이스티 복숭아", 1000, 10],
    5:  ["칠성사이다", 1000, 10],
    6:  ["트레비 라임", 1000, 10],
    7:  ["트로피카나 스파클링 사과", 1000, 10],
    8:  ["옥수수수염차", 1300, 10],
    9:  ["데일리-C 레몬워터 비타민C 1000", 1500, 10],
    10: ["칸타타 콘트라베이스 콜드브루 블랙", 2000, 0]
}

INIT_CASH = { # { key: [face_value, quantity] }
    1: [ 100, 100],
    2: [ 500, 100],
    3: [1000, 100]
}

# 로그인 함수 (비밀번호: /admin)
def login():
    print_line()
    print_color("< 자판기 시스템 >", 'B')
    print_line()
    password = input("관리자 모드로 진입하려면 '/admin'을 입력하세요 (일반 사용자는 Enter): ")
    print_line()
    return password == "/admin"

vm = VendingMachine(INIT_DRINK, INIT_CASH)

is_admin = login()
vm.start(is_admin)