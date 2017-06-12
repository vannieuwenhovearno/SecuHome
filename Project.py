from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
from DbClass import DbClass
import os
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    18 : {'name' : 'verlichting beneden', 'state' : GPIO.LOW},
    24 : {'name' : 'verlichting boven', 'state' : GPIO.LOW},
    12 : {'name': 'muziek', 'state':GPIO.LOW}
   }

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

# ----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    if 'email' in session:
        mail_session = escape(session['email'])

        database = DbClass()
        listVerlichting = database.getNameLights()

        print(listVerlichting)

        database = DbClass()
        listMuziek = database.getNameMusic()
        print(listMuziek)


        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek
        }
        return render_template('home.html', mail_session=mail_session, **templateData)
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

        database = DbClass()
        listVerlichting = database.getNameLights()

        print(listVerlichting)

        database = DbClass()
        listMuziek = database.getNameMusic()
        print(listMuziek)


        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek
        }
        return render_template('home.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route('/zonnewering')
def zonnewering():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('zonwering.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/muziek')
def muziek():
    if 'email' in session:
        mail_session = escape(session['email'])
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins
        }
        # Pass the template data into the template main.html and return it to the user
        return render_template('muziek.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/muziek/<veranderPin>/<actionMuziek>")
def actionMuziek(veranderPin, actionMuziek):
    if 'email' in session:
        mail_session = escape(session['email'])
        # Convert the pin from the URL into an integer:
        veranderPin = int(veranderPin)
        # Get the device name for the pin being changed:
        deviceName = pins[veranderPin]['name']
        # If the action part of the URL is "on," execute the code indented below:
        if actionMuziek == "on":
          # Set the pin high:
          GPIO.output(veranderPin, GPIO.HIGH)
          # Save the status message to be passed into the template:
        if actionMuziek == "off":
          GPIO.output(veranderPin, GPIO.LOW)
        if actionMuziek == "toggle":
          # Read the pin and set it to whatever it isn't (that is, toggle it):
          GPIO.output(veranderPin, not GPIO.input(veranderPin))

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

        # Along with the pin dictionary, put the message into the template data dictionary:
        templateData = {
          'pins' : pins
        }

        return render_template('muziek.html', mail_session=mail_session, **templateData)

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

pins={
    18: {'name': 'ledGelijkvloers', 'state': GPIO.HIGH},
    24: {'name': 'ledVerdiep1', 'state': GPIO.HIGH},
    12 : {'name': 'muziek', 'state':GPIO.HIGH}
}


@app.route("/verlichting")
def verlichting():
    if 'email' in session:
        mail_session = escape(session['email'])
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins
        }
        # Pass the template data into the template main.html and return it to the user
        return render_template('verlichting.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/verlichting/<changePin>/<action>")
def action(changePin, action):
    if 'email' in session:
        mail_session = escape(session['email'])
        # Convert the pin from the URL into an integer:
        changePin = int(changePin)
        # Get the device name for the pin being changed:
        deviceName = pins[changePin]['name']
        # If the action part of the URL is "on," execute the code indented below:
        if action == "on":
          # Set the pin high:
          GPIO.output(changePin, GPIO.HIGH)
          # Save the status message to be passed into the template:
        if action == "off":
          GPIO.output(changePin, GPIO.LOW)
        if action == "toggle":
          # Read the pin and set it to whatever it isn't (that is, toggle it):
          GPIO.output(changePin, not GPIO.input(changePin))

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

        # Along with the pin dictionary, put the message into the template data dictionary:
        templateData = {
          'pins' : pins
        }

        return render_template('verlichting.html', mail_session=mail_session, **templateData)

    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host="0.0.0.0"
    app.run(host=host, port=port,debug=True)
