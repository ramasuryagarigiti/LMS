import tkinter
from tkinter import messagebox

import instamojo_wrapper
from instamojo_wrapper import Instamojo
from flask import Flask, render_template, request, Blueprint, url_for, session, flash
import mysql.connector as ms
# from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_mail import Message, Mail
from mysqlx import Session
from validate_email import validate_email
import os, getpass, random
from submain import submain
from werkzeug.utils import redirect
from flask_session import Session

app = Flask(__name__)
# app.run(host='1111')


apikey = "test_de138abe63eba62f1f94adf5b90"
authkey = "test_f19f6a2bed51aa4b30e476ec277"
api = Instamojo(api_key=apikey, auth_token=authkey, endpoint="http://test.instamojo.com/api/1.1/")

app.register_blueprint(submain, url_prefix="")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hisir960@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qwert@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# app.secret_key="super secret"


app.debug = 1


# Session(app)
# app.register_blueprint(sec, url_prefix="/stock")
# app.register_blueprint(sec, url_prefix="/stock")
# app.register_blueprint(sec, url_prefix="/stock")
@app.route("/login", methods=["GET", "POST"])
def log():
    if request.method == 'POST':
        email = request.form['email']
        pswd1 = request.form['passwd']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            # cu.execute("create database grp");
            # cu.execute("use grp");cu.execute("create table userlogin(name varchar(45), passwd varchar(25))")
            # cu.execute("select userlogin.name from userlogin where email,passwd=(%s,%s)",(email,pswd1))
            cu.execute("use grp");
            print("(from lgn)email=", email)
            l = cu.execute("select userlogin.eml,userlogin.passwd from userlogin where userlogin.eml=%s", (email,))
            lst = cu.fetchall()
            # print("lst=", lst)
            # print("pswd1=",pswd1)
            for i in lst:
                if i[0] == email:
                    if i[1] == pswd1:
                        cu.execute("select userlogin.name,userlogin.id from userlogin where userlogin.eml=%s", (email,))
                        p = cu.fetchall()
                        cu.execute("select books.book_name,books.author,books.about from books")
                        data = cu.fetchall();
                        # print("before returning i[0]=",i[0],"i[1]=",i[1])
                        session["name"]=p[0][0]
                        session["id"] = p[0][1]
                        print("id from here: ",p[0][1] )
                        return render_template('stud.html', name=p[0][0], data=data)
                    else:
                        return "Incorrect Password"
                else:
                    return "user doesn't exist"
                # return render_template("home.html")

            else:
                # print("l=",l);print("lst(frkom userlgn)=",lst);
                cu.close()
                return "Incorrect username or password!!"

        except Exception as e:
            return str(e)
        finally:
            cu.close()
    return render_template("login.html")


@app.route("/admlgn", methods=["GET", "POST"])
def admlog():
    if request.method == 'POST':
        email = request.form['email']
        pswd1 = request.form['passwd']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use grp")
            cu.execute("select admlogin.eml,admlogin.passwd from admlogin where admlogin.eml=%s", (email,))

            lst = cu.fetchall()

            # print("l=",l)
            print("(adm)lst=", lst)
            for i in lst:
                if i[0] == email:
                    if i[1] == pswd1:
                        m = cu.execute("select admlogin.name from admlogin where admlogin.eml=%s", (email,))
                        nm = cu.fetchall()
                        return render_template('Adm.html', val=nm)
                    else:
                        return "Incorrect Password"
                else:
                    return "user doesn't exist"

            cu.close()
        except Exception as e:
            return str(e)

    return render_template("AdmLogin.html")


@app.route("/signup", methods=["GET", "POST"])
def sign():
    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        pswd = request.form['passwd']
        pswd2 = request.form['passwd1']
        ph = request.form['phone']
        rl = request.form['role']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            # cu.execute("create database grp");
            cu.execute("use grp");
            # cu.execute("create table signup(username varchar(50) ,email varchar(320) primary key,phone varchar(20),pswd varchar(20), role varchar(6) not null)")
            # cu.execute("create table userx(uname varchar(50),email varchar(320) primary key,phone varchar(20),pswd varchar(20))")
            lst = cu.fetchall()
            if (email,) in lst:
                return "Email already exists!!"
            if pswd != pswd2:
                return "Password doesn't matches"
            else:
                if str(validate_email(email)) == "False":
                    return "invalid email address"
                if str(rl.lower()) == "admin":
                    pin = str(random.randint(1000, 10000))
                    cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, email, ph, pswd, rl,))
                    # cu.execute("create table admlogin(name varchar(45), eml varchar(40), passwd varchar(25))")
                    cu.execute("insert into admlogin values(%s,%s,%s,%s)", (user, email, pswd, pin,))
                    mydb.commit();
                    cu.close()
                    sub = "LMS Registration"
                    msg = Message(
                        sub,
                        sender='hisir960@gmail.com',
                        recipients=[email]
                    )
                    msg.body = 'Hi, Thanks for registering for our website.You are a admin now.Please do not share this code with anyone your secret pin is:' + pin
                    mail.send(msg)
                    print("*" * 30, 'Email Sent')

                    # print(validate_email(email));
                    return render_template("AdmLogin.html")
                elif str(rl.lower()) == "user":
                    cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, email, ph, pswd, rl,))
                    # cu.execute("create table userlogin(name varchar(45), eml varchar(40), passwd varchar(25))")
                    cu.execute("insert into userlogin values(%s,%s,%s)", (user, email, pswd,))
                    mydb.commit();
                    cu.close();
                    sub = "LMS Registration"
                    msg = Message(
                        sub,
                        sender='hisir960@gmail.com',
                        recipients=[email]
                    )
                    msg.body = 'Hi, Thanks for registering for our website.You are a user now.Thank you using our site. we are happy to have you here!!'
                    mail.send(msg)
                    print("*" * 30, 'User Email Sent')
                    return render_template("login.html")

                # print(validate_email(email));


        except Exception as e:
            if "Duplicate entry" in str(e):
                return "Email already exists!!"
            else:
                return str(e)
    return render_template("signup.html")


@app.route("/")
@app.route("/wel")
def welc():
    return render_template("welcome.html")


@app.route("/home")
def hm():
    return render_template("home.html")


@app.route("/adm")
def admn():
    return render_template("Adm.html")


@app.route("/addbk", methods=["POST", "GET"])
def bk():
    if request.method == 'POST':
        bknm = request.form['bkname']
        author = request.form['author']
        branch = request.form['branch']
        yr = request.form['yr']
        about = request.form['about']
        eml = request.form['cnfrmeml']
        pin = request.form['pin']
        pdf = request.form['pdf']
        try:
            # def bintofile(bindata, filename):
            #     with open(pdf, bindata) as file:
            #         file.write(bindata)
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use grp")
            # cu.execute("create table books(book_name varchar(30), author varchar(15),branch varchar(6),yr varchar(3),about varchar(50),inserted_by varchar(30),pin varchar(4),book blob) ")
            l = cu.execute("select admlogin.eml,admlogin.pin from admlogin where admlogin.eml=%s", (eml,))
            lst = cu.fetchall()
            print("lst=", lst)
            for i in lst:
                if i[0] == eml:
                    if i[1] == pin:
                        cu.execute("insert into books values(%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (bknm, author, branch, yr, about, eml, pin, pdf,))
                        mydb.commit();
                        return "<h2 style='color:green;'>Book added successfully!!</h2>"
                    else:
                        return "incorrect password"
                else:
                    return "incorrect mail"

            cu.close()

            print("*" * 30)
            print("Book name=", bknm, "pdf=", pdf)

        except Exception as e:
            print("Erroor is:", str(e))

    user_details = {
        'name': os.getlogin(),
        # 'email': 'john@doe.com'
    }
    return render_template("addbk.html", user=user_details)


@app.route("/addcrs", methods=["POST", "GET"])
def crs():
    if request.method == 'POST':
        crnm = request.form['crnm']
        fac = request.form['fac']
        branch = request.form['branch']
        abt = request.form['about']
        eml = request.form['cnfrmeml']
        pin = request.form['pin']
        fee = request.form['fee']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use grp")
            # cu.execute("create table books(book_name varchar(30), author varchar(15),branch varchar(6),yr varchar(3),about varchar(50),inserted_by varchar(30),pin varchar(4),book blob) ")
            l = cu.execute("select admlogin.eml,admlogin.pin from admlogin where admlogin.eml=%s", (eml,))
            lst = cu.fetchall()
            print("lst=", lst)
            for i in lst:
                if i[0] == eml:
                    if i[1] == pin:
                        cu.execute("insert into courses values(%s,%s,%s,%s,%s,%s)",
                                   (crnm, fac, branch, abt, eml, fee,))
                        mydb.commit();
                        return "<h2 style='color:green;'>Course added successfully!!</h2>"
                    else:
                        return "incorrect password"
                else:
                    return "incorrect mail"

            cu.close()

            print("*" * 30)
            print("course name=", crnm, "pdf=", fee)

        except Exception as e:
            print("Erroor is:", str(e))

    user_details = {
        'name': os.getlogin(),
        # 'email': 'john@doe.com'
    }
    return render_template("addcrs.html", user=user_details)


@app.route("/addstud", methods=["GET", "POST"])
def stud():
    if request.method == 'POST':
        user = request.form['name']
        eml = request.form['stdeml']
        pswd = request.form['pswd']
        ph = request.form['phn']
        adpin = request.form['pin']
        ademl = request.form['ademl']
        rl = request.form['role'];
        count = 0
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            cu.execute("use grp");
            # cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, email, ph, pswd, rl,))

            l = cu.execute("select admlogin.eml,admlogin.pin from admlogin where admlogin.eml=%s", (ademl,))
            lst = cu.fetchall()
            for i in lst:
                if i[0] == eml: count += 1
                if i[0] == ademl:
                    if i[1] == adpin:
                        if str(rl.lower()) == "admin" and count == 0:
                            pin = str(random.randint(1000, 10000))
                            cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, eml, ph, pswd, rl,))
                            cu.execute("insert into admlogin values(%s,%s,%s,%s)", (user, eml, pswd, pin,))
                            mydb.commit();
                            sub = "LMS Registration"
                            msg = Message(
                                sub,
                                sender='hisir960@gmail.com',
                                recipients=[eml]
                            )
                            msg.body = 'Hi, Now you are registerd for our website.You are a admin now.Please do not share the below code with anyone.\n your secret pin is:' + pin
                            mail.send(msg)
                            return "Admin added successfully!!"
                        elif str(rl.lower()) == "user":
                            cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, eml, ph, pswd, rl,))
                            cu.execute("insert into userlogin values(%s,%s,%s)", (user, eml, pswd,))
                            mydb.commit();
                            sub = "LMS Registration"
                            msg = Message(
                                sub,
                                sender='hisir960@gmail.com',
                                recipients=[eml]
                            )
                            msg.body = 'Hi, Thanks for registering for our website.You are a user now.Thank you using our site. we are happy to have you here!!'
                            mail.send(msg)
                            return "user added successfully!!"
                        else:
                            return "unable to insert user(probably because the user already exists). please try again later!!"
                    else:
                        return "incorrect Security pin"
                else:
                    return "incorrect email or email already exists"

            cu.close();

        except Exception as e:
            return "error is:-" + str(e)
    user_details = {
        'name': os.getlogin(),
    }
    return render_template("addstud.html", user=user_details)


@app.route("/viewbks")
def vbks():
    user_details = {
        'name': os.getlogin(),
    }
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        # cu.execute("create database grp");
        cu.execute("use grp")

        l = cu.execute("select books.book_name,books.author,books.about,books.branch,books.inserted_by from books")
        data = cu.fetchall();
        cu.close()
        # vals = [("list-group-item list-group-item-primary"), ("list-group-item list-group-item-secondary"), ]
        hdr = ("Book", "Author", "About", "Branch", "Modified by",)
    except Exception as e:
        print("error:-", str(e))

    return render_template("viewbks.html", user=user_details, data=data, header=hdr)


@app.route("/viewstuds")
def stds():
    user_details = {
        'name': os.getlogin(),
    }
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        # cu.execute("create database grp");
        cu.execute("use grp")

        l = cu.execute("select userlogin.name, userlogin.eml from userlogin")
        data = cu.fetchall();
        cu.close()
        vals = [("list-group-item list-group-item-primary"), ("list-group-item list-group-item-secondary"), ]
        hdr = ("Student", "Email",)
    except Exception as e:
        print("error:-", str(e))

    return render_template("viewstds.html", user=user_details, data=data, header=hdr)


@app.route("/stud", methods=["GET", "POST"])
def std():
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        # cu.execute("create database grp");
        cu.execute("use grp")

        l = cu.execute("select books.book_name,books.author,books.about from books")
        data = cu.fetchall();
        cu.close()

    except Exception as e:
        print("error:-", str(e))

    return render_template("stud.html", data=data)


@app.route('/regb', methods=['POST', 'GET'])
def regbook():
    val = request.form['bknm']

    try:
        # bknm=request.form['bknm']
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor();
        cu.execute("use grp")
        l = cu.execute(
            "select books.book_name,books.author,books.about,books.branch,books.yr,books.inserted_by from books where books.book_name=%s",
            (val,))
        data = cu.fetchall();
        mydb.commit();
        cu.close()
        # return render_template("regbk.html",data=data)
        print("type of data", type(data))
    except Exception as e:
        print("error:-", str(e))

    return render_template("regbk.html", data=data)


@app.route('/courses', methods=['POST', 'GET'])
def crss():
    # val = request.form['crnm']
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        # cu.execute("create database grp");
        cu.execute("use grp")

        cu.execute("select courses.crnm,courses.fac,courses.abt from courses")
        data = cu.fetchall();
        cu.close()

    except Exception as e:
        print("error:-", str(e))

    return render_template("courses.html", data=data)


@app.route('/regcrs', methods=['POST', 'GET'])
def regcrs():
    val = request.form['crnm']
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        cu.execute("use grp")
        cu.execute(
            "select courses.crnm,courses.fac,courses.abt,courses.branch,courses.fee from courses where courses.crnm=%s",
            (val,))
        data = cu.fetchall()
        mydb.commit()
        cu.close()
        # print("**"*30 , "val=",val)
        # return render_template("regbk.html",data=data)
        print("type of data is:", type(data))
        if request.form['submit_button'] == 'Register to this course':
            print("crnm iis:", request.form['crnm'])
            return render_template("userDetails.html", values=request.form['crnm'])

    except Exception as e:
        print("error:-(", str(e))

    return render_template("regcrs.html", data=data)


@app.route("/suc")
def sc():
    return "<h1 style='color:green'>Payment successful</h1>"

@app.route("/cal")
def cals():
    return render_template("calendar.html")

# @app.route("/contact")
# def con():
#     return render_template("dial.html")


@app.route("/userdet", methods=["POST", "GET"])
def usrd():
    if request.method == "POST":
        nm = request.form.get('nm')
        ml = request.form.get('mail')
        amt = request.form.get('amt')
        crs = request.form.get('crs')
        # print("***"*15,"name=",nm)

        response = api.payment_request_create(
            amount=amt, purpose=crs, buyer_name=nm, send_email=True, email=ml,redirect_url="http://127.0.0.1:5000/suc")
        print(response['payment_request']['longurl'])
        return redirect(response['payment_request']['https://test.instamojo.com/@hisir960'])


    else:
        return redirect("/userdet")
    # return render_template("userDetails.html")
    # return render_template("payment.html",name=nm)


@app.route("/profile")
def prof():
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        cu.execute("use grp")
        cu.execute("select * from userlogin where userlogin.id=%s",(session["id"],))
        data1 = cu.fetchall();print("data(from prof): ",data1)
        cu.close()
    except  Exception as e:print("Error from profile page as:",str(e))

    return render_template("userprofile.html",data=data1)




@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


# @app.route('/paydet', methods=['POST', 'GET'])
# def det():
#     name = request.form['name']
#     if request.method == "POST" or "GET":
#         return render_template("payment.html",name=name)
# if request.method == "POST":
#
#     try:
#         print("name=", name)
#         return render_template("payment.html",name=name)
#     except Exception as e:
#         return "Dare to deal with this new one??\n" + str(e)
#
# else:
#     print("what the fuck!!!!!!!")
#     return "This is a method of type:" + request.method

# return render_template("paydet.html")


# @app.route("/pay", methods=["POST", "GET"])
# def mny():
#     if request.method == "post":
#         return render_template("payment.html")
#     else:
#         return "Not a post Method"
# return render_template("payment.html")


# @app.route('/regb/<bknm>', methods=['POST','GET'])
# def regbook(bknm):

# @app.route("/test", methods=["GET", "POST"])
# def tst():
#     if request.method == 'POST':
#         try:
#             print("--" * 30)
#             eml = request.form['email']
#             pdf = request.form['pdf']

# def filetobin(filename):
#     with open(pdf ,'rb'):
#         bindata=pdf.read()
# def bintofile(bindata, filename):
#     with open(pdf, bindata) as file:
#         file.write(bindata)

# mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
#         cu = mydb.cursor()
#         cu.execute("use grp")
#         cu.execute("create table test_table(eml varchar(25), pdf blob)")
#         cu.execute("insert into test_table values(%s,%s)",(eml,pdf,))
#         mydb.commit()
#         lst=cu.fetchall()
#         cu.close()
#         print(pdf);
#         print("path:-", pdf.path())
#         return render_template("test.html")
#     except Exception as e:
#         print("Error is:-", str(e))
# else:
#     return "not a post method"
# return render_template("test.html")
# login on 4-4-2022:


# user_details = {
# 'name': os.getlogin(),
# 'name': getpass.getuser(),
# 'email': 'john@doe.com'
# }

# @app.route("/login", methods=["GET", "POST"])
# def log():
# if request.method == 'POST':
#     email = request.form['email']
#     pswd1 = request.form['passwd']
#     try:
#         mydb=ms.connect(host="localhost", user="root", passwd="mysql@!@");cu=mydb.cursor()
# cu.execute("create database grp");
# cu.execute("use grp");cu.execute("create table userlogin(name varchar(45), passwd varchar(25))")
# cu.execute("select userlogin.name from userlogin where email,passwd=(%s,%s)",(email,pswd1))
# cu.execute("use grp")
# l = cu.execute("select userlogin.passwd from userlogin where userlogin.eml=%s", (email,))
# if l is not None:
#     p=cu.execute("select userlogin.passwd from userlogin where userlogin.eml=%s",(email,))
# p1=cu.fetchall()
# lst = cu.fetchall()
# else:
#     return "E-mail doesn't exist"
# if str(l)==str(pswd1):
#     return render_template("home.html")
# print("l=", l, "p=", l)
# if str(l)==str(email):
#     if str(p)==str(pswd1):
# if p is not None:
#     return render_template("home.html")
# else:
#     return "pswd error"
# else:
#     return "Incorrect username or password!!"
# mydb.commit();
# cu.close()
# return render_template("home.html")
#     except Exception as e:
#         return str(e)
#
# return render_template("login.html")
