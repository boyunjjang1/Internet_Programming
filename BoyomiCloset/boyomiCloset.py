from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 메인화면
# 회원기능 - 로그인
@app.route('/', methods=['GET','POST'])
def index():
    session.clear()
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
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                SELECT u_id, u_name FROM tbuser WHERE input_id=? AND pw=? AND use_flag='Y';
            ''',params)
            rows=cur.fetchall()
            con.close()
            app.logger.debug('index() -%s' % str(rows))
            if len(rows) == 1:
                session['u_id'] = rows[0][0]
                session['u_name'] = rows[0][1]
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
    
        con = sqlite3.connect('mywebsite_createtables')
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
        con = sqlite3.connect('mywebsite_createtables')
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
            con = sqlite3.connect('mywebsite_createtables')
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

            con = sqlite3.connect('mywebsite_createtables')
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

        con = sqlite3.connect('mywebsite_createtables')
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


# 게시판 기능 - 게시판_글목록
@app.route('/board/')
def board_list():
    pageNum = None
    pageNumList = None


    pageNum = request.args.get('page')
    if pageNum is None:
        pageNum = '1'
    pageNum = int(pageNum)
    if pageNum < 1:
        pageNum = 1
    app.logger.debug('board_list() - pageNum : %d' % pageNum)


    keyword = None
    keyword = request.args.get('keyword')
    app.logger.debug('board_list() - keyword : %s' % keyword)


    startNum, endNum = 0, 0
    if pageNum >= 3:
        startNum = pageNum - 2
    else:
        startNum = 1
    endNum = startNum + 4
    pageNumList = list(range(startNum, endNum+1))
    app.logger.debug('board_list() - pageNumList : %s' % pageNumList)
    # 조회 할 페이지 번호를 가져옴 get query string
    pageNum = request.args.get('page')
    if pageNum is None:
        pageNum = '1'
    pageNum = int(pageNum)
    if pageNum < 1:
        pageNum = 1
    app.logger.debug('board_list() - pageNum : %d' % pageNum)


    keyword = None
    keyword = request.args.get('keyword')
    app.logger.debug('board_list() - keyword : %s' % keyword)


    # DB로 부터 tbboard 게시판 글 목록을 가져옴
    offset = (pageNum - 1) * 10
    params = (offset,)
    con = sqlite3.connect('mywebsite_createtables')
    cur = con.cursor()
    if keyword == None:
        cur.execute('''
            SELECT b_id, u_name, title, b.add_at FROM tbboard AS b
            INNER JOIN tbuser AS u ON b.u_id = u.u_id
            WHERE b.use_flag = 'Y' ORDER BY b_id DESC LIMIT 10 OFFSET ?;
            ''', params)
    else:
        params = (keyword, keyword, offset)
        cur.execute('''
            SELECT b_id, u_name, title, b.add_at FROM tbboard AS b
            INNER JOIN tbuser AS u ON b.u_id = u.u_id
            WHERE b.use_flag = 'Y' AND (b.title like '%'||?||'%'
            OR b.content like '%'||?||'%') ORDER BY b_id DESC LIMIT 10 OFFSET ?;
        ''', params)

    rows = cur.fetchall()
    app.logger.debug('board_list() - %s' % rows)
    con.close()
    return render_template('board_list.html', board_rows = rows, pageNum = pageNum, pageNumList = pageNumList, keyword = keyword)



# 게시판 기능 - 게시판_글 등록
@app.route('/board/post', methods = ['GET','POST'])
def board_post():
    if isLogin():
        if request.method == 'POST':
            u_id = session['u_id']
            title = request.form['title']
            content = request.form['content']
            params = (u_id, title, content)
            app.logger.debug('board_post() - %s' % str(params))

            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                INSERT INTO tbboard (u_id, title, content) VALUES (?, ?, ?);
            ''', params)

            con.commit()
            con.close()
            return redirect(url_for('index'))
        else:
            u_name = session['u_name']
            return render_template('board_post.html', u_name = u_name)
    else:
        return render_template('user_notlogin.html')

# 게시판 기능 - 게시판_글 수정
@app.route('/board/<int:board_id>/update', methods=['GET','POST'])
def board_update(board_id):
    if isLogin():
        if request.method == 'GET':
            u_id = session['u_id']
            params = (board_id,)
            app.logger.debug('board_update() - %s' % str(params))
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                SELECT b_id, b.u_id, u_name, title, content, b.add_at, b.upd_at
                FROM tbboard AS b INNER JOIN tbuser AS u
                ON b.u_id = u.u_id
                WHERE b.use_flag = 'Y' AND b.u_id = ?;
            ''',params)
            rows = cur.fetchall()            
            app.logger.debug('board_update() - %s' %str(params))
            con.close()
            
            board_view = rows[0]
            if len(rows) == 1:
                u_name = session['u_name']
                if u_id == board_view[1]:
                    return render_template('board_update.html',board_view=board_view, u_id = u_id, u_name = u_name)
                else:
                    return render_template('user_notlogin.html')
            else:
                return render_template('user_notlogin.html')
        
        else:
            u_id = session['u_id']
            b_id = int(request.form['b_id'])
            title = request.form['title']
            content = request.form['content']
            params = (title, content, b_id, u_id)
            app.logger.debug('board_update() - params: %s' % str(params))

            if b_id != board_id:
                return render_template('user_notlogin.html')
            
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                UPDATE tbboard SET title=?, content=?, upd_at=DATETIME('now', 'localtime')
                WHERE b_id=? AND u_id=?;
            ''', params)
            con.commit()
            con.close()
            return redirect(url_for('board_view', board_id = board_id))
    else:
        return render_template('user_notlogin.html')

# 게시판 기능 - 글_삭제
@app.route('/board/<int:b_id>/delete')
def board_delete(board_id):
    if isLogin():
        u_id = session['u_id']
        params = (board_id, u_id)
        app.logger.debug('board_delete() - %s' %str(params))
        
        con = sqlite3.connect('mywebsite_createtables')
        cur = con.cursor()
        cur.execute('''
            UPDATE tbboard SET use_flag = 'N', upd_dt=DATETIME('now', 'localtime')
            WHERE b_id=? AND u_id=?
        ''', params)
        con.commit()
        con.close()
        return redirect(url_for('index'))
    else:
        return render_template('user_notlogin.html')

# 게시판 기능 - 게시판_글보기
@app.route('/board/<int:board_id>')
def board_view(board_id):
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        u_id = session['u_id']
        params = (board_id,)
        app.logger.debug('board_view() - %s' % str(params))
        con=sqlite3.connect('mywebsite_createtables')
        cur=con.cursor()
        cur.execute('''
        SELECT b_id, b.u_id, u_name, title, content, b.add_dt, b.upd_dt
        FROM tbboard b INNER JOIN tbuser u
        ON b.u_id = u.u_id
        WHERE b.use_flag='Y' AND b_id=?;
            ''', params)
        rows=cur.fetchall()
        app.logger.debug('board_view() - %s' % str(rows))
        con.close()
        board_view = rows[0]
        if len(rows) == 1:  # 로그인 정상
            u_name=session['u_name']
            return render_template('board_view.html', board_view=board_view, u_id=u_id, u_name=u_name)
        else:
            return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯
    else:                               # 로그인 되어 있지 않다면
        return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯
    

# admin기능 - 파일 업로드

def createtables():
    con = sqlite3.connect('mywebsite_createtables')
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
   # createtables()
   app.run(host='0.0.0.0', port=5000, debug=True)
