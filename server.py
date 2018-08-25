from flask import Flask, render_template, redirect, request, session, flash, url_for
import re
import requests
import sys
import os

from bs4 import BeautifulSoup



app = Flask(__name__)    # Global variable __name__ tells Flask whether or not we are running the file
app.secret_key = "ThisIsSecret!"
@app.route('/')          # The "@" symbol designates a "decorator" which attaches the following
                         # function to the '/' route. This means that whenever we send a request to
                         # localhost:5000/ we will run the following "hello_world" function.
def index():
    url = "https://hamexam.org/view_pool/15-Technician?class=flashCard"
    count = 1

    headers = {
        'cache-control': "no-cache",
        'postman-token': "0d130261-d5b0-7823-315a-83cd292d922c"
        }

    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    questions_bank = []
    answers_bank = []
    letters = []
    top_score = 0

    j = 0
    i = 0

    if not 'i' in session:
        session['i'] = 0
    else:
        session['i'] = session['i']

    i = session['i']

    print i
    if i < 11:
        category = 'Power circuits and hazards'
    elif i >= 11 and i < 24:
        category = 'Antenna safety'
    elif i >= 24 and i < 37:
        category ='RF hazards'
    elif i >= 37 and i < 48:
        category ='Amateur Radio Service'
    elif i >= 48 and i < 60:
        category ='Authorized frequencies'
    elif i >= 60 and i < 71:
        category ='Operator licensing'
    elif i >= 71 and i < 82:
        category ='Authorized and prohibited transmission'
    elif i >= 82 and i < 93:
        category ='Control operator and control types'
    elif i >= 93 and i < 104:
        category ='Station identification'
    elif i >= 104 and i < 116:
        category ='Station operation: choosing an operating frequency'
    elif i >= 116 and i < 130:
        category ='VHF/UHF operating practices'
    elif i >= 130 and i < 142:
        category ='Public service: emergency and non-emergency operations '
    elif i >= 142 and i < 155:
        category ='Radio wave characteristics'
    elif i >= 155 and i < 166:
        category ='Radio and electromagnetic wave properties'

    elif i >= 166 and i < 177:
        category = 'Propagation modes: line of sight'
    elif i >= 177 and i < 188:
        category = ' Station setup'

    elif i >= 188 and i < 201:
        category ='Operating controls'
    elif i >= 201 and i < 215:
        category ='Electrical principles, units, and terms'

    elif i >= 215 and i < 228:
        category ='Math for electronics'
    elif i >= 228 and i < 242:
        category ='Electronic principles: capacitance; inductance'
    elif i >= 242 and i < 258:
        category =' Ohms Law'
    elif i >= 258 and i < 269:
        category ='Electrical components'
    elif i >= 269 and i < 280:
        category ='Semiconductors'
    elif i >= 280 and i < 293:
        category ='Circuit diagrams'

    elif i >= 293 and i < 305:
        category = ' Component functions'

    elif i >= 305 and i < 316:
        category = 'Station equipment'

    elif i >= 316 and i < 328:
        category = 'Common transmitter and receiver problems'

    elif i >= 328 and i < 340:
        category = 'Antenna measurements and troubleshooting'
    elif i >= 340 and i < 352:
        category = 'Basic repair and testing: soldering'
    elif i >= 352 and i < 363:
        category = 'Modulation modes: bandwidth of various signals'
    elif i >= 363 and i < 375:
        category = 'Amateur satellite operation'
    elif i >= 375 and i < 386:
        category = ' Operating activities: radio direction finding'
    elif i >= 386 and i < 400:
        category = 'Non-voice and digital communications'
    elif i >= 400 and i < 412:
        category = 'Antennas, vertical and horizontal polarization'
    elif i >= 412 and i < 422:
        category = 'Feed lines: types, attenuation vs frequency, selecting'
    else:
        session['i'] = 0
        category = 'Congrats you hit the end!'


    if not 'top_score' in session:
        session['top_score'] = 1
    else:
        session['top_score'] = session['top_score']

    if not 'current_score' in session:
        session['current_score'] = 0
    else:
        session['current_score'] = session['current_score']


    for idx, questions in enumerate(soup.find_all('p','questionText')):
        questions_bank.append([idx,questions.text.strip()])

    for idx, answers in enumerate(soup.find_all('ul')):
        for id, incorrect in enumerate(answers.find_all('span','noMarks')):

            answers_bank.append([idx,id,incorrect.text.strip(),None])

        for id, correct in enumerate(answers.find_all('li','correctAnswer')):
            letter = correct.find("span","answerLabel")
            letter = letter.text.strip('.')

            letters.append([idx,letter])


    i = session['i']

    question = questions_bank[i][1]
    print question
    session['letter'] = letters[i][1]


    if i == len(questions_bank)-1:
        flash(u'you have answered every question, please reset', 'success')
    else:
        a = answers_bank[i*4][2]
        b = answers_bank[i*4+1][2]
        c = answers_bank[i*4+2][2]
        d = answers_bank[i*4+3][2]
    return render_template("index.html", i = session['i'],current_score = session['current_score'], top_score= session['top_score'], question = question, a=a,b=b,c=c,d=d, letter = session['letter'], category = category )


@app.route('/submit', methods= ['POST'])
def check():
    option = request.form['options']

    print "option:", option
    print "seshL:",session['letter']
    letter = session['letter']
    if option == letter:
        session['current_score'] = session['current_score']+1

        if (session['current_score'] > session['top_score']):
            session['top_score'] = session['current_score']

        session['i']=session['i']+1
        flash(u'Correct!  '+session['letter'], 'success')
        return redirect('/')
        # flash("Correct!", 'success')
    else:
        session['current_score'] = 0
        flash(u'Incorrect!', 'danger')
        return redirect('/')

@app.route('/change', methods = ['POST'])
def change():
    new_vals = request.form['new_vals']
    val = int(new_vals)
    session['i'] = val
    return redirect('/')

    # return render_template("index.html", i = session['i'], top_score= session['top_score'], letter = session['letter'] )

@app.route('/reset',methods= ['POST'])

def reset():
    # button = request.form['button']
    # session['counter']=0
    session.pop('i')
    session.pop('current_score')
    session['current_score']=0
    session.pop('letter')
    return redirect('/')


app.run(debug=True)      # Run the app in debug mode.
