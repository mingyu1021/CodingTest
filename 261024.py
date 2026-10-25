# 261024 야간
####################################################################

# my answer
def solution(slice, n):
    answer = 0
    print(n // slice + 1)
    return answer

slice = 8
n = 20
solution(slice, n)

####################################################################

# my answer
def solution(money):
    coffee = 5500
    answer = [money//coffee, money%coffee]
    print(answer)

    return answer

solution(15000)

####################################################################

# my answer
def solution(my_string, n):
    answer = ''
    for i in my_string:
        answer += i * n
    print(answer)
    return answer

solution("hello", 3)

# good answer
def solution(my_string, n):
    return ''.join(i*n for i in my_string)

####################################################################
