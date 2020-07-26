#!/usr/bin/python3.5
from flask import *
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
#from Model.dModel import *
#from functools import wraps
import os
import requests
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
#from flask_sslify import SSLify
#import ssl
#from OpenSSL import SSL
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import ast
from os import listdir
from os.path import isfile, join
import subprocess
import datetime
import pytz
from flask_required_args import required_data


#context = SSL.Context(ssl.OP_NO_SSLv3)
#context = ssl.create_default_context()
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')
#context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'resources/udara.com.crt')
key = os.path.join(os.path.dirname(__file__), 'resources/udara.com.key')
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
login_manager = LoginManager()
#sslify = SSLify(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "Please LOG IN"
login_manager.login_message_category = "info"
quest_id = ''
name = ''
inform = ''
fb_set = 0
email_send_num = 0
new_username = ''
socket = SocketIO(app)

subprocess.Popen("python3 /home/pi/ktanem/del_post.py", shell=True)

def query_user(username):
    user = UserAccounts.query.filter_by(UserName=username).first()
    if user:
        return True
    return False


def query_FBuser(FBuserID):
    FBuser = UserAccounts.query.filter_by(FBuserID=FBuserID).first()
    if FBuser:
        return True
    return False


@login_manager.user_loader
def user_loader(username):
    if query_user(username) or query_FBuser(username):
        user = User()
        user.id = username
        return user
    return None


@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    global new_username
    user_id = session.get('user_id')
    user = UserAccounts.query.filter_by(FBuserID=user_id).first()

    if user:
        if user.UserName == None:
            data = requests.get(
                "https://graph.facebook.com/me?fields=id,name,email&access_token=" + user.FBAccessToken)
            if data.status_code == 200:
                user.UserName = data.json()['name']
                db.session.add(user)
                db.session.commit()
                FBuser = data.json()['name']
        else:
            FBuser = user.UserName
    else:
        FBuser = ""

    return render_template("index.html", FBuser=FBuser)

@app.route('/server_on')
def server_on():
    subprocess.Popen("sudo systemctl restart tarber", shell=True)
    #os.makedirs("/home/gor/tarber/testmy11", mode=0o777)
    #os.chmod("testmy1", 777)
    return "11"


@app.route('/login', methods=['GET', 'POST'])
def login():
    global new_username
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    if request.method == 'GET':
        asd = ""
        if getsession() == "not":
            asd = 0;
        else:
            asd = getsession()
        return render_template("login.html", user=asd)

    if request.method == 'POST':
        print("YO")
        for i in range(len(c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())):
            if request.form['username'] ==  c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]:
                print("YOO")
                print(request.form['password'])
                if(request.form['password'][-1] == "!" and request.form['password'][-2] != "?" and request.form['password'][-3] == "!"):
                    print("man")
                    my_pass = list(request.form['password'])
                    my_pass.pop(-1)
                    my_back = 0
                    my_back = int(my_pass[-1])
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    print(my_pass)
                    my_fin_pass = ""
                    my_fin_pass = my_fin_pass.join(my_pass)
                    print(request.form['my_url_bc'])
                    some_val = request.form['my_url_bc']
                    if my_fin_pass ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        print("finall")
                        return redirect("/quest?id=" + str(my_back), code=302)

                  
                elif(request.form['password'][-1] == "!" and request.form['password'][-3] == "!" and request.form['password'][-2] == "?"):
                    print("man")
                    my_pass = list(request.form['password'])
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    print(my_pass)
                    my_fin_pass = ""
                    my_fin_pass = my_fin_pass.join(my_pass)
                    if my_fin_pass ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        print("finall")
                        return redirect("/noto?create=1", code=302)


                else:
                    if request.form['password'] ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        return redirect(url_for('noto'))
    return redirect(url_for('lg_dp'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'not'

@app.route('/valod', methods=['GET', 'POST'])
def valod():
    global break_sesion
    print(1)
    for i in range(5):
        while 'user' in session:
            print(getsession())
            session.pop('user', None)
            print(getsession())
    print(getsession())
    return getsession()

@app.route('/do_log', methods=['GET', 'POST'])
def do_log():
    print(getsession())
    while 'user' in session:
        print(getsession())
        session.pop('user', None)
        print(13)
    return "11"


@app.route('/user/<inform1>', methods=['GET', 'POST'])
def user(inform1):
    global inform
    inform = inform1
    return "11"

@app.route('/name/<name1>', methods=['POST', 'GET'])
def name(name1):
    global name
    name = name1
    check_fb()
    return "11"

def add_sm(us_id):
    #subprocess.Popen("sudo chmod 777 /home/gor/tarber/static/user_image", shell=True)
    #subprocess.Popen("mkdir /home/gor/tarber/static/user_image/" + us_id, shell=True)
    #subprocess.Popen("sudo chmod 777 /home/gor/tarber/static/user_image/" + us_id, shell=True)
    os.system("python3 /home/gor/tarber/add.py " + us_id)
    #os.system("sudo")
@app.route('/social_add/<us_id>/<us_phone>/<us_birth>/<us_gen>', methods=['POST', 'GET'])
def social_add(us_id, us_phone, us_birth, us_gen):
    conn1 = sqlite3.connect("kill1.db")
    c1 = conn1.cursor()
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    session['user'] = us_id
    session['user'] = us_id
    not_list = [['Welcome dear user'], []]
    user_info_f = c1.execute("SELECT * FROM un_reg WHERE id='" + us_id + "'").fetchall()[0]
    c.execute("CREATE TABLE IF NOT EXISTS " + us_id + " (name TEXT, surname TEXT, likes INT, posts TEXT, email TEXT, username TEXT, password TEXT, birth TEXT, gend TEXT, note TEXT)")
    password = user_info_f[2].replace("||", "/").replace("*", "?")
    c.execute('INSERT INTO ' + us_id + ' VALUES("' + user_info_f[1].split(" ")[0] + '", "' + user_info_f[1].split(" ")[1] + '", "' + '0' + '", "' + '[]' + '", "' + us_phone + '", "' + us_id + '", "' + password + '" , "' + us_birth + '" , "' + us_gen + '" , "' + str(not_list) +'")')
    import requests
    import shutil

    image_url = "https://" + password
    print(image_url)
    resp = requests.get(image_url, stream=True)
    #os.system("sudo chmod 777 /home/gor/tarber/static/user_image")
    os.makedirs("/home/gor/tarber/static/user_image/" + us_id, mode=0o777)
    #os.system("sudo chmod 777 /home/gor/tarber/static/user_image/" + us_id)
    #subprocess.Popen("sudo chmod 777 /home/gor/tarber/static/user_image", shell=True)
    #subprocess.Popen("mkdir /home/gor/tarber/static/user_image/" + us_id, shell=True)
    #subprocess.Popen("sudo chmod 777 /home/gor/tarber/static/user_image/" + us_id, shell=True)
    #add_sm(us_id)
    local_file = open('/home/gor/tarber/static/user_image/' + us_id + '/a.png', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp
    session['user'] = us_id
    session['user'] = us_id
    session['user'] = us_id
    session['user'] = us_id
    conn.commit()
    conn1.commit()
    return "11"


@app.route('/valodik/<name11>', methods=['POST', 'GET'])
def valodik(name11):
    global name
    name = name11
    check_fb()
    return "11"

@app.route('/check_if_exists/<user_idmy>/<us_name>/<us_image>/<us_email>', methods=['POST', 'GET'])
def check_if_exists(user_idmy, us_name, us_image, us_email):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.commit()
    for i in user_list:
        if i[0] == user_idmy:
            print("USER EXISTS")
            session['user'] = user_idmy
            session['user'] = user_idmy
            return jsonify("1")  
    #de_kill_me(user_idmy, us_name, us_image, us_email)               
    conn1 = sqlite3.connect("kill1.db")
    c1 = conn1.cursor()
    c1.execute("CREATE TABLE IF NOT EXISTS un_reg (id TEXT, name TEXT, image TEXT, email TEXT)")
    c1.execute("INSERT INTO un_reg VALUES ('" + str(user_idmy) + "', '" + str(us_name) + "', '" + str(us_image) + "', '" + str(us_email) + "')")
    conn1.commit()
    return jsonify("0")


def de_kill_me(user_idmy, us_name, us_image, us_email):
    conn = sqlite3.connect("kill1.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS un_reg (id TEXT, name TEXT, image TEXT, email TEXT)")
    c.execute("INSERT INTO un_reg VALUES ('" + str(user_idmy) + "', '" + str(us_name) + "', '" + str(us_image) + "', '" + str(us_email) + "')")
    conn.commit()

@app.route('/update_post/<ider>/<froom>/<to>/<time>/<money>/<car>/<space>/<phone>/<info11>', methods=['GET', 'POST'])
def update_post(ider, froom, to, time, money, car, space, phone, info11):
    conn = sqlite3.connect("db/post.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET fromo = '" + froom + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET too = '" + to + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET go_time = '" + time + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET money = '" + money + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET car = '" + car + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET free_space = '" + space + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET phone = '" + phone + "' WHERE id='" + str(ider) + "'")
    c.execute("UPDATE posts SET more_inf = '" + info11 + "' WHERE id='" + str(ider) + "'")
    conn.commit()
    return "11"

@app.route('/update_user_info/<curr_un>/<e_name>/<e_sur>/<e_phone>/<e_birth>/<e_uname>', methods=['GET', 'POST'])
def update_user_info(curr_un, e_name, e_sur, e_phone, e_birth, e_uname):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    c.execute("UPDATE " + curr_un + " SET name='" + e_name + "'")
    c.execute("UPDATE " + curr_un + " SET surname='" + e_sur + "'")
    c.execute("UPDATE " + curr_un + " SET email='" + e_phone + "'")
    c.execute("UPDATE " + curr_un + " SET birth='" + e_birth + "'")
    c.execute("UPDATE " + curr_un + " SET username='" + e_uname + "'")

    try:
        c.execute("ALTER TABLE '" + curr_un + "' RENAME TO '" + e_uname + "'")
    except:
        pass
    session['user'] = e_uname
    session['user'] = e_uname
    conn.commit()
    return "11"

@app.route('/check_fb/<fb_us_inf>/<fb_us_inf1>/<fb_us_inf2>/<fb_us_inf3>/<fb_us_inf4>', methods=['GET', 'POST'])
def check_fb(fb_us_inf, fb_us_inf1, fb_us_inf2, fb_us_inf3, fb_us_inf4):    
    print(fb_us_inf)
    print(fb_us_inf1)
    print(fb_us_inf2.replace("||", "/").replace("*", "?"))
    print(fb_us_inf3)
    print(fb_us_inf4)
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    curr_name = ''
    us_id = fb_us_inf
    name = fb_us_inf1.split(" ")[0]
    surname = fb_us_inf1.split(" ")[1]
    email = "NONE"
    
    password = "NONE"
    print(fb_us_inf)
    birth_dat = fb_us_inf4
    gend = fb_us_inf3
    not_list = [['Welcome dear user'], []]
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    password = fb_us_inf2.replace("||", "/").replace("*", "?")
    us_ida = "a" + us_id
    session['user'] = us_ida
    session['user'] = us_ida
    username = us_ida
    for i in user_list:
        if i[0] == us_ida:
            print("WTF")
            return "11"
    c.execute("CREATE TABLE IF NOT EXISTS " + us_ida + " (name TEXT, surname TEXT, likes INT, posts TEXT, email TEXT, username TEXT, password TEXT, birth TEXT, gend TEXT, note TEXT)")
    c.execute('INSERT INTO ' + us_ida + ' VALUES("' + name + '", "' + surname + '", "' + '0' + '", "' + '[]' + '", "' + email + '", "' + username + '", "' + password + '" , "' + birth_dat + '" , "' + gend + '" , "' + str(not_list) +'")')
    import requests
    import shutil
    image_url = "https://" + password
    print(image_url)
    resp = requests.get(image_url, stream=True)
    os.system("sudo chmod 777 /home/gor/tarber/static/user_image")
    os.system("mkdir /home/gor/tarber/static/user_image/" + us_ida)
    os.system("sudo chmod 777 /home/gor/tarber/static/user_image/" + us_ida)
    local_file = open('/home/gor/tarber/static/user_image/' + us_ida + '/a.png', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp
    #c.execute("CREATE TABLE IF NOT EXISTS " + name.replace(" ", "") + " (name TEXT, surname TEXT, likes INT, posts TEXT, token TEXT)")
    #c.execute('INSERT INTO ' + name.replace(" ", "") + ' VALUES("' + name.split(' ')[0] +'", "' + name.split(' ')[1] + '", "' + '0' + '", "' + '{}' + '", "' + inform.split('$')[0] + '")')
    print('vsyo')
    conn.commit()
    return "11"
    #login()

@app.route("/add_new_phone/<user>/<new_phone>", methods=['GET', 'POST'])
def add_new_phone(user, new_phone):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    nums = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][4])
    nums.append(str(new_phone))
    c.execute('UPDATE ' + user + ' SET email="' + str(nums) + '"')
    conn.commit()
    return "11"

@app.route("/delete_user_num/<user>/<phone_id>", methods=['GET', 'POST'])
def delete_user_num(user, phone_id):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    nums = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][4])
    nums.pop(int(phone_id))
    c.execute('UPDATE ' + user + ' SET email="' + str(nums) + '"')
    conn.commit()
    return "11"

@app.route("/user_change_lang/<user>/<lang>", methods=['GET', 'POST'])
def user_change_lang(user, lang):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    c.execute("UPDATE " + user + " SET lang='" + lang + "'")
    conn.commit()
    return "11"

@app.route("/main", methods=['GET', 'POST'])
def main():
    print("axxc")
    return render_template("main.html")

@app.route("/temp", methods=['GET', 'POST'])
def temp():
    return render_template("temp.html")

@socket.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    return "11"

@socket.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    return "11"

@app.route("/my_booked", methods=['GET', 'POST'])
def my_booked():
    asd = ""
    if getsession() == "not":
        asd = 0;
    else:
        asd = getsession()
    if getsession() != "not":
        return render_template("my_booked.html", user=asd)
    else:
        return render_template("login.html", user=asd)

@app.route("/my_pos", methods=['GET', 'POST'])
def my_pos():
    asd = ""
    if getsession() == "not":
        asd = 0;
    else:
        asd = getsession()
    if getsession() != "not":
        return render_template("my_pos.html", user=asd)
    else:
        return render_template("login.html", user=asd)

@app.route("/test", methods=['GET', 'POST'])
def test():
    print("axxc")
    return render_template("new_quest.html")

@app.route("/smthi", methods=['GET', 'POST'])
def smthi():
    emit('asdfg', {'data': 'Hello World'})
    return "11"


@app.route("/user_infon", methods=['GET', 'POST'])
def user_infon():
    return render_template("user_info.html")

@app.route("/social_rg", methods=['GET', 'POST'])
def social_rg():
    return render_template("social_register.html")

@app.route("/noto", methods=['GET', 'POST'])
def noto():
    if getsession() != "not":
        return render_template("noto.html")
    else:
        asd = ""
        if getsession() == "not":
            asd = 0;
        else:
            asd = getsession()
        return render_template("login.html", user=asd)        

@app.route("/lg_dp", methods=['GET', 'POST'])
def lg_dp():
    return render_template("login1.html")

@app.route("/rg_dp", methods=['GET', 'POST'])
def rg_dp():
    return render_template("regist.html")

@app.route('/emailver/<email_inform>/<code>', methods=['GET', 'POST'])
def emailver(email_inform, code):
    global email_send_num
    email = 'sahak.sahakyan2017@gmail.com'
    password = 'newdvbt2'
    subject = 'Verification'
    send_num = random.randint(10000, 99999)
    email_send_num = send_num
    email_code()
    send_to_email = email_inform.split('$')[0]
    message = "Dear " + email_inform.split('$')[1] + " your verification code is " + str(code)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
    return "11"

@app.route('/email_code', methods=['GET', 'POST'])
def email_code():
    global email_send_num
    return jsonify(email_send_num)

@app.route('/user_login_info', methods=['GET', 'POST'])
def user_login_info():
    return jsonify(getsession())

@app.route('/read_notefic/<notefic_username>', methods=['GET', 'POST'])
def read_notefic(notefic_username):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    a = ast.literal_eval(c.execute("SELECT * FROM " + notefic_username).fetchall()[0][9].strip())
    if len(a) > 0:
        send_list = []
        l = a[1]
        for i in a[0]:

            l.append(i)
            print(i, l)
        send_list = [[], l]
        print(send_list)
        c.execute('UPDATE ' + notefic_username + ' SET note = " '  + str(send_list) +  '"')
        conn.commit()
    return "11"

@app.route('/add_new_user/<new_user_inform>/<lang>', methods=['GET', 'POST'])
def add_new_user(new_user_inform, lang):
    global new_username
    import sqlite3
    conn3 = sqlite3.connect("db/user.db")
    c3 = conn3.cursor()
    name = new_user_inform.split('|||')[0]
    surname = new_user_inform.split('|||')[1]
    email = new_user_inform.split('|||')[2]
    username = "tarber" + str(len(c3.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()))
    password = new_user_inform.split('|||')[4]
    birth_dat = new_user_inform.split('|||')[5]
    gend = new_user_inform.split('|||')[6]
    print(new_user_inform.split("|||"))

    new_username = username
    phone_numbers = [email]
    os.mkdir("/home/gor/tarber/static/user_image/" + username)
    os.chmod("/home/gor/tarber/static/user_image/" + username , 0o777)
    #os.system("sudo chmod 777 /home/gor/tarber/static/user_image")
    #os.system("sudo chmod 777 /home/gor/tarber/static/user_image/" + username)
    not_list = [['1,'], []]
    session['user'] = username
    print(getsession())
    c3.execute("CREATE TABLE IF NOT EXISTS " + username + " (name TEXT, surname TEXT, likes INT, posts TEXT, email TEXT, username TEXT, password TEXT, birth TEXT, gend TEXT, note TEXT)")
    c3.execute('INSERT INTO ' + username + ' VALUES("' + name + '", "' + surname + '", "' + '0' + '", "' + '[]' + '", "' + str(phone_numbers) + '", "' + username + '", "' + password + '" , "' + birth_dat + '" , "' + gend + '" , "' + str(not_list) +'", "' + lang + '")')
    print(getsession())
    session['user'] = username
    session['user'] = username
    print(getsession())
    conn3.commit()
    return "11"

@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    global new_username
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for i in user_list:
        print(getsession())
        if i[0] == getsession():
            print("gnac")
            return jsonify(c.execute("SELECT * FROM " + getsession()).fetchall(), sqlite3.connect("db/post.db").cursor().execute('SELECT * FROM posts').fetchall())

@app.route('/get_full_users/<w_uname>', methods=['GET', 'POST'])
def get_full_users(w_uname):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if w_uname == "0":
        return jsonify(user_list)
    else:
        return jsonify(c.execute("SELECT * FROM " + w_uname).fetchall())

@app.route('/get_full_posts', methods=['GET', 'POST'])
def get_full_posts():
    return jsonify(sqlite3.connect("db/post.db").cursor().execute('SELECT * FROM posts').fetchall())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/rate_user/<username>/<rateing>/<rater>', methods=['GET', 'POST'])
def rate_user(username, rateing, rater):
    print("RATEING STARTED")
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    c.execute('UPDATE ' + username +  ' SET likes="' + str((float(c.execute("SELECT * FROM " + username).fetchall()[0][2]) + float(rateing)) / 2) + '"')
    my_list = ast.literal_eval(c.execute("SELECT * FROM " + rater).fetchall()[0][9].strip())
    send_list = []
    for i in my_list[1]:
        print(i)
        try:

            if len(i.split("&")) > 1:
                print("INSIDE IF")
                if i.split("&")[1].strip() == username:
                    print("DETECTED THAT FUCKIN USRENAME")
                    pass
                else:
                    send_list.append(i)
            else:
                send_list.append(i)
        except:
            send_list.append(i)

    update_list = [[], send_list]
    print(update_list)
    c.execute('UPDATE ' + rater +  ' SET note="' + str(update_list) + '"')

    conn.commit()
    return "11"

@app.route('/book_agree/<agree_info>', methods=['GET', 'POST'])
def book_agree(agree_info):
    print(agree_info.split("|||"))
    driver = agree_info.split("|||")[0]
    not_id = agree_info.split("|||")[1]
    user = agree_info.split("|||")[2]
    want_palce = agree_info.split("|||")[3]
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("db/post.db")
    c1 = conn1.cursor()
    new_ls = []
    booked_places = c1.execute("SELECT * FROM posts WHERE id = " + str(not_id)).fetchall()[0][-5]
    booked_list =  ast.literal_eval(c1.execute("SELECT * FROM posts WHERE id = " + str(not_id)).fetchall()[0][-2].strip())
    for i in booked_list:
        if i[0] == user:
            new_ls.append([user, 1])
        else:
            new_ls.append(i)
    c1.execute('UPDATE posts SET goue = "' + str(new_ls) + '"' + ' WHERE id=" ' + str(not_id) + '"')
    c1.execute('UPDATE posts SET av_space = "' + str(int(want_palce) + int(booked_places)) + '" WHERE id=" ' + str(not_id) + '"')
    my_list = ast.literal_eval(c.execute("SELECT * FROM " + driver).fetchall()[0][9].strip())
    my_list_wanter = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][9].strip())
    my_list_wanter[0].append("2," + driver)
    my_list_wanter[0].append("3," + driver + "  &" + driver)
    send_list = []
    print(my_list)
    for i in my_list[1]:
        print(i)
        try:
            if int(i.split("||||")[1]) == int(not_id) and i.split(",")[1] == user:
                send_str = "4," + user + "||||" + not_id + "||||" + "0" 
                send_list.append(send_str)
            
            else:
                send_list.append(i)
        except:
            send_list.append(i)
    print(send_list)
    update_list = [[], send_list]
    print(update_list)
    c.execute('UPDATE ' + driver +  ' SET note="' + str(update_list) + '"')
    c.execute('UPDATE ' + user +  ' SET note="' + str(my_list_wanter) + '"')
    conn.commit()
    conn1.commit()
    return "11"

@app.route('/book_seat/<booking_info>', methods=['GET', 'POST'])
def book_seat(booking_info):
    conn = sqlite3.connect("db/post.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("db/user.db")
    c1 = conn1.cursor()
    number = booking_info.split("|||")[0]
    want_seat = booking_info.split("|||")[1]
    way_id = booking_info.split("|||")[2]
    book_uname = booking_info.split("|||")[3]
    driver = booking_info.split("|||")[4]
    fromo = booking_info.split("|||")[5]
    too = booking_info.split("|||")[6]
    my_list = ast.literal_eval(c1.execute("SELECT * FROM " + driver).fetchall()[0][9].strip())
    print(my_list)
    my_mess = "5," + book_uname + "," + want_seat + "," + number + "," + fromo + "," + too + "!||||" + str(way_id) + "||||" + "1"
    my_list[0].append(my_mess)
    print(my_list)
    booked_list =  ast.literal_eval(c.execute("SELECT * FROM posts WHERE id = " + str(way_id)).fetchall()[0][-2].strip())
    booked_list.append([book_uname, 0])
    c.execute('UPDATE posts SET goue = "' + str(booked_list) + '"' + ' WHERE id=" ' + str(way_id) + '"')
    c1.execute('UPDATE ' + driver + ' SET note = "' + str(my_list) + '"')
    conn1.commit()
    conn.commit()
    return "11"

@app.route('/unbook/<unbooking_info>', methods=['GET', 'POST'])
def unbook(unbooking_info):
    conn = sqlite3.connect("db/user.db")
    conn1 = sqlite3.connect("db/post.db")
    c = conn.cursor()
    c1 = conn1.cursor()
    some_val = 0
    way_id = unbooking_info.split("|||")[0]
    curr_name = unbooking_info.split("|||")[1]
    driver = unbooking_info.split("|||")[2]
    new_ls = []
    new_not = []
    new_not1 = []
    kim = []
    booked_list =  ast.literal_eval(c1.execute("SELECT * FROM posts WHERE id = " + str(way_id)).fetchall()[0][-2].strip())  #Deleting booked user from posts
    for i in booked_list:
        if i[0] == curr_name:
            pass
        else:
            new_ls.append(i)


    my_list = ast.literal_eval(c.execute("SELECT * FROM " + driver).fetchall()[0][9].strip())      #sending notefication to driver
    my_mess = "6," + curr_name + "||||" + str(way_id) + "||||" + "0"


    for i in my_list[0]:                                                                        #adding netofiaction 
        if i.split(" ")[0] == curr_name:
            new_not.append(my_mess)
            some_val = 1
        else:
            new_not.append(i)

    if some_val == 0:
        for k in my_list[1]:
            if k.split(" ")[0] and "accecpted" not in k and "deciled" not in k and "decilind" not in k:
                new_not.append(my_mess)
            else:
                kim.append(k)
    else:
        kim = my_list[1]

    new_not1.append(new_not)
    new_not1.append(kim)
    #my_list[0].append(my_mess)
    print(my_list)
    print(new_ls)
    
    c1.execute('UPDATE posts SET goue = "' + str(new_ls) + '"' + ' WHERE id=" ' + str(way_id) + '"')        #Sending all information to Database
    c.execute('UPDATE ' + driver + ' SET note = "' + str(new_not1) + '"')
    conn1.commit()
    conn.commit()
    return "11"

@app.route('/book_decil/<deciling_info>', methods=['GET', 'POST'])
def book_decil(deciling_info):
    conn = sqlite3.connect("db/user.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("db/post.db")
    c1 = conn1.cursor()

    not_id = deciling_info.split("|||")[1]
    user = deciling_info.split("|||")[2]   
    driver =  deciling_info.split("|||")[0]
    wh_users = [ l for l in ast.literal_eval(c1.execute("SELECT * FROM posts WHERE id='" + str(not_id) + "'").fetchall()[0][12])]
    my_list_wanter = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][9].strip())
    my_list_wanter[0].append("7," + driver)
    my_list = ast.literal_eval(c.execute("SELECT * FROM " + driver).fetchall()[0][9].strip())
    send_list = []
    print(my_list)
    wh_users_new = []
    for j in wh_users:
        if j[0] == user:
            pass
        else:
            wh_users_new.append(j)

    c1.execute("UPDATE posts SET goue='" + str(wh_users_new) + "' WHERE id='" + str(not_id) + "'")

    for i in my_list[1]:
        print(i)
        try:
            if i.split("||||")[1] == not_id and i.split("||||")[0].split(" ")[0] == user:
                send_str = "8," + user + "||||" + not_id + "||||" + "0" 
                send_list.append(send_str)
                
            else:
                send_list.append(i)
        except:
            send_list.append(i)
    update_list = [[], send_list]
    c.execute('UPDATE ' + driver +  ' SET note="' + str(update_list) + '"')
    c.execute('UPDATE ' + user +  ' SET note="' + str(my_list_wanter) + '"')
    conn.commit()
    conn1.commit()
    return "11"

@app.route("/new_quest", methods=['GET', 'POST'])
def new_quest():
    return render_template("new_quest.html")

@app.route("/quest", methods=['GET', 'POST'])
def quest():
    asd = ""
    if getsession() == "not":
        asd = 0;
    else:
        asd = getsession()
    return render_template("quest.html", user=asd)

@app.route("/sc", methods=['GET', 'POST'])
def sc():
    asd = ""
    if getsession() == "not":
        asd = 0;
    else:
        asd = getsession()
    return render_template("search.html", user=asd)

@app.route("/just_test", methods=['GET', 'POST'])
def just_test():
    session['user'] = "testmy"
    return getsession()

@app.route("/sl_ph", methods=['GET', 'POST'])
def sl_ph():
    return render_template("frame.html")

@app.route("/gtp", methods=['GET', 'POST'])
def gtp():
    return render_template("getpr.html")

@app.route("/quest_404", methods=['GET', 'POST'])
def quest_404():
    return render_template("quest_404.html")

@app.route("/get_quest/<quest_info>", methods=['GET', 'POST'])
def get_quest(quest_info):
    global quest_id
    quest_id = quest_info
    return "11"

@app.route("/do_del/<main>/<code>", methods=['GET', 'POST'])
def do_del(main, code):
    conn = sqlite3.connect("db/post.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("db/user.db")
    c1 = conn1.cursor()
    c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11]
    if int(code) == 15022:
        print("PASS DELETE")
        try:
            print("TRY PASS")
            if int(main.split("&")[1]) == 1502:
                print("DOING DELETE")
                user_notef_unr = ast.literal_eval(c1.execute("SELECT * FROM " + str(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11])).fetchall()[0][9].strip())[0]
                user_notef_r = ast.literal_eval(c1.execute("SELECT * FROM " + str(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11])).fetchall()[0][9].strip())[1]
                print(user_notef_unr)
                print(user_notef_r)
                user_new_unr = []
                user_new_r = []
                wh_users = [ l[0] for l in ast.literal_eval(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][12])]
                for k in user_notef_r:
                    if len(k.split("||||")) > 2:
                        if int(k.split("||||")[1]) == int(main.split("&")[0]):
                            print("DELETEED THAT UNREAD POST")
                        else:
                            user_new_r.append(k)
                    else:
                        user_new_r.append(k)

                for j in user_notef_unr:
                    if len(j.split("||||")) > 2:
                        if int(j.split("||||")[1]) == int(main.split("&")[0]):
                            print("DELETEED THAT READ POST")
                        else:
                            user_new_unr.append(j)
                    else:
                        user_new_unr.append(j)

                print(wh_users)
                for n in wh_users:
                    print(ast.literal_eval(c1.execute("SELECT * FROM " + str(n)).fetchall()[0][9].strip())[0])
                    that_us_notef_unr = ast.literal_eval(c1.execute("SELECT * FROM " + str(n)).fetchall()[0][9].strip())[0]
                    print(ast.literal_eval(c1.execute("SELECT * FROM " + str(n)).fetchall()[0][9].strip())[1])
                    that_us_notef_r = ast.literal_eval(c1.execute("SELECT * FROM " + str(n)).fetchall()[0][9].strip())[1]
                    that_us_notef_unr.append( "9," + c1.execute("SELECT * FROM " + str(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11])).fetchall()[0][0] + "," + c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][1] + "," + c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][2])
                    print("UPDATEING "+ n)
                    print([that_us_notef_unr, that_us_notef_r])
                    c1.execute("UPDATE " + n + " SET note='" + str([that_us_notef_unr, that_us_notef_r]).replace("'", '"') + "'")
                    conn1.commit()
                    print("UPDATED " + n)
                notef_str = str([user_new_unr, user_new_r])
                print(notef_str)
                c1.execute("UPDATE " + str(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11]) + " SET note = '" + notef_str.replace("'", '"') + "'")
                print("UPDATED DRIVER " + str(c.execute("SELECT * FROM posts WHERE id='" + str(main.split("&")[0]) + "'").fetchall()[0][11]))
                c.execute("DELETE FROM posts WHERE id='" + str(main.split("&")[0]) + "'")
                print("DELETEED POST  " + str(main.split("&")[0]))
                conn.commit()
                conn1.commit()
                r = requests.get("https://codetg.cf/tarber_out")
            else: return "13"
        except: return "12"
    else: return "14"
    conn.commit()
    conn1.commit()
    return "11"

@app.route("/user_add_ph/<user_ph_info>", methods=['GET', 'POST'])
def user_add_ph(user_ph_info):
    uname = user_ph_info.split("|||")[0]
    don = user_ph_info.split("|||")[1]
    session['user'] = uname
    if int(don) == 1:
        if(1): 
            os.system("sudo mkdir /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname)
            os.system("sudo rm /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname + "/a.png")
            os.system("sudo cp /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/last_ph/" + uname + ".png /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname + "/a.png")
            #os.system("sudo rm /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/last_ph/" + uname + ".png")
    else:
        os.system("sudo mkdir /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname)
        os.system("sudo rm /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname + "/a.png")
        os.system("sudo cp /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/no_user.png /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + uname + "/a.png")

    return "11"

@app.route("/send_quest", methods=['GET', 'POST'])
def send_quest():
    global quest_id
    conn = sqlite3.connect("db/post.db")
    c = conn.cursor()
    return jsonify(c.execute("SELECT * FROM posts WHERE id = " + quest_id).fetchall(), c.execute("SELECT * FROM posts").fetchall())

@app.route('/new_posts/<new_post_info>/<is_tuda>', methods=['GET', 'POST'])
def new_posts(new_post_info, is_tuda):
    conn = sqlite3.connect("db/user.db")
    conn1 = sqlite3.connect("db/post.db")
    x = datetime.datetime.now(pytz.timezone('Asia/Yerevan'))
    curr_time = x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + " " + x.strftime("%H") + ":" + x.strftime("%M")
    c = conn.cursor()
    c1 = conn1.cursor()
    info = tuple(new_post_info.split('$$$'))
    print(info)
    id = int(c1.execute("SELECT * FROM tab_count").fetchall()[0][0]) + 1
    c1.execute("UPDATE tab_count SET num='" + str(id) + "'")
    save_info = []
    my_dict = {id : {new_post_info : ()}}
    my_dict[id][new_post_info] = []
    print(my_dict)
    a = ast.literal_eval(c.execute('SELECT * FROM ' + new_post_info.split('$$$')[9]).fetchall()[0][3])
    a.append(id)
    c.execute('UPDATE ' + info[9] + ' SET posts = "' + str(a) + ' "')
    c1.execute("CREATE TABLE IF NOT EXISTS posts (id INT, fromo TEXT, too TEXT, go_time TEXT, back_time TEXT, money INT, car TEXT, free_space INT, phone TEXT, av_space INT, more_inf TEXT, driver TEXT, goue TEXT, smth TEXT)")
    c1.execute('INSERT INTO posts VALUES(  " ' + str(id) + ' ", "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[2]) + '", "' + curr_time + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]).replace('"', "'") + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", "' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + '" )')
    print('INSERT INTO posts VALUES(  " ' + str(id) + ' ", "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[2]) + '", "' + curr_time + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]).replace('"', "'") + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", ' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + ' )')
    if str(is_tuda) == "true":
        print("DETECTED TUDA")
        c1.execute("UPDATE tab_count SET num='" + str(id + 1) + "'")
        c1.execute('INSERT INTO posts VALUES(  " ' + str(id + 1) + ' ", "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[3]) + '", "' + curr_time + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]).replace('"', "'") + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", "' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + '" )')
        print('INSERT INTO posts VALUES(  " ' + str(id + 1) + ' ", "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[3]) + '", "' + curr_time + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]).replace('"', "'") + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", ' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + ' )')
        a1 = ast.literal_eval(c.execute('SELECT * FROM ' + new_post_info.split('$$$')[9]).fetchall()[0][3])
        a1.append(id + 1)
        c.execute('UPDATE ' + info[9] + ' SET posts = "' + str(a1) + ' "')
    conn1.commit()
    conn.commit()
    return "11"



#ssl_context=('cert.pem', 'key.pem')
if __name__ == '__main__':
#    socket.run(app, host='0.0.0.0')
    app.run(host='0.0.0.0', debug=True)