import random

result = []

for i in range(1,6,1):
    print("0: 가위\n1: 바위\n2:보")
    user = int(input())
    cmp = random.randrange(0,3)
    print("user : %d" %user)
    print("cmp : %d" %cmp)
    
    if (user == 0 and cmp == 1) or (user == 1 and cmp == 2) or (user == 2 and cmp == 0):
        result.append("사용자 패")
    elif(user == cmp):
        result.append("비김")
    else:
        result.append("사용자 승")


for j in range(0,5,1):
    print(result[j])
        
        
    