from flask import Flask, render_template, url_for, redirect, request
import sqlite3
import study9

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('customer_list'))


# 회원 목록 조회
@app.route('/customers/', methods=['GET'])
def customer_list():
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('select * from customer ORDER BY u_id DESC;')
    rows = cur.fetchall()
    return render_template('customer_list.html', rows=rows)


# a tag 는 get방식으로 넘어간다
@app.route('/customers/new', methods=['GET','POST'])
def customer_new():
    err = None
    if(request.method == 'POST'):
        u_name = request.form['u_name']
        gender = request.form['gender']
        age = request.form['age'] # 우선 튜플로 값을 넣는다.
        params = (u_name, gender, age)
        app.logger.debug(u_name, gender, age)

        con = sqlite3.connect('myshop')
        cur = con.cursor()
        cur.execute('''
        INSERT INTO (u_name, gender, age) VALUES (?,?,?);
        ''', params)
        con.commit()
        con.close()
        return redirect(url_for('customer_list'))
    
    return render_template('customer_new.html', err=err)

@app.route('/customers/delete/<int:u_id>')
def customer_delete(u_id):
    u_id = int(u_id)
    params = (u_id,) # , 를 안찍으면 튜플이 안되기 때문에! !!
    app.logger.debug(u_id)
    
    con = sqlite3.connect('myshop')
    cur = con.cursor()
    cur.execute('DELETE FROM customer WHERE u_id=?;',params)
    con.commit()
    con.close()
    return redirect(url_for('customer_list'))


if __name__ == '__main__':
    # study9.createTable()
    app.run(host='0.0.0.0',port=5000,debug=True)