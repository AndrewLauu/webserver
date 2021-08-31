from flask import Flask
from flask import render_template as rt
from flask import request,redirect,abort
import subprocess as sp
import json

app=Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def check_password():
    return rt('password.html')

@app.route('/index')
def index():
    ref=request.referrer
    if not ref:
        abort(403)

    d=getSMS()
    t1,t2,t3=d.keys()
    s1,s2,s3=d.values()
    return rt('index.html',s1=s1,s2=s2,s3=s3,t1=t1,t2=t2,t3=t3)

def getSMS():
    cmd='termux-sms-list -t inbox -f 10086'
    p=sp.Popen(cmd,shell=True,stdout=sp.PIPE)
    out=p.stdout.read().decode('utf8')
    j=json.loads(out)
    sms={i['received']:i['body'] for i in j[::-1][:3]}
    return sms

@app.route('/form', methods=['POST', 'GET'])
def bio_data_form():    
    if request.method == "POST":
        username = request.form['username']        
        age = request.form['age']
        email = request.form['email']       
        hobbies = request.form['hobbies']        
        return redirect(url_for('showbio',username=username,age=age,email=email,hobbies=hobbies))    
    return rt("form.html")


if __name__=='__main__':
    app.run(host='0.0.0.0')
