########################################################################################################################################

# Problem 1
# 가위 바위 보
# 가위는 2 바위는 0 보는 5로 표현합니다. 가위 바위 보를 내는 순서대로 나타낸 문자열 rsp가 매개변수로 주어질 때, rsp에 저장된 가위 바위 보를 모두 이기는 경우를 순서대로 나타낸 문자열을 return하도록 solution 함수를 완성해보세요.
# My Answer
def solution(rsp):
    answer = ""
    for i in rsp:
        if i == "0":
            answer += "5"
        elif i == "2":
            answer += "0"
        elif i == "5":
            answer += "2"
    return answer

print(solution("205"))


# Good Answer
def solution(rsp):
    d = {'0':'5','2':'0','5':'2'}
    return ''.join(d[i] for i in rsp)

# Good Answer2
def solution(rsp):
    rsp =rsp.replace('2','s')
    rsp =rsp.replace('5','p')
    rsp =rsp.replace('0','r')
    rsp =rsp.replace('r','5')
    rsp =rsp.replace('s','0')
    rsp =rsp.replace('p','2')
    return rsp

########################################################################################################################################

# Problem 2
# 문자열 정렬하기 (2)
# 영어 대소문자로 이루어진 문자열 my_string이 매개변수로 주어질 때, my_string을 모두 소문자로 바꾸고 알파벳 순서대로 정렬한 문자열을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(my_string):
    lower_string = my_string.lower()
    sorted_string = sorted(lower_string)
    
    return ''.join(sorted_string)

print(solution("Bcad"))
print(solution("heLLo"))
print(solution("Python"))
# Good Answer


########################################################################################################################################

# Problem 3
# 중복된 숫자 개수
# 정수가 담긴 배열 array와 정수 n이 매개변수로 주어질 때, array에 n이 몇 개 있는 지를 return 하도록 solution 함수를 완성해보세요.

# My Answer
def solution(array, n):
    count = 0
    for i in array:
        if i == n:
            count += 1
    return count

# Good Answer
def solution(array, n):
    return array.count(n)

########################################################################################################################################

# Problem 4
# 중앙값 구하기
# 중앙값은 어떤 주어진 값들을 크기의 순서대로 정렬했을 때 가장 중앙에 위치하는 값을 의미합니다. 예를 들어 1, 2, 7, 10, 11의 중앙값은 7입니다. 정수 배열 array가 매개변수로 주어질 때, 중앙값을 return 하도록 solution 함수를 완성해보세요.
# My Answer
def solution(array):
    return sorted(array)[len(array)//2]

print(solution([1, 2, 7, 10, 11]))
print(solution([9, -1, 0]))
# Good Answer


########################################################################################################################################

# Problem 5
# 직각삼각형 출력하기
# "*"의 높이와 너비를 1이라고 했을 때, "*"을 이용해 직각 이등변 삼각형을 그리려고합니다. 정수 n 이 주어지면 높이와 너비가 n 인 직각 이등변 삼각형을 출력하도록 코드를 작성해보세요.
# My Answer
n = int(input())
for i in range(1, n + 1):
    print("*" * i)

# Good Answer
print('\n'.join('*' * (i + 1) for i in range(int(input()))))

########################################################################################################################################

# Problem 6
# 개미 군단
# 개미 군단이 사냥을 나가려고 합니다. 개미군단은 사냥감의 체력에 딱 맞는 병력을 데리고 나가려고 합니다. 장군개미는 5의 공격력을, 병정개미는 3의 공격력을 일개미는 1의 공격력을 가지고 있습니다. 예를 들어 체력 23의 여치를 사냥하려고 할 때, 일개미 23마리를 데리고 가도 되지만, 장군개미 네 마리와 병정개미 한 마리를 데리고 간다면 더 적은 병력으로 사냥할 수 있습니다. 사냥감의 체력 hp가 매개변수로 주어질 때, 사냥감의 체력에 딱 맞게 최소한의 병력을 구성하려면 몇 마리의 개미가 필요한지를 return하도록 solution 함수를 완성해주세요.
# My Answer
def solution(hp):
    cnt = 0
    cnt += hp // 5
    cnt += (hp % 5) // 3
    cnt += (hp % 5) % 3
    return cnt

print(solution(23))
print(solution(24))
print(solution(999))

# Good Answer
def solution(hp):    
    return hp // 5 + (hp % 5 // 3) + ((hp % 5) % 3)

# Good Answer 2
def solution(hp):
    answer = 0
    for ant in [5, 3, 1]:
        d, hp = divmod(hp, ant)
        answer += d
    return answer

########################################################################################################################################

# Problem 7
# 주사위의 개수
# 머쓱이는 직육면체 모양의 상자를 하나 가지고 있는데 이 상자에 정육면체 모양의 주사위를 최대한 많이 채우고 싶습니다. 상자의 가로, 세로, 높이가 저장되어있는 배열 box와 주사위 모서리의 길이 정수 n이 매개변수로 주어졌을 때, 상자에 들어갈 수 있는 주사위의 최대 개수를 return 하도록 solution 함수를 완성해주세요.
# My Answer
def solution(box, n):
    width = box[0]
    length = box[1]
    height = box[2]

    return (width // n) * (length // n) * (height // n)

print(solution([1, 1, 1], 1))
print(solution([10, 8, 6], 3))


# Good Answer
def solution(box, n):
    x, y, z = box
    return (x // n) * (y // n) * (z // n )

########################################################################################################################################

# Problem 
# 
# 
# My Answer


# Good Answer


########################################################################################################################################