# 261024 밤 -> 261025 야간
####################################################################

# Problem 1
# 특정 문자 제거하기
# 문자열 my_string과 문자 letter이 매개변수로 주어집니다. my_string에서 letter를 제거한 문자열을 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(my_string, letter):
    answer = ''
    for i in my_string:
        if i != letter:
            answer += i

    print(answer)
    return answer


solution("abcdef", "f")
solution("abcdefBBBSS", "B")

# Good Answer
def solution(my_string, letter):
    return my_string.replace(letter, '')

####################################################################

# Problem 2
# 배열 자르기
# 정수 배열 numbers와 정수 num1, num2가 매개변수로 주어질 때, numbers의 num1번 째 인덱스부터 num2번째 인덱스까지 자른 정수 배열을 return 하도록 solution 함수를 완성해보세요.

# My Answer
def solution(numbers, num1, num2):
    return numbers[num1:num2+1]

print(solution([1, 2, 3, 4, 5], 1, 3))
print(solution([1, 3, 5], 1, 2))

####################################################################

# Problem 3
# 순서쌍의 개수
#순서쌍이란 두 개의 숫자를 순서를 정하여 짝지어 나타낸 쌍으로 (a, b)로 표기합니다. 자연수 n이 매개변수로 주어질 때 두 숫자의 곱이 n인 자연수 순서쌍의 개수를 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(n):
    answer = 0
    for i in range(1, n//2 + 1):
        if n % i == 0:
            answer += 1

    # 자기 자신 * 1 추가
    answer += 1

    return answer

# Good Answer
def solution(n):
    answer = 0
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            answer += 2

            if i * i == n:
                answer -= 1

    return answer

print(solution(100))

# Good Answer 2
def solution(n):
    return len(list(filter(lambda v: n % (v+1) == 0, range(n))))

####################################################################

# Problem 4
# 점의 위치 구하기
# 사분면은 한 평면을 x축과 y축을 기준으로 나눈 네 부분입니다. 사분면은 아래와 같이 1부터 4까지 번호를매깁니다.
# x 좌표와 y 좌표가 모두 양수이면 제1사분면에 속합니다.
# x 좌표가 음수, y 좌표가 양수이면 제2사분면에 속합니다.
# x 좌표와 y 좌표가 모두 음수이면 제3사분면에 속합니다.
# x 좌표가 양수, y 좌표가 음수이면 제4사분면에 속합니다.
# x 좌표 (x, y)를 차례대로 담은 정수 배열 dot이 매개변수로 주어집니다. 좌표 dot이 사분면 중 어디에 속하는지 1, 2, 3, 4 중 하나를 return 하도록 solution 함수를 완성해주세요.

# My Answer
def solution(dot: list) -> int:
    # dot는 (x, y)를 차례대로 담은 정수 배열
    x = dot[0]
    y = dot[1]
    if x == 0 or y == 0:
        return 0
    if x > 0:
        return 1 if y > 0 else 4
    else:
        return 2 if y > 0 else 3

# Good Answer
def solution(dot):
    quad = [(3,2),(4,1)]
    return quad[dot[0] > 0][dot[1] > 0]

# Good Answer 2
def solution(dot):
    x,y = dot
    if x*y>0:
        return 1 if x>0 else 3
    else:
        return 4 if x>0 else 2

print(solution([1, -2]))

####################################################################
# Problem 5
# 모음 제거
# 영어에선 a, e, i, o, u 다섯 가지 알파벳을 모음으로 분류합니다. 문자열 my_string이 매개변수로 주어질 때 모음을 제거한 문자열을 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(my_string):
    answer = ""
    vowel = ['a', 'e', 'i', 'o', 'u']
    for i in my_string:
        if i in vowel:
            continue
        else:
            answer += i
    return answer

print(solution("nice to meet you"))

# Good Answer
def solution(my_string):
    return "".join(i for i in my_string if not (i in "aeiou"))

# Good Answer 2
def solution(my_string):
    vowels = ['a', 'e', 'i', 'o', 'u']
    for vowel in vowels:
        my_string = my_string.replace(vowel, '')
    return my_string

####################################################################
# Problem 6
# 숨어있는 숫자의 덧셈
# 문자열 my_string이 매개변수로 주어집니다. my_string안의 모든 자연수들의 합을 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(my_string: str) -> int:
    total = 0
    for i in my_string:
        if i in "0123456789":
            total += int(i)
    return total

print(solution("1a2b3c4d123"))

# Good Answer
# isdigit() 함수는 문자열의 모든 문자가 숫자로만 이루어져있는지 확인하는 함수
def solution(my_string):
    return sum(int(i) for i in my_string if i.isdigit())

# Good Answer 2
# isnumeric() 함수: 문자열이 숫자로만 이루어져 있는지 판별
def solution(my_string):
    answer = 0
    for c in my_string:
        if c.isnumeric():
            answer += int(c)
    return answer

####################################################################
# Problem 7
# 배열 원소의 길이
# 문자열 배열 strlist가 매개변수로 주어집니다. strlist 각 원소의 길이를 담은 배열을 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(strlist: list) -> list:
    return list(len(i) for i in strlist)
print(solution(["I", "Love", "Programmers."]))

# Good Answer
def solution(strlist: list) -> list:
    return list(map(len, strlist))
print(solution(["I", "Love", "Programmers."]))

####################################################################
# Problem 8
# 삼각형의 완성조건 (1)
# 선분 세 개로 삼각형을 만들기 위해서는 다음과 같은 조건을 만족해야 합니다.
# 가장 긴 변의 길이는 다른 두 변의 길이의 합보다 작아야 합니다.
# 삼각형의 세 변의 길이가 담긴 배열 sides이 매개변수로 주어집니다. 세 변으로 삼각형을 만들 수 있다면 1, 만들 수 없다면 2를 return하도록 solution 함수를 완성해주세요.

# My Answer
def solution(sides: list) -> int:
    # 두 변의 길이의 합이 가장 긴 변의 길이보다 커야한다.
    long_len = max(sides)
    total = sum(sides)
    return 1 if total - long_len > long_len else 2

print(solution([199, 72, 222]))

####################################################################


