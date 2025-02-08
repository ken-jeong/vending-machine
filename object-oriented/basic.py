# '─'을 100번 반복하여 구분선을 출력하는 함수
def print_line():
    print('─'*100)

# 문자열을 해당 색으로 변환하여 반환하는 함수, ANSI 이스케이프 코드
def str_color(msg, color=None):
    if color == 'R':   # red
        return "\033[41m"+msg+"\033[0m"
    elif color == 'G': # green
        return "\033[42m"+msg+"\033[0m"
    elif color == 'Y': # yellow
        return "\033[30m\033[43m"+msg+"\033[0m"
    elif color == 'B': # blue
        return "\033[44m"+msg+"\033[0m"
    else:              # exception
        return msg

# 문자열을 해당 색으로 출력하는 함수
def print_color(msg, color=None):
    print(str_color(msg, color))

VALUE_ERROR = str_color("[Error] 입력한 값이 정수가 아닙니다. 다시 입력해주세요.", 'R')

# 범위 내의 정수만을 입력받는 함수
def input_range(msg, start=0, end=10):
    while True:
        try:
            num = int(input(f"{msg} ({start} 이상 {end} 이하의 정수로 입력): "))
            if num < start:
                print_color(f"[Error] 입력한 값이 {start} 이상의 정수가 아닙니다. 다시 입력해주세요.", 'R')
            elif end < num:
                print_color(f"[Error] 입력한 값이 {end} 이하의 정수가 아닙니다. 다시 입력해주세요.", 'R')
            else:
                return num
        
        except ValueError:
            print(VALUE_ERROR)

# 100원 단위의 정수만을 입력받는 함수
def input_unit(msg):
    while True:
        try:
            num = int(input(f"{msg} (100원 단위의 정수로 입력): "))
            if num <= 0:
                print_color("[Error] 입력한 값이 0보다 큰 정수가 아닙니다. 다시 입력해주세요.", 'R')
            elif num % 100 != 0:
                print_color("[Error] 입력한 값이 100원 단위가 아닙니다. 다시 입력해주세요.", 'R')
            else:
                return num

        except ValueError:
            print(VALUE_ERROR)