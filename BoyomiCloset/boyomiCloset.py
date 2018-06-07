from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 메인화면
# 회원기능 - 로그인
@app.route('/', methods=['GET','POST'])
def index():
    u_name = None
    login_error = None
    if isLogin():
        return render_template('index.html', u_name = session['u_name'], login_error = login_error)
    else:
        if request.method == 'POST':
            id = request.form["id"]
            pw = request.form["pw"]
            params = (id,pw)
            app.logger.debug('index() - %s' % str(params))
            con = sqlite3.connect('mywebsite_tables')
            cur = con.cursor()
            cur.execute('''
                SELECT u_id, u_name, FROM tbuser WHERE input_id=? AND pw=? AND use_flag='Y';
            ''',params)
            rows=cur.fetchall()
            con.close()
            app.logger.debug('index() -%s' % str(rows))
            if len(rows) == 1:
                session['u_id'] = rows[0][0]
                session['u_name'] = rows[0][4]
                session['input_id'] = rows[0][1]
                return redirect(url_for('index'))
            else:
                login_error = '로그인에 실패하셨습니다.'
                return render_template('index.html', u_name = u_name, login_error = login_error)
        else:
            return render_template('index.html', u_name = u_name, login_error = login_error)

# 회원기능 - 회원등록
@app.route('/user/join', methods=['GET','POST'])
def user_signup():
    if request.method == 'POST':
        input_id = request.form["id"]
        email = request.form["email"]
        pw = request.form["pw"]
        u_name = request.form["name"]
        gender = request.form["gender"]
        birth = request.form["date"]
        u_tel = request.form["tel"]
        u_live = request.form["live"]
        sns_inform = request.form["SNS"]
        params = (input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform)
        app.logger.debug('user_signup() - %s' % str(params))
    
        con = sqlite3.connect('mywebsite_tables')
        cur = con.cursor()
        cur.execute('''
            INSERT INTO tbuser (input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform)
            VALUES (?,?,?,?,?,?,?,?,?);
        ''', params)
        con.commit()
        con.close()
        return redirect(url_for('index'))
    return render_template('join.html')
# 회원기능 - 로그아웃
@app.route('/user/logout')
def user_logout():
    logout()
    return redirect(url_for('index'))

# 로그아웃 수행
def logout():
    session.pop('u_id',None)
    session.pop('u_name',None)

# 로그인 여부
def isLogin():
    return 'u_id' in session

# 회원 기능 - 회원 정보보기
@app.route('/user/')
def user_profile():
    user_info = None
    if isLogin():
        u_id = session['u_id']
        params = (u_id,)
        con = sqlite3.connect('mywebsite_tables')
        cur = con.cursor()
        cur.execute('''
            SELECT u_id, input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform, add_at, upd_at
            From tbuser WHERE u_id=?; 
        ''', params)
        rows = cur.fetchall()
        app.logger.debug('index() - %s' % str(rows))
        con.close()
        user_info = rows[0]
        if len(rows) == 1:
            return render_template('user_profile.html', user_info = user_info)
        else:
            return render_template('user_notlogin.html')
# 회원기능 - 회원 수정
@app.route('/user/update', methods=['GET','POST'])
def user_update():
    user_info = None
    if isLogin():
        if request.method != 'POST':
            u_id = session['u_id']
            params = (u_id,)
            con = sqlite3.connect('mywebsite_tables')
            cur = con.cursor
            cur.execute('''
                SELECT u_id, input_id, pw, u_name, gender, birth, u_tel, u_live, sns_inform, add_at, upd_at
                FROM tbuser WHERE u_id=?;
            ''', params)
            rows = cur.fetchall()
            app.logger.debug('user_update() - rows: %s' % str(rows))
            con.close()
            user_info = rows[0]
            if len(rows) == 1:
                return render_template('user_update.html', user_info = user_info)
            else:
                return render_template('user_notlogin.html')
        else:
            u_id = session['u_id']
            email = request.form["email"]
            pw = request.form["pw"]
            u_name = request.form["name"]
            gender = request.form["gender"]
            birth = request.form["date"]
            u_tel = request.form["tel"]
            u_live = request.form["live"]
            sns_inform = request.form["SNS"]
            params = (email, pw, u_name, gender, birth, u_tel, u_live, sns_inform)
            app.logger.debug('user_update() - params: %s' % str(params))

            con = sqlite3.connect('mywebsite_tables')
            cur = con.cursor()
            cur.execute('''
                UPDATE tbuser SET email=?, pw=?, u_name=?, gender=?, birth_year=?, u_tel=?, u_live=?, sns_inform=?;
            ''', params)
            con.commit()
            con.close()
            return redirect(url_for('user_profile'))
    else:
        return render_template('user_notlogin.html')
        

# 회원기능 - 회원 탈퇴
@app.route('/user/leave')
def user_leave():
    if isLogin():
        u_id = session['u_id']
        params = (u_id,)
        app.logger.debug('user_leave() - params: %s' % str(params))

        con = sqlite3.connect('mywebsite_tables')
        cur = con.cursor()
        cur.execute('''
            UPDATE tbuser SET use_flag='N', upd_at = DATETIME('now', 'localtime') WHERE u_id=?;
        ''', params)
        con.commit()
        con.close()
        logout()
        return redirect(url_for('index'))
    
    else:
        return render_template('user_notlogin.html')

# admin기능 - 파일 업로드
@app.route('/admin')
def upload_file():
    if request.method == 'POST':
        p_name = request.form['p_name']
        price = request.form['price']
        file = request.files['file']

def createtables():
    con = sqlite3.connect('mywebsite_tables')
    cur = con.cursor()
    cur.execute('''
        DROP TABLE IF EXISTS tbuser;
    ''')
    cur.execute('''
        DROP TABLE IF EXISTS tbboard;
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tbuser(
        u_id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_id TEXT NOT NULL UNIQUE,
        email TEXT NULL UNIQUE,
        pw TEXT NOT NULL,
        u_name TEXT NOT NULL,
        gender TEXT NULL,
        birth TEXT NULL,
        u_tel INTEGER NULL,
        u_live TEXT NULL,
        sns_inform TEXT NULL,
        add_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
        upd_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
        use_flag TEXT DEFAULT('Y')
        );
    ''')
    con.commit()
    pass



if __name__ == '__main__':
   createtables()
   app.run(host='0.0.0.0', port=5000, debug=True)
