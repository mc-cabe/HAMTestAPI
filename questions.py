import requests
import os

import sys
import re
from bs4 import BeautifulSoup


# url = "https://hamexam.org/view_pool/15-Technician"
url = "https://hamexam.org/view_pool/15-Technician?class=flashCard"
count = 1
headers = {
    'cache-control': "no-cache",
    'postman-token': "0d130261-d5b0-7823-315a-83cd292d922c"
    }

response = requests.request("GET", url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# print(response.text)
#
# try:
#     all = re.findall('questionText\">(.*\n.*\n.*\n.*\n.*\n.*\n.*)</ul',response.text)
#     questions = re.findall('questionText\">(.*)</p>',response.text)
#     options = re.findall('<li(.*)</li>',response.text)
#
# except AttributeError:
#     text = ''
questions_bank = []
answers_bank = []
letters = []
top_score = 0
i = 0
j = 0




for idx, questions in enumerate(soup.find_all('p','questionText')):
    questions_bank.append([idx,questions.text.strip()])

for idx, answers in enumerate(soup.find_all('ul')):
    for id, incorrect in enumerate(answers.find_all('span','noMarks')):

        answers_bank.append([idx,id,incorrect.text.strip(),None])

    for id, correct in enumerate(answers.find_all('li','correctAnswer')):
        letter = correct.find("span","answerLabel")
        letter = letter.text.strip('.')

        letters.append([idx,letter])



def quizMe():
    i = 0
    top_score = 1
    curr_score = 0
    os.system('clear')

    while i < len(questions_bank):
        print "(q or quit to quit) \n \n"
        print " ****************** HIGH SCORE:",top_score,"******************"
        print  "\n ******************* QUESTION ",i+1,'*********************** \n\n'
        print questions_bank[i][1]
        print "------------------------------------"
        print answers_bank[i*4][2]
        print answers_bank[i*4+1][2]
        print answers_bank[i*4+2][2]
        print answers_bank[i*4+3][2]

        print "Answer is:",letters[i][1] #ANSWER
        # return
        text = raw_input("\nEnter A,B,C,D:  ").decode('utf-8').upper()
        if (text == letters[i][1]):
            i=i+1
            curr_score = curr_score + 1
            if (curr_score > top_score): top_score = curr_score
            os.system('clear')


        elif (text == "Q" or text == 'QUIT'):

            sys.exit("exiting program")
        else:
            os.system('clear')
            print "************\n incorrect, answer is ",letters[i][1]
            print "top score of :",top_score
            print "\n\n RESTARTING TO QUESTION 1"
            i = 0
            top_score = 0
            curr_score = 1


quizMe()
