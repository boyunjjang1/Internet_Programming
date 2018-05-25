from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],request.form['password']):
            return log_the_user_in(request.form['username'])
        
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)



def valid_login(un,pw):
    # 여기서 DB를 연결하여서 해당 사용자가 있는지 확인하면 됨
    if(un=='redcarrot' and pw == '1234'):
        return True
    
    else:
        return False


def log_the_user_in(username):
    # 여기서 정상적으로 로그인 된 사용자를 위한 페이지를 보여주면 됨
    return '%s님 환영합니다.' % username

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)