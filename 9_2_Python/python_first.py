# 주석 

money = 0
amount, balance = 0, 0
c500 = c100 = c50 = c10 = 0

print('money: ', end='')

money = input() # input은 기본적으로 자료형이 문자열로 반환됨
money = int(money) # 정수형으로 형변환후 다시 자기자신에게 넣어준다

amount = int(input('amount: ')) # 상품 총 금액

balance = money - amount # 잔액

if balance<0:
    print('입금한 돈이 상품 총 금액 보다 작습니다.')
elif balance==0:
    print('입금한 돈과 상품 총 금액이 일치하여 지불할 잔돈이 없습니다.')
else:
    pass

c500 = balance // 500
balance = balance % 500 

c100 = balance // 100
balance %= 100

c50 = balance // 50
balance %= 50

c10 = balance // 10
balance %= 10

# print(c500, c100, c50, c10, balance)
print()
print('입금한 돈: ', money)
print('상품 총 금액 : ', amount, end='')
print('지불할 잔돈 : %d' %(money-amount))
print('500원 : %d\n100원 : %d' % (c500, c100))
print(' 50원 : {0:d}'.format(c50))
print(' 50원 : {0:4d}'.format(c10))
print(' 50원 : {0:04d}'.format(balance))


boolVar, intVar, floatVar, strVar = True, 0, 0.0, ''
print(type(boolVar))
print(type(intVar))
print(type(floatVar))
print(type(strVar))
