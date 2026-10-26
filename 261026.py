# 261026 월요일
####################################################################

# Problem 1
# 대문자와 소문자
# 문자열 my_string이 매개변수로 주어질 때, 대문자는 소문자로 소문자는 대문자로 변환한 문자열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(my_string):
    answer = ''
    for char in my_string:
        if char.islower():
            answer += char.upper()
        else:
            answer += char.lower()
    return answer

# Good Answer
def solution(my_string):
    return my_string.swapcase()

print(solution("Hello"))

####################################################################

# Problem 2
# 약수 구하기
# 정수 n이 매개변수로 주어질 때, n의 약수를 오름차순으로 담은 배열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(n):
    answer = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            answer.append(i)
    answer.append(n)
    return answer

# Good Answer
# sqrt n을 사용하면 시간복잡도 좋아짐.

print(solution(60))

####################################################################

# Problem 3
# 가장 큰 수 찾기
# 정수 배열 array가 매개변수로 주어질 때, 가장 큰 수와 그 수의 인덱스를 담은 배열을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(array):
    max_index = 0
    max_value = array[0]

    for i in range(0, len(array)):
        if max_value < array[i]:
            max_value = array[i]
            max_index = i
    
    return [max_value, max_index]

# Good Answer
def solution(array):
    return [max(array), array.index(max(array))]

print(solution([1, 8, 3, 9, 11]))

####################################################################

# Problem 4
# 배열의 유사도
# 두 배열이 얼마나 유사한지 확인해보려고 합니다. 문자열 배열 s1과 s2가 주어질 때 같은 원소의 개수를 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(s1, s2):
    answer = 0
    for i in s1:
        for j in s2:
            if i == j:
                answer += 1
            
    return answer

# Good Answer
# set 함수 사용
def solution(s1, s2):
    return len(set(s1)&set(s2))

####################################################################

# Problem 5
# n의 배수 고르기
# 정수 n과 정수 배열 numlist가 매개변수로 주어질 때, numlist에서 n의 배수가 아닌 수들을 제거한 배열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(n, numlist):
    return [i for i in numlist if i % n == 0]

# Good Answer
def solution(n, numlist):
    return list(filter(lambda v: v%n==0, numlist))

print(solution(3,[4, 5, 6, 7, 8, 9, 10, 11, 12]))


####################################################################

# Problem 6
# 문자열 안에 문자열
# 문자열 str1, str2가 매개변수로 주어집니다. str1 안에 str2가 있다면 1을 없다면 2를 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(str1, str2):
   return 1 if str2 in str1 else 2

# Good Answer

print(solution("ab6CDE443fgh22iJKlmn1o", "6CDs"))

####################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


####################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


####################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


####################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


####################################################################