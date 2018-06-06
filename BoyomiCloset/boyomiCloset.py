from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 메인화면
# 회원기능 - 로그인
@app.route('/', methds=['GET','POST'])
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
            app.loger.debug('index() - %s' % str(params))

            con = sqlite3.connect('mywebsite_tables')
            cur = con.cursor()
            cur.execute('''
                SELECT u_id, u_name, FROM tbuser WHERE input_id=? AND pw=? AND use_flag='Y';
            ''',params)
            rows=cur.fetchall()
            con.close()
            app.loger.debug('index() -%s' % str(rows))
            if len(rows) == 1:
                session['u_id'] = rows[0][0]
                session['u_name'] = rows[0][1]
                return redirect(url_for('index'))
            else:
                login_error = '로그인에 실패하셨습니다.'
                return render_template('index.html', u_name = u_name, login_error = login_error)

# 회원기능 - 회원등록
@app.route('/user/join', methods=['GET','POST'])
def user_signup():
    if request.method == 'POST':
        input_id = request.form["id"]
        email = request.form["email"]
        pw = request.form["pw"]
        u_name = request.form["name"]
        gedner = request.form["gender"]
        birth = request.form["date"]
        u_tel = request.form["tel"]
        u_live = request.form["live"]
        sns_inform = request.form["SNS"]
        params = (input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform)
        app.loger.debug('user_signup() - %s', % str(params))

        con = sqlite3.connect('mywebsite_tables')
        cur = con.cursor()
        cur.execute('''
            INSERT INTO tbuser (input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform)
            VALUES (?,?,?,?,?,?,?,?,?,?);
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
        app.loger.debug('index() - %s' % str(rows))
        con.close()

# 회원기능 - 회원 수정

# 회원기능 - 회원 탈퇴





if __name__ == '__main__':
   # createtables()
   app.run(host='0.0.0.0', port=5000, debug=True)