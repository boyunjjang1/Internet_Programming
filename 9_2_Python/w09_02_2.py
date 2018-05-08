import random

lottoList = []

while(True):
    lottos = []
    for i in range(0,6):
        lottos.append(random.randrange(1,46))
    

    lottos.sort()
    lottoList.append(lottos)

    for j in range(0,5):
        if(lottos[j] == lottos[j+1]):
            lottoList.pop()
            break


    if(len(lottoList) == 5):
        break




for i in lottoList:
    for j in i:
        print(j,end=" ")
    print()