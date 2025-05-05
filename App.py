from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import sys, fsdk, math, ctypes, time
import mysql.connector

app = Flask(__name__)

app.config['DEBUG']
app.config['SECRET_KEY'] = 'san'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Active'")
    data1 = cur.fetchall()

    return render_template('AdminHome.html', data=data, data1=data1)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where status='waiting'")
            data = cur.fetchall()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where status='Active'")
            data1 = cur.fetchall()
            return render_template('AdminHome.html', data=data, data1=data1)
        else:
            flash( "UserName or Password Incorrect!")

            return render_template('AdminLogin.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']

        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        accno = request.form['accno']
        username = request.form['username']
        Password = request.form['Password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' or AccountNo='" + accno + "'")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + age + "','" + mobile + "','" + email + "','" + address + "','" + accno + "','" + username + "','" + Password + "','nill','waiting','0.00')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into multitb values('','" + accno + "','" + username + "')")
            conn.commit()
            conn.close()

        else:
            flash('Already Register Account Number or Username')
            return render_template('NewUser.html')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Approved'")
    data1 = cur.fetchall()

    return render_template('AdminHome.html', data=data, data1=data1)


@app.route("/Approved")
def Approved():
    import LiveRecognition as liv
    #liv.att()

    del sys.modules["LiveRecognition"]

    id = request.args.get('lid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Active'  where id='" + id + "' ")
    conn.commit()
    conn.close()

    return Approved1()



@app.route("/UpdateF")
def UpdateF():
    import LiveRecognition as liv
    #liv.att()

    del sys.modules["LiveRecognition"]

    return Approved1()
@app.route("/Approved1")
def Approved1():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Active'")
    data1 = cur.fetchall()

    return render_template('AdminHome.html', data=data, data1=data1)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['Password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:

            session['acc'] = data[6]

            pin = data[9]
            session['pin'] = data[9]

            if pin == "nill":

                return render_template('NewPin.html')

            else:
                return render_template('SelectLogin.html')
        flash('Username or Password is wrong')
        return render_template('UserLogin.html')




@app.route("/newpin", methods=['GET', 'POST'])
def newpin():
    if request.method == 'POST':
        pin = request.form['pin']
        rpin = request.form['rpin']

        if pin == rpin:

            uname = session['uname']

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute(
                "update regtb set  Pin= '" + pin + "' where Username='" + uname + "'")
            conn.commit()
            conn.close()

            return render_template('SelectLogin.html')
        else:
            flash('Pin Mismatch')
            return render_template('NewPin.html')


@app.route("/selectlogin", methods=['GET', 'POST'])
def selectlogin():
    if request.method == 'POST':

        if request.form["submit"] == "IllusionPin":

            import random
            thislist = []
            for x in range(9):
                num1 = random.randint(0, 9)
                thislist.append(num1)
            mylist = list(dict.fromkeys(thislist))
            # print(mylist)
            for x1 in range(10):
                if x1 in mylist:

                    print("hai")
                else:

                    mylist.append(x1)
            mylist1 = []
            for x in mylist:
                x1 = str(x) + '.png'
                mylist1.append(x1)

            return render_template('LoginPin.html', data=mylist1, data1=mylist)

        elif request.form["submit"] == "BrightnessPin":

            import random
            thislist = []

            for x in range(4):
                num1 = random.randint(0, 3)

                thislist.append(num1)
            mylist = list(dict.fromkeys(thislist))
            print(mylist)
            for x1 in range(4):
                if x1 in mylist:
                    print("hai")
                else:
                    mylist.append(x1)
            mylist1 = []
            for x in mylist:
                x1 = str(x) + '.png'
                mylist1.append(x1)

            session["list"] = mylist1
            return render_template('BrightnessPin.html', data=mylist1)


def remove(string):
    return string.replace(",", "")


@app.route("/loginpin", methods=['GET', 'POST'])
def loginpin():
    if request.method == 'POST':

        uname = session['uname']
        print(uname)

        n = request.form['seats']

        string = str(n)
        # print("hello" + string)

        pin = remove(string)

        print(pin)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where pin='" + str(pin) + "' and username='" + str(uname) + "'")
        data = cursor.fetchone()
        if data is None:
            import random
            thislist = []

            for x in range(9):
                num1 = random.randint(0, 9)

                thislist.append(num1)

                # print(x)

            mylist = list(dict.fromkeys(thislist))

            for x1 in range(10):
                if x1 in mylist:

                    print("hai")
                else:

                    mylist.append(x1)
            mylist1 = []
            for x in mylist:
                x1 = str(x) + '.png'
                mylist1.append(x1)

            return render_template('LoginPin.html', data=mylist1, data1=mylist)
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()

            try:
                import MyNewCode as liv1
                del sys.modules["MyNewCode"]
            except OSError as e:
                print("Caught OSError:", e)
            return facelogin()


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)


@app.route("/NewBeneficiary")
def NewBeneficiary():
    return render_template('NewBeneficiary.html')


@app.route("/Transaction")
def Transaction():
    uname = session['uname']
    accno = session['acc']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT AccountNo FROM beneficiarytb where UserName='" + uname + "' ")
    data = cur.fetchall()
    return render_template('Transaction.html', data=data, uname=uname, Accno=accno)


@app.route("/Deposit")
def Deposit():
    return render_template('Deposit.html')


@app.route("/Withdraw")
def Withdraw():
    return render_template('Withdraw.html')


@app.route("/brightlogin", methods=['GET', 'POST'])
def brightlogin():
    if request.method == 'POST':
        pin0 = request.form['pin0']
        pin1 = request.form['pin1']
        pin2 = request.form['pin2']
        pin3 = request.form['pin3']

        mylist1 = session["list"]
        print(mylist1)
        for x in mylist1:
            if x == "0.png":
                pos = mylist1.index(x)

        if pos == 0:
            pin0 = 0
        elif pos == 1:
            pin1 = 0
        elif pos == 2:
            pin2 = 0
        elif pos == 3:
            pin2 = 0

        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + uname + "' ")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)

        else:

            string = data[9]
            position = pos
            new_character = '0'

            string = string[:position] + new_character + string[position + 1:]
            string1 = str(pin0) + str(pin1) + str(pin2) + str(pin3)
            if string == string1:

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
                cursor = conn.cursor()
                cursor.execute("truncate table temptb")
                conn.commit()
                conn.close()

                import LiveRecognition1 as liv1
                del sys.modules["LiveRecognition1"]

                return facelogin()
            else:

                import random
                thislist = []

                for x in range(4):
                    num1 = random.randint(0, 3)

                    thislist.append(num1)
                mylist = list(dict.fromkeys(thislist))
                print(mylist)
                for x1 in range(4):
                    if x1 in mylist:
                        print("hai")
                    else:
                        mylist.append(x1)
                mylist1 = []
                for x in mylist:
                    x1 = str(x) + '.png'
                    mylist1.append(x1)

                session["list"] = mylist1
                flash("Password Incorrect!")
                return render_template('BrightnessPin.html', data=mylist1)





def loginvales1():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regtb where username='" + uname + "'")
    data = cursor.fetchone()

    if data:
        Email = data[4]
        Phone = data[3]
        Accountno = data[6]



    else:
        return 'Incorrect username / password !'

    return uname, Email, Phone, Accountno


@app.route("/facelogin")
def facelogin():
    uname = session['uname']
    account = session['acc']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb where AccountNo='" + account + "' ")
    data = cursor.fetchone()
    if data is None:

        flash('Face  is wrong')
        return render_template('UserLogin.html')


    else:

        account = session['acc']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM temptb where AccountNo='" + account + "'")
        data = cursor.fetchone()

        if data:
            session['loginuser'] = data[2]
            session['otp'] = data[3]

        else:
            return 'Incorrect username / password !'

        return render_template('OTP.html')


@app.route("/verifyotp", methods=['GET', 'POST'])
def verifyotp():
    if request.method == 'POST':
        votp = request.form['votp']
        num = int(session['otp'])
        reversed_num = 0

        while num != 0:
            digit = num % 10
            reversed_num = reversed_num * 10 + digit
            num //= 10

        print("Reversed Number: " + str(reversed_num))

        if str(reversed_num) == votp:
            uname = session['uname']

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + uname + "'  ")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)

        else:
            flash('OTP Incorrect')
            return render_template('OTP.html')




import hmac
import hashlib
import binascii
import random
import datetime


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


@app.route("/transaction", methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']

        bacc = request.form['bacc']

        currency = request.form['currency']

        tcc = float(currency)

        date = datetime.datetime.now().strftime('%Y-%b-%d')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM   regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:

            bal = data[11]

            Amount = float(bal) - float(tcc)

            print(Amount)


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM    beneficiarytb where  AccountNo='" + bacc + "'")
        data = cursor.fetchone()

        if data:
            bname = data[2]

        else:
            return 'Incorrect username / password !'

        if Amount < 0:

            flash('Amount Transaction Failed Balance:' + str(Amount))

            return render_template('Transaction.html')
        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute("Update regtb set Balance='" + str(Amount) + "'  where  UserName='" + uname + "' ")
            conn.commit()
            conn.close()

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor1 = conn1.cursor()
            cursor1.execute("select max(id) from transtb")
            da = cursor1.fetchone()
            if da:
                d = da[0]
                print(d)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
                cursor = conn.cursor()
                cursor.execute("SELECT  *  FROM transtb where  id ='" + str(d) + "'   ")
                data = cursor.fetchone()
                if data:
                    hash1 = data[8]
                    num1 = random.randrange(1111, 9999)
                    hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25newfacebankdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + bname + "','" + bacc + "','" + currency + "','" + date + "','" + hash1 + "','" + hash2 + "','Transaction')")
                    conn.commit()
                    conn.close()
                else:

                    hash1 = '0'
                    num1 = random.randrange(1111, 9999)
                    hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25newfacebankdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + bname + "','" + bacc + "','" + currency + "','" + date + "','" + hash1 + "','" + hash2 + "','Transaction')")
                    conn.commit()
                    conn.close()

        flash('Amount Transaction Successfully Balance:' + str(Amount))

        return render_template('Transaction.html')


@app.route("/amtwithdraw", methods=['GET', 'POST'])
def amtwithdraw():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']

        amt = request.form['amt']

        tcc = float(amt)

        date = datetime.datetime.now().strftime('%Y-%b-%d')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM   regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:

            bal = data[11]

            Amount = float(bal) - float(tcc)

            print(Amount)


        else:
            return 'Incorrect username / password !'

        if Amount < 0:

            flash('Amount Transaction Failed Balance:' + str(Amount))

            return render_template('Withdraw.html')

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute("Update regtb set Balance='" + str(Amount) + "'  where  UserName='" + uname + "' ")
            conn.commit()
            conn.close()

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor1 = conn1.cursor()
            cursor1.execute("select max(id) from transtb")
            da = cursor1.fetchone()
            if da:
                d = da[0]
                print(d)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
                cursor = conn.cursor()
                cursor.execute("SELECT  *  FROM transtb where  id ='" + str(d) + "'   ")
                data = cursor.fetchone()
                if data:
                    hash1 = data[8]
                    num1 = random.randrange(1111, 9999)
                    hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25newfacebankdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + uname + "','" + accno + "','" + amt + "','" + date + "','" + hash1 + "','" + hash2 + "','Withdraw')")
                    conn.commit()
                    conn.close()
                else:

                    hash1 = '0'
                    num1 = random.randrange(1111, 9999)
                    hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25newfacebankdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + uname + "','" + accno + "','" + amt + "','" + date + "','" + hash1 + "','" + hash2 + "','Withdraw')")
                    conn.commit()
                    conn.close()

            flash('Amount Transaction Successfully Balance:' + str(Amount))
            return render_template('Withdraw.html')


@app.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']
        amt = request.form['amt']
        date = datetime.datetime.now().strftime('%Y-%b-%d')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM   regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:

            price = data[11]

            Amount = float(price) + float(amt)

            print(Amount)


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute("Update regtb set Balance='" + str(Amount) + "'  where  UserName='" + uname + "' ")
        conn.commit()
        conn.close()

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor1 = conn1.cursor()
        cursor1.execute("select max(id) from transtb")
        da = cursor1.fetchone()
        if da:
            d = da[0]
            print(d)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM transtb where  id ='" + str(d) + "'   ")
            data = cursor.fetchone()
            if data:
                hash1 = data[8]
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='25newfacebankdb')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + uname + "','" + accno + "','" + amt + "','" + date + "','" + hash1 + "','" + hash2 + "','Deposit')")
                conn.commit()
                conn.close()
            else:

                hash1 = '0'
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='25newfacebankdb')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO  transtb VALUES ('','" + uname + "','" + accno + "','" + uname + "','" + accno + "','" + amt + "','" + date + "','" + hash1 + "','" + hash2 + "','Deposit')")
                conn.commit()
                conn.close()

        flash('Amount Deposit Successfully Balance:' + str(Amount))

        return render_template('Deposit.html')


@app.route("/TransactionInfo")
def TransactionInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM beneficiarytb where UserName='" + uname + "'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM transtb where UserName='" + uname + "'")
    data1 = cur.fetchall()

    return render_template('TransactionInfo.html', data=data, data1=data1)


@app.route("/ATransactionInfo")
def ATransactionInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM transtb ")
    data1 = cur.fetchall()

    return render_template('ATransactionInfo.html', data1=data1)


@app.route("/JoinUser")
def JoinUser():
    return render_template('MulitiUser.html')


@app.route("/newbeneficiary", methods=['GET', 'POST'])
def newbeneficiary():
    if request.method == 'POST':
        uname = session['uname']

        aname = request.form['aname']

        accno = request.form['accno']
        Ifsc = request.form['Ifsc']
        bname = request.form['bname']
        address = request.form['address']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into beneficiarytb values('','" + uname + "','" + aname + "','" + accno + "','" + Ifsc + "','" + bname + "','" + address + "')")
        conn.commit()
        conn.close()

    flash('New Beneficiary Info Saved!')

    return render_template('NewBeneficiary.html')


@app.route("/newmulti", methods=['GET', 'POST'])
def newmulti():
    if request.method == 'POST':
        uname = session['uname']
        Loginuser = session['loginuser']

        jname = request.form['uname']
        accno = session['acc']

        if Loginuser == uname:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25newfacebankdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into multitb values('','" + accno + "','" + jname + "')")
            conn.commit()
            conn.close()

            import LiveRecognition  as liv

            del sys.modules["LiveRecognition"]

            flash('New Join User Info Saved!')
            return render_template('MulitiUser.html')

        else:

            flash('Your Not Owner!')

            return render_template('MulitiUser.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
