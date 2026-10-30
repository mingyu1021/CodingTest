########################################################################################################################################

# Problem 1
# 암호 해독
# 군 전략가 머쓱이는 전쟁 중 적군이 다음과 같은 암호 체계를 사용한다는 것을 알아냈습니다.
# 암호화된 문자열 cipher를 주고받습니다.
# 그 문자열에서 code의 배수 번째 글자만 진짜 암호입니다.
# 문자열 cipher와 정수 code가 매개변수로 주어질 때 해독된 암호 문자열을 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(cipher: str, code: int) -> str:
    return ''.join([cipher[i] for i in range(code-1, len(cipher), code)])

print(solution("dfjardstddetckdaccccdegk", 4))
print(solution("pfqallllabwaoclk", 2))

# Good Answer
def solution(cipher, code):
    answer = cipher[code-1::code]
    return answer

########################################################################################################################################

# Problem 2
# 인덱스 바꾸기
# 문자열 my_string과 정수 num1, num2가 매개변수로 주어질 때, my_string에서 인덱스 num1과 인덱스 num2에 해당하는 문자를 바꾼 문자열을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(my_string, num1, num2):
    return my_string[:min(num1, num2)] + my_string[max(num1, num2)] + my_string[min(num1, num2) + 1:max(num1, num2)] + my_string[min(num1, num2)] + my_string[max(num1, num2) + 1:]

print(solution("hello", 1, 2))
print(solution("I love you", 3, 6))

# Good Answer
def solution(my_string, num1, num2):
    s = list(my_string)
    s[num1],s[num2] = s[num2],s[num1]
    return ''.join(s)

########################################################################################################################################

# Problem 3
# 숫자 찾기
# 정수 num과 k가 매개변수로 주어질 때, num을 이루는 숫자 중에 k가 있으면 num의 그 숫자가 있는 자리 수를 return하고 없으면 -1을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(num, k):
    if str(k) in str(num):
        return (str(num).index(str(k))) + 1
    return -1

print(solution(29183, 1))
print(solution(232443, 4))
print(solution(123456, 7))

# Good Answer


########################################################################################################################################