
import flask

foods = {'짜장면': '단무지',
        '피자' : '피클',
        '치킨' : '맥주',
        '삼겹살' : '상추',
        '라면' : '김치'}


print(foods.keys())
print(foods.values())
print(foods.items())

while True: # 무한반복
    print(str(list(foods.keys())))
    myFood = input('먹고 싶은 음식은?')
    if myFood in foods: # 입력받은 값이 key 값이 있다면 True가 나옴
        print('같이 먹어야 할 음식은', foods.get(myFood), '입니다')
    elif myFood == '끝':
        break
    else:
        print('입력한 음식은 없습니다.')