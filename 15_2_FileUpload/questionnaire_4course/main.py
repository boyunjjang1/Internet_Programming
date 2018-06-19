from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    error_msg = None
    statistic = None
    if request.method == 'GET':  
        return render_template('index.html', error_msg=error_msg)
    else:           # POST 일 때        
        try :
            # form 태그의 입력항목을 받아옴
            q1 = str(request.form['q1'])
            q2 = str(request.form['q2'])
            s_num = str(request.form['s_num'])
            name = request.form['name']
            email = request.form['email']

            if s_num.strip() == '' or name.strip() == '' or email.strip() == '':
                raise ValueError

            params = (q1, q2, s_num, name, email,)   # db에 쿼리 데이터 생성
            app.logger.debug(list(params))
        except:            
            error_msg = '입력된 항목을 선택하지 않았습니다.'
            app.logger.warning(error_msg)
        finally:
            if error_msg != None:
                return render_template('index.html', error_msg=error_msg)
        
        try:
            # 데이터베이스에 해당 정보를 업데이트함
            con=sqlite3.connect('q.sqlite3')
            cur=con.cursor()
            cur.execute('''
                UPDATE tbQ 
                SET q1 = ?, 
                    q2 = ?, 
                    upd_dt = DATETIME('now', 'localtime'), 
                    use_flag = 'N'
                WHERE s_num = ? 
                AND name = ? 
                AND email = ? 
                AND use_flag = 'Y' 
                ''', params)
            app.logger.debug('cur.rowcount: %s' % str(cur.rowcount))
            con.commit()
            if cur.rowcount != 1:   # 레코드가 반영되지 않은 경우
                raise ValueError
        except: 
            error_msg = '해당 사용자 정보가 불일치하거나 혹은 이미 설문조사를 하여 진행할 수가 없습니다.'
            app.logger.warning(error_msg)            
        finally:
            con.close()
            if error_msg != None:
                return render_template('index.html', error_msg=error_msg)            
    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    try:
        # 설문조사 결과를 출력
        r = result()

        con=sqlite3.connect('q.sqlite3')
        cur=con.cursor()
        cur.execute('''
        SELECT COUNT(*) as student_total,
        SUM( CASE WHEN use_flag='Y' THEN 1 ELSE 0 END ) as student_y_cnt, 
        SUM( CASE WHEN use_flag='N' THEN 1 ELSE 0 END ) as student_n_cnt, 
        SUM( CASE WHEN q1='Y' THEN 1 ELSE 0 END ) as q1_y, 
        SUM( CASE WHEN q1='N' THEN 1 ELSE 0 END ) as q1_n, 
        SUM( CASE WHEN q1 is null THEN 1 ELSE 0 END ) as q1_null, 
        SUM( CASE WHEN q2='1' THEN 1 ELSE 0 END ) as q2_1, 
        SUM( CASE WHEN q2='2' THEN 1 ELSE 0 END ) as q2_2, 
        SUM( CASE WHEN q2='3' THEN 1 ELSE 0 END ) as q2_3, 
        SUM( CASE WHEN q2 is null THEN 1 ELSE 0 END ) as q2_null
        FROM tbQ;
        ''')
        rows=cur.fetchall()
        app.logger.debug('rows[0]: %s' % str(rows[0]))
        if len(rows) == 1: # 데이터가 정상이라면
            r.student_total = rows[0][0]
            r.student_y_cnt = rows[0][1]
            r.student_n_cnt = rows[0][2]
            r.q1_y = rows[0][3]
            r.q1_n = rows[0][4]
            r.q1_null = rows[0][5]
            r.q2_1 = rows[0][6]
            r.q2_2 = rows[0][7]
            r.q2_3 = rows[0][8]
            r.q2_null = rows[0][9]
    except:
        app.logger.warning('오류!!!')
        pass
    finally:
        con.close()

    return render_template('result.html', r=r)

class result:
    student_total = 0
    student_y_cnt = 0
    student_n_cnt = 0
    q1_y = 0
    q1_n = 0
    q1_null = 0
    q2_1 = 0
    q2_2 = 0
    q2_3 = 0
    q2_null = 0

def initDatabase():
    # Questionnaire.sqlite3
    con=sqlite3.connect('q.sqlite3')
    cur=con.cursor()
    # tbQuestionnaire
    cur.execute('''
        DROP TABLE IF EXISTS tbQ;
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tbQ (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            s_num TEXT NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            email TEXT NOT NULL,
            q1 TEXT NULL,
            q2 TEXT NULL, 
            upd_dt DATETIME DEFAULT (DATETIME('now', 'localtime')),
            use_flag TEXT DEFAULT ('Y')
        );        
        ''')
    cur.execute('''
        INSERT INTO tbQ (s_num, name, class, email) VALUES 
        ('12130001', '홍길동', '002', '1@2.3'), 
        ('12130001', '웹코딩', '002', '1@2.3'),
        ('12130003', '귀찮음', '002', '1@2.3');
    ''')
    con.commit()
    con.close()

if __name__ == '__main__':
    # initDatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)
