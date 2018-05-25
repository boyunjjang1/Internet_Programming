from flask import Flask, url_for, request
app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'login - post method'
    else:
        return 'login - get method'


@app.route('/user/<username>')
def profile(username):
    return '{0}\'s profile'.format(username)


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('static', filename='style.css'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)