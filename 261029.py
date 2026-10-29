########################################################################################################################################

# Problem 1
# 문자열 정렬하기 1
# 문자열 my_string이 매개변수로 주어질 때, my_string 안에 있는 숫자만 골라 오름차순 정렬한 리스트를 return 하도록 solution 함수를 작성해보세요.
# My Answer
def solution(my_string):
    answer = []

    for i in my_string:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            answer.append(int(i))

    return sorted(answer)

print(solution("hi12392"))
print(solution("p2o4i8gj2"))
print(solution("abcde0"))

# Good Answer
def solution(my_string):
    return sorted([int(c) for c in my_string if c.isdigit()])

########################################################################################################################################

# Problem 2
# 최댓값 만들기(2)
# 정수 배열 numbers가 매개변수로 주어집니다. numbers의 원소 중 두 개를 곱해 만들 수 있는 최댓값을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(numbers):
    return max(numbers[i] * numbers[j] for i in range(len(numbers)) for j in range(len(numbers)) if i != j)
    
print(solution([1, 2, -3, 4, -5]))
print(solution([0, -31, 24, 10, 1, 9]))
print(solution([10, 20, 30, 5, 5, 20, 5]))
# Good Answer
def solution(numbers):
    numbers = sorted(numbers)
    return max(numbers[0] * numbers[1], numbers[-1]*numbers[-2]) 

########################################################################################################################################

# Problem 3
# 369게임
# 머쓱이는 친구들과 369게임을 하고 있습니다. 369게임은 1부터 숫자를 하나씩 대며 3, 6, 9가 들어가는 숫자는 숫자 대신 3, 6, 9의 개수만큼 박수를 치는 게임입니다. 머쓱이가 말해야하는 숫자 order가 매개변수로 주어질 때, 머쓱이가 쳐야할 박수 횟수를 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(order):
    order_str = str(order)
    cnt = 0
    for i in order_str:
        if i in ['3', '6', '9']:
            cnt += 1
    return cnt

print(solution(3))
print(solution(29423))

# Good Answer


########################################################################################################################################