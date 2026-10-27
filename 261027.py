####################################################################

# Problem 1 
# 제곱수 판별하기
# 어떤 자연수를 제곱했을 때 나오는 정수를 제곱수라고 합니다. 정수 n이 매개변수로 주어질 때, n이 제곱수라면 1을 아니라면 2를 return하도록 solution 함수를 완성해주세요.
# My Answer
import numpy as np
def solution(n):
    answer = 0
    n_sqrt = np.sqrt(n)
    if n_sqrt - int(n_sqrt) > 0:
        answer = 2
    else:
        answer = 1
    return answer

# Good Answer
def solution(n):
    return 1 if (n ** 0.5).is_integer() else 2

########################################################################################################################################

# Problem 2
# 머쓱이보다 키 큰 사람
# 머쓱이는 학교에서 키 순으로 줄을 설 때 몇 번째로 서야 하는지 궁금해졌습니다. 머쓱이네 반 친구들의 키가 담긴 정수 배열 array와 머쓱이의 키 height가 매개변수로 주어질 때, 머쓱이보다 키 큰 사람 수를 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(array, height):
    count = 0
    for i in array:
        if i > height:
            count += 1
    return count
print(solution([149, 180, 192, 170], 167))

# Good Answer


########################################################################################################################################

# Problem 3
# 옷가게 할인 받기
# 머쓱이네 옷가게는 10만 원 이상 사면 5%, 30만 원 이상 사면 10%, 50만 원 이상 사면 20%를 할인해줍니다.
# 구매한 옷의 가격 price가 주어질 때, 지불해야 할 금액을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(price):
    if price >= 500000:
        return int(price * 0.8)
    elif price >= 300000:
        return int(price * 0.9)
    elif price >= 100000:
        return int(price * 0.95)
    else:
        return price

print(solution(580000))

# Good Answer
def solution(price):
    discount_rates = {500000: 0.8, 300000: 0.9, 100000: 0.95, 0: 1}
    for discount_price, discount_rate in discount_rates.items():
        if price >= discount_price:
            return int(price * discount_rate)
        
print(solution(580000))


########################################################################################################################################

# Problem 4
# 짝수는 싫어요
# 정수 n이 매개변수로 주어질 때, n 이하의 홀수가 오름차순으로 담긴 배열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(n):
    return list(i for i in range(1, n+1, 2))

print(solution(15))

# Good Answer
def solution(n):
    return list(range(1, n+1, 2))

########################################################################################################################################

# Problem 5
# 배열 두 배 만들기
# 정수 배열 numbers가 매개변수로 주어집니다. numbers의 각 원소에 두배한 원소를 가진 배열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(numbers):
    return list(i * 2 for i in numbers)
print(solution([1, 2, 3, 4, 5]))

# Good Answer
def solution(numbers):
    return [i * 2 for i in numbers]

########################################################################################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


########################################################################################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


####################################################################