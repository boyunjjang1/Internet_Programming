i, j = 0, 0



for j in range(1, 10, 1):
    print("* %d단 *" % j, end='  ')

for i in range(1, 10, 1): # 행 , 들여쓰기한 모든 구간은 for 문이 돌아감
    for j in range(2, 10, 1):
        print("%d*%d=%2d" %(j, i, j*i),end='  ')
    print()