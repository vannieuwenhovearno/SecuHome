from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
from DbClass import DbClass
import os
import RPi.GPIO as GPIO

app = Flask(__name__)

@app.route('/')
def home():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('home.html', mail_session=mail_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    database = DbClass()
    error = None
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email_form = request.form['email']
        password_form = request.form['password']

        list_user = database.getUser(email_form)
        print(list_user)

        for user in list_user:
            if email_form == user[2]:
                UserTrying = user
                print(UserTrying)

                password = password_form
                salt = "?a4D.&oD8!éM_°"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                if fullpassword == UserTrying[3]:
                    session['email'] = request.form['email']
                    return redirect(url_for('home'))
                else:
                    error = "Dit wachtwoord komt niet overeen met deze gebruiker"
            else:
                error = "Deze gegevens bestaan niet in onze database"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

app.secret_key = 'sdh//*gfg4e--z64tg-s68dtu7r8§!4è'




@app.route('/registreren' , methods=['GET', 'POST'])
def registreren():
    database = DbClass()
    error = None
    if request.method == 'POST':
        fullname_form = request.form['fullname']
        email_form = request.form['email']
        password_form = request.form['password']
        passwordConf_form = request.form['confPassword']

        list_user = database.getUser(email_form)

        if list_user == []:
            if password_form == passwordConf_form:

                password = password_form
                salt = "?a4D.&oD8!éM_°"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                database = DbClass()
                database.setNewUser(fullname_form,email_form,fullpassword)
                return render_template('login.html')
            else:
                error = "De 2 wachtwoorden komen niet overeen."
        else:
            error = "Deze gegevens bestaan al in onze database"

    return render_template('registreren.html', error=error)

@app.route('/wachtwoord-vergeten')
def wachtwoord_vergeten():
    return render_template('wachtwoord_vergeten.html')

@app.route('/home')
def start():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('home.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/zonnewering')
def zonnewering():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('zonwering.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/verlichting')
def verlichting():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('verlichting.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/muziek')
def muziek():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('muziek.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/grafieken')
def grafieken():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('grafieken.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('contact.html', mail_session=mail_session)
    return redirect(url_for('login'))

def ledBenedenAan():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    return True;


if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host="0.0.0.0"
    app.run(host=host, port=port,debug=True)
