from flask import Flask
from flask import render_template
from pymysql import connect
from flask import request
from flask import make_response, send_from_directory

app = Flask(__name__)


@app.route('/download')
def hello():
    return render_template('download.html')


@app.route('/get/<category>', methods=['GET', 'POST'])
def get_it(category):
    con = connect('localhost', 'root', '123456', 'spider')
    cur = con.cursor()
    if request.method == 'POST':
        if request.form['need_correct'] != '':
            # category=request.form['category']
            need_correct = request.form['need_correct']
            corrected = request.form['corrected']
            sql_2 = 'SELECT * from yuliao_yuan WHERE name="%s" ORDER BY pk_id DESC' % need_correct
            cur.execute(sql_2)
            cat_num = len(cur.fetchall())
            if cat_num == 0:
                sql = 'INSERT INTO yuliao_yuan(category, name, url) VALUES ("%s","%s","%s")' % (
                category, need_correct, corrected)
                cur.execute(sql)
                con.commit()
            sql = 'SELECT * from yuliao_yuan WHERE category="%s" ORDER BY pk_id DESC' % category
            cur.execute(sql)
            values = cur.fetchall()
        else:
            sql = 'SELECT * from yuliao_yuan WHERE category="%s" ORDER BY pk_id DESC' % category
            cur.execute(sql)
            values = cur.fetchall()
    if request.method == 'GET':
        sql = 'SELECT * from yuliao_yuan WHERE category="%s" ORDER BY pk_id DESC' % category
        cur.execute(sql)
        values = cur.fetchall()
    values = [values, category]
    con.close()
    return render_template('title1.html', values=values)


@app.route('/category', methods=['GET', 'POST'])
def get_category():
    con = connect('localhost', 'root', '123456', 'spider')
    cur = con.cursor()
    sql_1 = 'SELECT * from category  ORDER BY pk_id DESC'
    if request.method == 'POST':
        if request.form['need_correct'] != '':
            # category=request.form['category']
            need_correct = request.form['need_correct']
            # corrected=request.form['corrected']
            sql_2 = 'SELECT * from category WHERE category="%s" ORDER BY pk_id DESC' % need_correct
            cur.execute(sql_2)
            cat_num = len(cur.fetchall())
            # cat_num=1
            if cat_num == 0:
                sql = 'INSERT INTO category(category,url) VALUES ("%s","%s")' % (need_correct, '/get/%s' % need_correct)
                cur.execute(sql)
                con.commit()
            cur.execute(sql_1)
            values = cur.fetchall()
        else:
            cur.execute(sql_1)
            values = cur.fetchall()
    if request.method == 'GET':
        cur.execute(sql_1)
        values = cur.fetchall()
        values = values
    con.close()
    return render_template('category.html', values=values)


@app.route('/send_file1')
def post_it():
    filename = 'text_101_fenci.txt'
    directory = r'D:\语料库\\'
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
