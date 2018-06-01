import sqlite3
con, cur = None, None

# create table example

def createTable():
    print('createTable()')
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS
        customer(
            u_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_name TEXT NOT NULL,
            gender TEXT,
            age INT);
    ''')

    # IF NOT EXISTS ==> 이미 테이블이 있는데 또 만들 경우를 대비해서 
    con.commit();
    con.close();

# insert into example

def insertInto():
    print('inserInto()')
    con=sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('''
    INSERT OR REPLACE INTO customer(u_name, gender, age) VALUES ('hong', 'M', 30);
    ''')
    cur.execute('''
    INSERT OR REPLACE INTO customer(u_name, gender, age) VALUES ('lee', 'F', 30);
    ''')
    cur.execute('''
    INSERT OR REPLACE INTO customer(u_name) VALUES ('kim');
    ''')

    # INSERT OR REPLACE ==> 데이터가 겹칠 경우에는 insert하지말고 replace 해야함
    con.commit()
    con.close()


# update example

def update():
    print('update()')
    con=sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('''
    UPDATE customer SET age = age + 1
    ''')
    con.commit()
    con.close()


# delete example

def delete(whereStr):
    print('delete()')
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    sql = 'DELETE FROM customer %s;' % whereStr
    cur.execute(sql)
    con.commit()
    # con.rollback // 이제까지 했던 쿼리문이 날아감
    con.close()


# select by fetchone example

def selectByFetchOne(): # select는 가져오기만 하기 때문에 보여주려면 fetch 사용 ! 
    print('selectByFetchOne()')
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('''
    select * from customer;
    ''')
    # 튜플로 데이터를 가져옴
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        
        print('%4s %10s %10s %4s' % (row[0],row[1],row[2],row[3])) 
    print()


# select by fetchall example

def selectByFetchAll():
    print('selectByFetchAll()')
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('''
    select * from customer;
    ''')
    row = cur.fetchall()
    print('type(row) = ',type(row)) # list로 가져옴
    print('row = ',row)
    print('type(row[0])=',type(row[0])) # tuple로 가져옴
    print('row[0]=',row[0])
    print('type(row[0][0])=',type(row[0][0])) # int의 값으로 가져옴
    print('row[0][0]=',row[0][0])
    print()



if __name__ == '__main__':
    createTable()
    selectByFetchOne()
    insertInto()
    selectByFetchOne()
    update()
    selectByFetchOne()
    delete('WHERE age is null')
    selectByFetchAll()
    delete('')
    selectByFetchOne()

