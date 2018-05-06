import random

lottoList = [[0] * 5 for x in range(6)]



for i in range(0,6,1):
    for j in range(0,5,1):
        lotto = random.randrange(1,46)
        lottoList[i][j] = lotto


for i in range(0,6,1):
    for j in range(0,5,1):
        print(lottoList[i][j],end=" ")
    print("\n")