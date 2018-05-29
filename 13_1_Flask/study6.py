from flask import Flask, session, redirect, url_for, escape, request
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # session을 사용할거면 secret_key 를 반드시 넣어줘야함 !! , b ==? byte형태로 data를 처리할 것

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s <a href="%s">To logout</a>' % \
            (escape(session['username']), url_for('logout'))
    
    return 'You are not logged in <a href="%s">To login</a>' % url_for('login')

    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    
    return '''
            <form method='post'> 
                <p><input type='text' name='username'></p>
                <p><input type='submit' value='login'></p>
            </form>
        '''
        # action이 없으면 자기자신한테 보냄

@app.route('/logout')
def logout():
    session.pop('username', None)
    # return redirect(url_for('index')) --> 바로 점프
    return '<p>logout</p><a href="' + url_for('index') + '">goto /</a>'

    # session은 해당컴퓨터에 브라우저 별로 열 수 있다.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)