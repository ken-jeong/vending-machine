####################################################################################################
# basic_module
####################################################################################################

# '─'을 100번 반복하여 구분선을 출력하는 함수
def print_l(): # line
    print('─'*100)

####################################################################################################

# 문자열을 해당 색으로 변환하여 반환하는 함수
def str_c(m, c):    # color, message
    if c == 'R':    # red
        return '\033[41m'+m+'\033[0m'
    elif c == 'G':  # green
        return '\033[42m'+m+'\033[0m'
    elif c == 'Y':  # yellow
        return '\033[30m\033[43m'+m+'\033[0m'
    elif c == 'B':  # blue
        return '\033[44m'+m+'\033[0m'
    else:           # exception
        return m

# 문자열을 해당 색으로 출력하는 함수
def print_c(m, c=False): # color, message
    print(str_c(m, c))

####################################################################################################

ve = str_c('입력한 값이 정수가 아닙니다. 다시 입력해주세요.', 'R') # value error

# 범위 내의 정수만을 입력받는 함수
def input_rng(m, start=0, end=10): # range, message, 디폴트 인수 insert_cash에서 사용 중
    while True:
        try:
            i = int(input(m+' ('+str(start)+' 이상 '+str(end)+' 이하의 정수로 입력): '))
            if i < start:
                print_c('입력한 값이 '+str(start)+' 이상의 정수가 아닙니다. 다시 입력해주세요.', 'R')
            elif end < i:
                print_c('입력한 값이 '+str(end)+' 이하의 정수가 아닙니다. 다시 입력해주세요.', 'R')
            else:
                return i

        except ValueError:
            print(ve)

# 현금 단위에 맞는 정수만을 입력받는 함수
def input_unit(m): # message
    while True:
        try:
            i = int(input(m+' (100원 단위 정수로 입력): '))
            if i < 0:
                print_c('입력한 값이 0 이상의 정수가 아닙니다. 다시 입력해주세요.', 'R')
            elif i % 100 != 0:
                print_c('입력한 값이 100원 단위의 정수가 아닙니다. 다시 입력해주세요.', 'R')
            else:
                return i

        except ValueError:
            print(ve)