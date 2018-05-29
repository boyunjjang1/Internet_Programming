from flask import Flask, url_for, redirect, make_response
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login')) # login 페이지로 이동
    

@app.route('/login')
def login():
    return 'login page'


@app.errorhandler(404) # 오류처리
def page_not_found(error):
    resp = make_response('Page not found',404) # 본문 처리
    resp.headers['X-Something'] = 'A value' # 어떤 의미로 보낸건지 header에다가도 보냄
    return resp;



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)