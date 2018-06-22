# -*- coding=utf-8 -*-
# author = "tungtt"

from flask import Flask, request , render_template
import json
from tfidf_model import TfidfModel

model = TfidfModel('data/phat_trien_ky_nang/train.txt','data/phat_trien_ky_nang/corpus_train.txt')
app = Flask('qa')


@app.route('/',methods = ['GET'])
def homepage():
	return render_template('home.html')


@app.route('/qa', methods=['POST'])
def process_request():
    data = request.get_data()
    # handle = Thread(target=save_new_sen,args=(data,))
    # handle.start()
    print data
    x = model.get_sim(data)
    if len(x) == 0:
        return "none"
    else:
        x = json.dumps(x)
        print ('Response data to client .')
        return x

@app.route('/update' , methods = ['POST'])
def update():
    data = request.get_data()
    true_data = data.split("---");
    ques = true_data[0]
    ans = true_data[1]
    model.update(ques,ans)
    print("Model updated!!!")
    return "OK"

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response



if __name__ == '__main__':
    app.run(port = 8008)