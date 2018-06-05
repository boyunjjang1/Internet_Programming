from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 메인화면
# 회원기능 - 로그인

# 회원기능 - 회원등록

# 회원기능 - 로그아웃

# 로그아웃 수행

# 로그인 여부

# 회원 기능 - 회원 정보보기

# 회원기능 - 회원 수정

# 회원기능 - 회원 탈퇴





if __name__ == '__main__':
   # createtables()
   app.run(host='0.0.0.0', port=5000, debug=True)