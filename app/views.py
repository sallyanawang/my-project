from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/task1')
def task1():
    return render_template("task1.html")

@app.route('/task2')
def task2():
    return render_template("task2.html")
	
@app.route('/task3')
def task3():
    return render_template("task3.html")
	
@app.route('/task4')
def task4():
    return render_template("task4.html")
	
@app.route('/task5')
def task5():
    return render_template("task5.html")
	
@app.route('/task6')
def task6():
    return render_template("task6.html")