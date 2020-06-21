from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'the random string'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    engine = create_engine('mysql+pymysql://root:Veni$ramya143@localhost/crudapplication')
    conn = engine.connect()
else:
    app.debug = False
    engine = create_engine('postgres://kujrrtuapcyldt:05d9a283c5520b094485621b89ab066d459a6a187882d2533e123c1f6e22d2d3@ec2-52-20-248-222.compute-1.amazonaws.com:5432/d6mefonigbjjl2')
    conn = engine.connect()

def CreateTable():
    conn .execute ('''
    CREATE TABLE IF NOT EXISTS students (
    id int NOT NULL AUTO_INCREMENT,   
    name varchar(255),
    email varchar(255),
    phone varchar(10),
    PRIMARY KEY (id)
);
    
    ''')
CreateTable()
@app.route('/')
def Index():
    result = conn.execute('SELECT * FROM students')
    data = result.fetchall()
    result.close()
    return render_template('index.html',students = data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        return redirect(url_for('Index'))

@app.route('/update', methods = ['POST','GET'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn.execute("""
        UPDATE  students
        SET name=%s,email=%s,phone=%s
        WHERE id=%s
        """, (name,email,phone,id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['POST','GET'])
def delete(id_data):
        conn.execute("""
        DELETE FROM students
        WHERE id=%s 
        """, (id_data))
        flash("Data Deleted Successfully")
        return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run()
