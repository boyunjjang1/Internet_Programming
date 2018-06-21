import os
from flask import Flask, render_template, url_for, redirect, request, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
import sqlite3

# 파일업로드

UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16 MB, byte 단위
app.secret_key = 'super secret key'

def allowed_file(filename): # 업로드 할 때 확장자 제한 체크 함수
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            app.logger.debug('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '': # 파일명이 없다는거는 보낸것이 없다는것, 파일안보냈을 때 에러처리
            app.logger.debug('No selected file') 
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # 여기서 한글이 깨짐
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # form tag에서 받아온 binary Data를 임시로 저장함
            product = filename
            p_name = request.form["p_name"]
            price = request.form["price"]
            img_path = app.config['UPLOAD_FOLDER'] + product
            kind = request.form["cate"]
            params = (p_name, price, img_path, kind)
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                INSERT INTO tbproduct (p_name, price, img_path, kind) VALUES (?, ?, ?, ?);
            ''', params)
            con.commit()
            con.close()
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('newfile.html')
    # '''
    # <!doctype html>
    # <meta charset="UTF-8">
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method="post" enctype="multipart/form-data">
    #   <input type="file" name="file">
    #   이름 : <input type="text" name="p_name">
    #   가격 : <input type="text" name="price">
    #   <input type="submit" value="Upload">
    # </form>
    # '''

# 메인화면
# 회원기능 - 로그인
@app.route('/', methods=['GET','POST'])
def index():
    u_name = None
    login_error = None

    connection = sqlite3.connect('mywebsite_createtables')
    cur = connection.cursor()
    cur.execute('''
        SELECT p_id, p_name, price, img_path FROM tbproduct LIMIT 12;
    ''')
    products = cur.fetchall()
    connection.close()

    if isLogin():
        return render_template('index.html', u_name = session['u_name'], login_error = login_error, products = products)
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
            rows = cur.fetchall()
            con.close()
            app.logger.debug('index() -%s' % str(rows))
            if len(rows) == 1:
                session['u_id'] = rows[0][0]
                session['u_name'] = rows[0][1]
                return redirect(url_for('index'))
            else:
                login_error = '로그인에 실패하셨습니다.'
                return render_template('index.html', u_name = u_name, login_error = login_error, products = products)
        else:
            return render_template('index.html', u_name = u_name, login_error = login_error, products = products)

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
            FROM tbuser WHERE u_id=?; 
        ''', params)
        rows = cur.fetchall()
        app.logger.debug('index() - %s' % str(rows))
        con.close()
        user_info = rows[0]
        if len(rows) == 1:
            return render_template('user_profile.html', user_info = user_info)
        else:
            return render_template('user_notlogin.html')
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
            cur = con.cursor()
            cur.execute('''
                SELECT u_id, input_id, email, pw, u_name, gender, birth, u_tel, u_live, sns_inform, add_at, upd_at
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
                UPDATE tbuser SET email=?, pw=?, u_name=?, gender=?, birth=?, u_tel=?, u_live=?, sns_inform=?;
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
            SELECT b_id, u_name, title, b.add_at, visit FROM tbboard AS b
            INNER JOIN tbuser AS u ON b.u_id = u.u_id
            WHERE b.use_flag = 'Y' ORDER BY b_id DESC LIMIT 10 OFFSET ?;
            ''', params)
    else:
        params = (keyword, keyword, offset)
        cur.execute('''
            SELECT b_id, u_name, title, b.add_at, visit FROM tbboard AS b
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
            params = (u_id, board_id,)
            app.logger.debug('board_update() - %s' % str(params))
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                SELECT b_id, b.u_id, u_name, title, content, b.add_at, b.upd_at 
                FROM tbboard AS b INNER JOIN tbuser AS u 
                ON b.u_id = u.u_id 
                WHERE b.use_flag = 'Y' AND b.u_id = ? AND b_id = ?;
            ''',params)
            rows = cur.fetchall()            
            app.logger.debug('board_update() - %s' % str(params))
            app.logger.debug('--------------------------------- %d' % len(rows))
            con.close()

            app.logger.debug(str(rows))
            board_view = rows
            if len(rows) == 1:
                u_name = session['u_name']
                if str(u_id) == str(board_view[0][1]):
                    return render_template('board_update.html',board_view=board_view[0], u_id = u_id, u_name = u_name)
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
@app.route('/board/<int:board_id>/delete')
def board_delete(board_id):
    if isLogin():
        u_id = session['u_id']
        params = (board_id, u_id)
        app.logger.debug('board_delete() - %s' %str(params))
        
        con = sqlite3.connect('mywebsite_createtables')
        cur = con.cursor()
        cur.execute('''
            UPDATE tbboard SET use_flag = 'N', upd_at=DATETIME('now', 'localtime')
            WHERE b_id=? AND u_id=?;
        ''', params)
        con.commit()
        con.close()
        return redirect(url_for('index'))
    else:
        return render_template('user_notlogin.html')

# 게시판 기능 - 게시판_글보기
@app.route('/board/<int:board_id>', methods=['GET','POST'])
def board_view(board_id):
    if isLogin(): #'u_id' in session:   # 로그인 되어 있다면
        u_id = session['u_id']
        params = (board_id,)
        app.logger.debug('board_view() - %s' % str(params))
        con=sqlite3.connect('mywebsite_createtables')
        cur=con.cursor()
        cur.execute('''
        SELECT b_id, b.u_id, u_name, title, content, b.add_at, b.upd_at, visit
        FROM (tbboard b INNER JOIN tbuser u
        ON b.u_id = u.u_id)
        WHERE b.use_flag='Y' AND b_id=?;
            ''', params)
        rows = cur.fetchall()
        cur.execute('''
            UPDATE tbboard SET visit = visit + 1 WHERE b_id=?;
        ''', params)
        con.commit()
        app.logger.debug('board_view() - %s' % str(rows))
        con.close()
        board_view = rows[0] 
        app.logger.debug(board_view)

        con = sqlite3.connect('mywebsite_createtables')
        cursor = con.cursor()
        cursor.execute('''
            SELECT b_id, u_name, naeyong FROM comment WHERE b_id = ? ORDER BY b_id ASC;
        ''', params)
        comment_table = cursor.fetchall()
        con.close()

        if len(comment_table) != 0:
            comment_view = comment_table
        else:
            comment_view = None

        if request.method == 'POST':
            u_name = session['u_name']
            naeyong = request.form["naeyong"]
            params = (board_id, u_name, naeyong)
            con = sqlite3.connect('mywebsite_createtables')
            cur = con.cursor()
            cur.execute('''
                INSERT INTO comment (b_id, u_name, naeyong) VALUES (?,?,?);
            ''', params)
            con.commit()
            con.close()
            return redirect(url_for('board_view', board_id=board_id))

        if len(rows) == 1:  # 로그인 정상
            u_name=session['u_name']
            return render_template('board_view.html', board_view=board_view, u_id=u_id, board_id = board_view[0], u_name=u_name, comment_view = comment_view)
        else:
            return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯
    else:                               # 로그인 되어 있지 않다면
        return render_template('user_notlogin.html')   # 잘못된 페이지 접근이라고 보여주고 이동해도 될듯

@app.route('/dailylook')
def dailylook():
    con = sqlite3.connect('mywebsite_createtables')
    cur = con.cursor()
    cur.execute('''
        SELECT p_name, price, img_path, p_id FROM tbproduct WHERE kind='dailylook';
    ''')
    rows = cur.fetchall()
    con.close()

    # if request.method == 'POST':
    #     choice_product = request.form["choice"]

    #     con = sqlite3.connect('mywebsite_createtables')
    #     cur = con.cursor()
    #     cur.execute('''
    #         SELECT p_id FROM tbproduct WHERE p_id = ?;
    #     ''',choice_product)
        

    return render_template('dailylook.html', rows = rows)

@app.route('/top')
def top():
    con = sqlite3.connect('mywebsite_createtables')
    cur = con.cursor()
    cur.execute('''
        SELECT p_name, price, img_path, p_id FROM tbproduct WHERE kind='top';
    ''')
    rows = cur.fetchall()
    con.close()

    return render_template('top.html',rows = rows)

@app.route('/skirt')
def skirt():
    con = sqlite3.connect('mywebsite_createtables')
    cur = con.cursor()
    cur.execute('''
        SELECT p_name, price, img_path, p_id FROM tbproduct WHERE kind='skirt';
    ''')
    rows = cur.fetchall()
    con.close()
    return render_template('skirt.html', rows = rows)

@app.route('/acc')
def acc():
    con = sqlite3.connect('mywebsite_createtables')
    cur = con.cursor()
    cur.execute('''
        SELECT p_name, price, img_path, p_id FROM tbproduct WHERE kind='acc';
    ''')
    rows = cur.fetchall()
    con.close()
    return render_template('skirt.html', rows = rows)


# def createtables():
#     con = sqlite3.connect('mywebsite_createtables')
#     cur = con.cursor()
#     cur.execute('''
#         DROP TABLE IF EXISTS tbuser;
#     '''
#     cur.execute('''
#         DROP TABLE IF EXISTS tbboard;
#     ''')
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS tbuser(
#         u_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         input_id TEXT NOT NULL UNIQUE,
#         email TEXT NULL UNIQUE,
#         pw TEXT NOT NULL,
#         u_name TEXT NOT NULL,
#         gender TEXT NULL,
#         birth TEXT NULL,
#         u_tel INTEGER NULL,
#         u_live TEXT NULL,
#         sns_inform TEXT NULL,
#         add_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
#         upd_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
#         use_flag TEXT DEFAULT('Y')
#         );
#     ''')
#     con.commit()
#     pass



if __name__ == '__main__':
   # createtables()
   # session.clear()
   app.run(host='0.0.0.0', port=5000, debug=True)
   
