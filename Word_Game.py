from flask import Flask, session, render_template, request
from collections import Counter
import random, time, datetime, math

app = Flask(__name__)


def get_source_word() -> str:               #gets a random source word
    with open('large.txt') as words:
        source_word = []
        for w in words:
            source_word.append(w.strip())
        w2 = random.choice(source_word)
    return w2            


@app.route('/')
@app.route('/showform')
def display_form() -> 'html':
    session['source_word'] = get_source_word()
    session['time_stamp'] = time.time()
    return render_template('get_input.html',
                           title='Word Game',
                           source_word = session['source_word'],
                           time_stamp = session['time_stamp'])


def check_if_valid(word) -> bool:           #checks if input is a real word
    with open('small.txt') as sf:
        for w in sf:
            if w.strip() == word:
                return True
    return False
        
def compare_letters(w, s) -> bool:                  #compares the letters in the words
    c_source  = Counter(s)
    c_word =  Counter(w)   
    for k, v in c_word.items():
        if c_source[k] >= v:
            pass
        elif c_source[k] == 0:
            return False
        else:
            return False
    return True        


@app.route('/processform', methods=['POST'])
def process_the_data() -> 'html':
    valid_words1 = []
    invalid_words = []
    valid_words2 = []
    num_of_invalid = 0
    st = time.time()
    
    for k, v in request.form.items():
        if k == 'hidden_time_stamp':
            ft = v
            first_stamp = datetime.datetime.fromtimestamp(float(ft)).strftime('%H:%M:%S')
            session['first_stamp'] = first_stamp
            second_stamp = datetime.datetime.fromtimestamp(st).strftime('%H:%M:%S')
            session['second_stamp'] = second_stamp
            player_time = float(st) - float(ft)
            session['player_time'] = math.ceil(player_time*100)/100
            
    for k, v in request.form.items():
        if k == 'hidden_source_word' or k == 'hidden_time_stamp':
            pass
        else:
            v2 = v.lower()
            if check_if_valid(v2) and v2 != session['source_word']:      #splits the valid and invalid words
                if compare_letters(v2, session['source_word']):
                    valid_words1.append(v2)
                else:
                    invalid_words.append(v2)
            else:
                invalid_words.append(v2)
    session['invalid_words'] = invalid_words

    set_of_valids = set(valid_words1)       #stops duplicate answers
    num_of_valid = len(set_of_valids)
    for w in set_of_valids:        
            valid_words2.append(w)                  
    session['valid_words'] = valid_words2
    if len(invalid_words) > 0:              #gets the number of invalid
        for w in invalid_words:
            num_of_invalid = num_of_invalid + 1
    session['num_of_invalid'] = num_of_invalid
        

    if num_of_valid == 7:
        return render_template('user_name.html',
                           title='Word Game',
                           source_word = session['source_word'],
                           first_stamp = session['first_stamp'],
                           second_stamp = session['second_stamp'],
                           player_time = session['player_time'],
                           valid_words = session['valid_words'])
    
    return render_template('you_failed.html',
                           title='Word Game',
                           num_of_invalid = session['num_of_invalid'],
                           invalid_words = session['invalid_words'],
                           source_word = session['source_word'])
    


@app.route('/score', methods=['POST'])
def score_board():
    scores = []
    for k, v in request.form.items():       
        if k == 'user_name':                
            user_name = v                      

    score = (session['player_time'], user_name)
            
    with open('score.txt', 'a') as fh:
        print(score, file=fh)
        
    with open('score.txt') as top:
        for w in top:
            scores.append(w.strip())
            
    score_board = [eval(t) for t in scores] 
    top_ten = sorted(score_board)[:10]
    session['first'] = top_ten[0]
    session['second'] = top_ten[1]
    session['third'] = top_ten[2]
    session['fourth'] = top_ten[3]
    session['fifth'] = top_ten[4]
    session['sixth'] = top_ten[5]
    session['seventh'] = top_ten[6]
    session['eight'] = top_ten[7]
    session['ninth'] = top_ten[8]
    session['tenth'] = top_ten[9]
        
    
    return render_template('top_ten.html',
                           title='Word Game',
                           first = session['first'],
                           second = session['second'],
                           third = session['third'],
                           fourth = session['fourth'],
                           fifth = session['fifth'],
                           sixth = session['sixth'],
                           seventh = session['seventh'],
                           eight = session['eight'],
                           ninth = session['ninth'],
                           tenth = session['tenth'])                           

app.secret_key = 'kjvHVYIuypmpjRDHgdflrDTy'

if __name__ == '__main__':    
    app.run(debug = True)
