# Internet_Programming
### 인하대학교 인터넷프로그래밍 과목 수업시간에 공부한 내용 입니다.




## SQLite
### 대소문자 구분 안함

1. 기본 명령어
```
.table # table 보여줌
.schema 테이블이름 # 특정 테이블 열과 데이터 형식 조회
.header on # SELECT문 이용 시 컬럼 정보를 같이 조회
.mode column # SELECT문 이용 시 컬럼 모드로 조회
.exit # SQLite 종료
```
2. 테이블 생성
```
CREATE TABLE 테이블이름(
 id varchar(10),
 username varchar(10),
 age int,
 email varchar(20)
);
```

3. 테이블 생성
    - 데이터 형식과 크기가 강제되지 않음. SQLite는 Dynamic data types를 제공함
    - 다른 DBMS에서 사용하는 자료형을 써도 무관하며, 지정한 데이터 형식에 맞지 않게 데이터를 넣어도 무관함
```
PRIMARY KEY # 기본키
NOT NULL # NULL 미허용
NULL # NULL 허용
UNIQUE # 유일값 설정
DEFAULT value # 기본값 지정
```

4. 테이블 삭제
```
DROP TABLE 테이블이름;
DROP TABLE usertable;
```

5. 데이터 추가
```
INSERT INTO 테이블 이름 (컬럽이름1,컬럽이름2) VALUES (값1,값2);
```
입력하려는 레코드의 컬럼 개수가 실제테이블의 컬럼 개수와 같은 경우 컬럼명을 나열 할 필요 없음

6. 데이터 조회
```
SELECT id, username, age, eamil # 조회할 컬럼들
FROM usertable # 조회할 컬럼을 가진 테이블
WHERE id = 1 # 조건에 따른 레코드 제한
ORDER BY username # 그룹화
LIMIT 3 OFFSET 3; # 조회할 레코드 수 제한
```

7. 데이터 변경
```
UPDATE usertable
SET age = 37
WHERE id = 1;
```

8. 데이터 삭제
```
DELETE FROM usertable
WHRE id = 1;
```

count, avg --> null 값은 세지않는다.
as --> 별칭정해주기
where 보다 on 을 권장 join 할 때
