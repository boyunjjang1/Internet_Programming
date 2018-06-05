from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 메인화면
# 회원 기능 - 로그인
@app.route('/', methods=['GET', 'POST'])
def index():
    u_name=None
    login_error=None
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        return render_template('index.html', u_name = session['u_name'], login_error=login_error)
    else:                               # 로그인 되어 있지 않다면
        if request.method == 'POST':    # 회원 등록 정보가 넘어오는 경우
            email = request.form['email']
            password = request.form['password']
            params = (email, password)
            app.logger.debug('index() - %s' % str(params))

            con=sqlite3.connect('mywebsite')
            cur=con.cursor()
            cur.execute('''
                SELECT u_id, u_name FROM tbuser WHERE email=? AND password=? AND use_flag='Y';
                ''', params)
            rows=cur.fetchall()
            con.close()
            app.logger.debug('index() - %s' % str(rows))
            if len(rows) == 1:  # 로그인 정상
                # 세션을 생성하고 다시 리다이렉션
                session['u_id'] = rows[0][0]
                session['u_name'] = rows[0][1]
                return redirect(url_for('index'))
            else:               # 로그인 오류
                login_error='로그인에 실패하였습니다.'
                return render_template('index.html', u_name=u_name, login_error=login_error)
        else:                           # 기본 접속 (미 로그인 & GET)
            return render_template('index.html', u_name=u_name, login_error=login_error)

# 회원 기능 - 회원_등록 
@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        # 입력받은 email, u_name, password, gender, birth_year 를 데이터베이스에 저장한다. 오류 처리는 생략 한다. 
        email = request.form['email']
        u_name = request.form['u_name']
        password = request.form['password']
        gender = request.form['gender']
        birth_year = request.form['birth_year']
        params = (email, u_name, password, gender, birth_year)
        app.logger.debug('user_signup() - %s' % str(params))
        
        con=sqlite3.connect('mywebsite')
        cur=con.cursor()
        cur.execute('''
            INSERT INTO tbuser (email, u_name, password, gender, birth_year) 
            VALUES (?, ?, ?, ?, ?);
            ''', params)
        con.commit()
        con.close()
        return redirect(url_for('index'))
    return render_template('user_signup.html')

# 회원 기능 - 로그아웃
@app.route('/user/logout')
def user_logout():
    logout()
    return redirect(url_for('index'))

#로그아웃 수행
def logout():
    session.pop('u_id', None)
    session.pop('u_name', None)

#로그인 여부
def isLogin():
    return 'u_id' in session    

# 회원 기능 - 회원_정보보기
@app.route('/user/')
def user_profile():
    user_info=None
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        u_id = session['u_id']
        params = (u_id,)
        con=sqlite3.connect('mywebsite')
        cur=con.cursor()
        cur.execute('''
            SELECT u_id, email, password, u_name, gender, birth_year, add_dt, upd_dt FROM tbuser WHERE u_id=?;
            ''', params)
        rows=cur.fetchall()
        app.logger.debug('index() - %s' % str(rows))
        con.close()
        user_info = rows[0]
        if len(rows) == 1:  # 로그인 정상
            return render_template('user_profile.html', user_info=user_info)
        else:
            return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯
    else:                               # 로그인 되어 있지 않다면
        return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯

# 회원 기능 - 회원_수정
@app.route('/user/update', methods=['GET', 'POST'])
def user_update():
    user_info=None
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        if request.method != 'POST':            # 회원 정보를 제공함
            u_id = session['u_id']
            params = (u_id,)
            con=sqlite3.connect('mywebsite')
            cur=con.cursor()
            cur.execute('''
                SELECT u_id, email, password, u_name, gender, birth_year, add_dt, upd_dt FROM tbuser WHERE u_id=?;
                ''', params)
            rows=cur.fetchall()
            app.logger.debug('user_update() - rows: %s' % str(rows))
            con.close()
            user_info = rows[0]
            if len(rows) == 1:  # 로그인 정상
                return render_template('user_update.html', user_info=user_info)
            else:
                return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯
        else:                           # 회원 정보를 업데이트 함 (POST)
            # 입력받은 email, u_name, password, gender, birth_year 를 데이터베이스에 저장한다. 오류 처리는 생략 한다. 
            u_id = session['u_id']
            email = request.form['email']
            u_name = request.form['u_name']
            password = request.form['password']
            gender = request.form['gender']
            birth_year = request.form['birth_year']
            params = (email, u_name, password, gender, birth_year, u_id)
            app.logger.debug('user_update() - params: %s' % str(params))
            
            con=sqlite3.connect('mywebsite')
            cur=con.cursor()
            cur.execute('''
                UPDATE tbuser SET email=?, u_name=?, password=?, gender=?, birth_year=?, upd_dt=DATETIME('now', 'localtime') WHERE u_id=?
                ''', params)
            con.commit()
            con.close()
            return redirect(url_for('user_profile'))
    else:                               # 로그인 되어 있지 않다면
        return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯

# 회원 기능 - 회원_탈퇴
@app.route('/user/leave')
def user_leave():
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        u_id = session['u_id']
        params = (u_id,)
        app.logger.debug('user_leave() - params: %s' % str(params))
        
        con=sqlite3.connect('mywebsite')
        cur=con.cursor()
        cur.execute('''
            UPDATE tbuser SET use_flag='N', upd_dt=DATETIME('now', 'localtime') WHERE u_id=?
            ''', params)
        con.commit()
        con.close()
        logout()        # 로그아웃
        return redirect(url_for('index'))
    else:                               # 로그인 되어 있지 않다면
        return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯

# 게시판 기능 - 게시판_글목록
@app.route('/board/')
def board_list():
    pass

# 게시판 기능 - 게시판_글등록
@app.route('/board/post')
def board_post():
    pass

# 게시판 기능 - 게시판_글수정
@app.route('/board/update')
def board_update():
    pass

# 게시판 기능 - 게시판_글삭제
@app.route('/board/delete')
def board_delete():
    pass

# 게시판 기능 - 게시판_글보기
@app.route('/board/<int:page_id>')
def borad_readpost():
    pass

def createTables():
    con=sqlite3.connect('mywebsite')
    cur=con.cursor()
    cur.execute('''
        DROP TABLE IF EXISTS tbuser;
        ''')
    cur.execute('''
        DROP TABLE IF EXISTS tbboard;
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tbuser (
            u_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE, 
            password TEXT NOT NULL,
            u_name TEXT NOT NULL,
            gender TEXT NULL,
            birth_year INT NULL,
            add_dt DATETIME DEFAULT (DATETIME('now', 'localtime')), 
            upd_dt DATETIME DEFAULT (DATETIME('now', 'localtime')),
            use_flag TEXT DEFAULT ('Y')
        );
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tbboard (
            b_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER NOT NULL,
            title TEXT NOT NULL, 
            content TEXT NOT NULL, 
            add_dt DATETIME DEFAULT (DATETIME('now', 'localtime')), 
            upd_dt DATETIME DEFAULT (DATETIME('now', 'localtime')),
            use_flag TEXT DEFAULT ('Y')
        );
        ''')
    con.commit()
    pass    

if __name__ == '__main__':
    # createTables()
    app.run(host='0.0.0.0', port=5000, debug=True)

