import pyrebase 
from datetime import date,datetime
from flask import Flask, render_template, request, redirect,session
config={
    
    "apiKey": "AIzaSyDbX-U9I6kRFacOepvlLF7fDSOnrPbNglw",
    "authDomain": "pradem-2e2ae.firebaseapp.com",
    "databaseURL": "https://pradem-2e2ae.firebaseio.com",
    "projectId": "pradem-2e2ae",
    "storageBucket": "pradem-2e2ae.appspot.com",
    "messagingSenderId": "918004148066",
    "appId": "1:918004148066:web:204751a326f984ea72ee3b",
    "measurementId": "G-N8ZTFZZKLQ"

}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Main.html')

@app.route('/CustomerLogin', methods=['GET','POST'])
def customerLogin():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        auth.sign_in_with_email_and_password(email,password)
    return render_template('Customer_Login.html')

@app.route('/AdminLoginl', methods=['GET','POST'])
def adminLogin():
    return render_template('Admin_login.html')

@app.route('/signup',methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = auth.create_user_with_email_and_password(email,password)
        return render_template('Customer_Login.html')
    return render_template('signup.html')

@app.route('/main',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        problem = request.form['problem']
        phone = request.form['phone']
        db.child("latest_patents").push(name)
        db.child("latest_patents").child(name).update({"phone":phone})
        db.child("latest_patents").child(name).update({"email":email})
        db.child("latest_patents").child(name).update({"problem":problem})
        na=db.child("latest_patents").get()
        to=na.val()
        temp={}
        t=[]
        count=1
        t_t=""
        now=datetime.now()
        dt_string=now.strftime("%d/%m/%Y")
        H=now.strftime("%H")
        M=now.strftime("%M")
        m=int(M)
        h=int(H)
        hh="12"
        for i in to.values():
            m=m+30
            mm=str(m)
            if m>=60:
                h=h+1
                hh=str(h)
                m=0
                if m==0:
                    mm=str(m)+str("0")                
                if(h==24):
                    h=0
                    if h==0:
                        hh=str(h)+str("0")
            if type(i)!=type(temp):
                t_t=t_t+str(count)+"."+i+" "+str(dt_string)+" "+hh+":"+mm
                t.append(t_t)
                count+=1
                t_t=""
        return render_template('CustomerMain.html',tt=t,len=count-1)
    return render_template('CustomerMain.html')
if __name__ == '__main__':
    app.run(debug=True)