from flask import Flask
from flask import render_template
from pymysql import connect
from flask import request
from flask import make_response,send_from_directory


app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello'


@app.route('/get',methods=['GET','POST'])
def get_it():
    con=connect('localhost','root','123456','text_cleaning')
    cur=con.cursor()
    if request.method=='POST':
        if request.form['need_correct']!='':
            need_correct=request.form['need_correct']
            corrected=request.form['corrected']
            sql='INSERT INTO therule(need_correct, corrected) VALUES ("%s","%s")'%(need_correct,corrected)
            cur.execute(sql)
            con.commit()
            sql = 'SELECT * from therule ORDER BY pk_id DESC'
            cur.execute(sql)
            values = cur.fetchall()
        else:
            sql = 'SELECT * from therule ORDER BY pk_id DESC'
            cur.execute(sql)
            values = cur.fetchall()
    if request.method=='GET':
        sql = 'SELECT * from therule ORDER BY pk_id DESC'
        cur.execute(sql)
        values = cur.fetchall()
    con.close()
    return render_template('title1.html',values=values)

@app.route('/send_file1')
def post_it():
    filename='correct.ibd'
    directory=r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\text_cleaning\\'
    response=make_response(send_from_directory(directory,filename,as_attachment=True))
    return response

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
