list1, list2 = [], []

v = 1

for i in range(0,2):
    for j in range(0,3):
        list1.append(v)
        v+=1
    list2.append(list1)
    list1 = []
print(list2)


for i in range(0, len(list2)):
    for j in range(0, len(list2[i])):
        print(list2[i][j],end="")
    print()


for i in list2: #[1,2,3] , [4,5,6] ==== list2 는 2차원 배열
    for j in i: #[1,2,3] -> 1,2,3
        print(j,end=",")
    print()