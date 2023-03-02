from flask import Flask, flash, render_template, url_for, request, jsonify, session, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random
import json
import numpy as np
import datetime
import os

import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from keras.utils import load_img, img_to_array
import glob
import cv2 as cv
from PIL import Image as im

from klasifikasi import cnn_model

app = Flask(__name__)
CORS(app)
app.secret_key = "check" 
  
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 4024 * 4024
app.config['UPLOAD_EXTENSIONS']  = ['.jpg','.JPG','.PNG','.png','.jpeg','.JPEG']
app.config['UPLOAD_PATH']        = './static/images/uploads/'
app.config['REKOMENDASI_PATH']   = './static/images/recommendation/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hair'

mysql = MySQL(app) 

model_cnn = cnn_model()

lemmatizer = WordNetLemmatizer()

with open('chatbot/chatbot.json') as content:
  intents = json.load(content)

words = []
classes = []
documents = []
ignore_letters = ['?', '!',',','.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag =[]
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu')) 
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

@app.route("/", methods=['GET', 'POST'])
def login():
    if session.get('login') == True:
        return redirect(url_for('history'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone() 
        if account != None:
            session['login'] = True
            # msg = 'Login Success'
            # flash(msg)
            return redirect(url_for('history'))
        else:
            msg = 'Login Fail!'
            flash(msg, 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/history", methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        if session.get('login') == True:
            date = datetime.datetime.now()
            tanggal = date.strftime("%Y-%m-%d")
            cursor = mysql.connection.cursor()
            query = "SELECT id, image, face, DATE_FORMAT(FROM_UNIXTIME(timestamp), '%Y-%m-%d %H:%i:%s') FROM history WHERE DATE_FORMAT(FROM_UNIXTIME(timestamp), '%Y-%m-%d') = '{0}'".format(tanggal)
            cursor.execute(query)
            recommendation = cursor.fetchall()
            cursor.close()
            return render_template("history.html", recommendation=recommendation)
        else:
            return redirect(url_for('login'))
    elif request.method == 'POST' and 'filtertanggal' in request.form:
        if session.get('login') == True:
            filtertanggal = request.form['filtertanggal']
            cursor = mysql.connection.cursor()
            query = "SELECT id, image, face, DATE_FORMAT(FROM_UNIXTIME(timestamp), '%Y-%m-%d %H:%i:%s') FROM history WHERE DATE_FORMAT(FROM_UNIXTIME(timestamp), '%Y-%m-%d') = '{0}'".format(filtertanggal)
            print(query)
            cursor.execute(query)
            recommendation = cursor.fetchall()
            cursor.close()
            return render_template("history.html", recommendation=recommendation)
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('login', False)
    return redirect(url_for('login'))

@app.route("/chatbot", methods=['GET', 'POST'])
def chatbot():  
    if request.method == 'GET':
        return 'test api'
    else:
        message_input = request.get_json().get("message")
        ints = predict_class(message_input)
        res = get_response(ints, intents)
        message = {"answer": res}
            
        return jsonify(message) 

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    result_predict  = '(none)'
    classess = ['Diamond','Heart','Oblong','Oval','Round','Square','Triangle']

    uploaded_file = request.files['file']
    
    curent_time = datetime.datetime.now()
    timestamp = curent_time.timestamp()
    filename = str(timestamp).replace(".", "") + '.jpg'
    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    path = os.path.join(app.config['UPLOAD_PATH'], filename)
    img = load_img(path, target_size=(200,200))
    x = img_to_array(img)
    y = np.expand_dims(x, axis=0)
    images = np.vstack([y])
    classes = model_cnn.predict(images, batch_size=50)
    classes = np.argmax(classes)
  
    #Klasifikasi
    if classes==0:
        diamond = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Diamond\*g")]
        print(classess[classes])
    elif classes==1:
        heart = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Heart\*g")]
        print(classess[classes])
    elif classes==2:
        oblong = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Oblong\*g")]
        print(classess[classes])
    elif classes==3:
        oval = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Oval\*g")]
        print(classess[classes])
    elif classes==4:
        round = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Round\*g")]
        print(classess[classes])
    elif classes==5:
        square = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Square\*g")]
        print(classess[classes])
    else:
        triangle = [cv.imread(file) for file in glob.glob(".\dataset\model_rambut\Triangle\*g")]
        print(classess[classes])

    result_predict = classes
    face = classess[classes]

    listimage = list()
    for i in range(4):
        if (result_predict == 0 ):
            data = im.fromarray(cv.cvtColor(diamond[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 1):
            data = im.fromarray(cv.cvtColor(heart[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 2):
            data = im.fromarray(cv.cvtColor(oblong[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 3):
            data = im.fromarray(cv.cvtColor(oval[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 4):
            data = im.fromarray(cv.cvtColor(round[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 5):
            data = im.fromarray(cv.cvtColor(square[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))
        elif (result_predict == 6):
            data = im.fromarray(cv.cvtColor(triangle[i], cv.COLOR_RGB2BGR))
            resultimage = str(timestamp).replace(".", "") + str(random.randint(0, 1000)) + '.jpg'
            listimage.append(resultimage)
            data.save(os.path.join(app.config['REKOMENDASI_PATH'], resultimage))

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO history (image, face, timestamp) VALUES (%s, %s, %s)''', (filename, face, timestamp))
    mysql.connection.commit()
    cursor.close()

    return jsonify({
        "Face": face,
        "Recommendation": listimage,
    })

if __name__ == "__main__":
    model.load_weights('./chatbot/chatbotmodel.h5')
    model_cnn.load_weights('./model.h5')
    app.run(host="0.0.0.0", debug=True)