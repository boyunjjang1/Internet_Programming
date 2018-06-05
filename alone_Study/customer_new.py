from flask import Flask, render_template, url_for, redirect, request
import sqlite3
import tables

app = Flask(__name__)

@app.route('/join', methods=['GET','POST'])
def customer_new():
    if(request.method == 'POST'):
        u_id = request.form['id']
        u_name = request.form['name']
        u_pw = request.form['pw']
