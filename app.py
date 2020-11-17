from flask import Flask, render_template, request, redirect
import pymysql

conn = pymysql.connect(host='ahmo.kro.kr', 
                        port=3306, 
                        db='pyapp', 
                        user='root', 
                        passwd='java1004')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def msg_list():
    cursor = conn.cursor()
    cursor.execute('SELECT msg_id, msg_text FROM msg')
    msg_list = cursor.fetchall()
    print(msg_list)
    return render_template('msg_list.html', msg_list = msg_list)

@app.route('/add_msg', methods=['GET', 'POST'])
def add_msg():
    if request.method == 'GET':
        return render_template('add_msg.html')
    elif request.method == 'POST':
        msg_text = request.form['msg_text']
        cursor = conn.cursor()
        cursor.execute('INSERT INTO msg(msg_text) VALUES(%s)', [msg_text])
        conn.commit()

        return redirect('/')

@app.route('/del_msg/<msg_id>', methods=['GET'])
def del_msg(msg_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM msg WHERE msg_id=%s', [msg_id])
    conn.commit()

    return redirect('/')


@app.route('/mod_msg/<msg_id>', methods=['GET', 'POST'])
def mod_msg(msg_id):
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('SELECT msg_id, msg_text FROM msg WHERE msg_id=%s',[msg_id])
        msg = cursor.fetchone()
        return render_template('mod_msg.html', msg=msg)
    elif request.method == 'POST':
        msg_id = request.form['msg_id']
        msg_text = request.form['msg_text']
        cursor = conn.cursor()
        cursor.execute('UPDATE msg SET msg_text=%s WHERE msg_id=%s', [msg_text, msg_id])
        conn.commit()

        return redirect('/')

        

app.run(host='127.0.0.1', port=80)


