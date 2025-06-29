import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import re
import plotly.express as px
import plotly.graph_objects as go
from flask import *
import mysql.connector
import pickle

db=mysql.connector.connect(host='localhost',user="root",password="",port='3306',database='Intrusion')
cur=db.cursor()


app=Flask(__name__)
app.secret_key = "fghhdfgdfgrthrttgdfsadfsaffgd"

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        useremail=request.form['useremail']
        session['useremail']=useremail
        userpassword=request.form['userpassword']
        sql="select count(*) from user where Email='%s' and Password='%s'"%(useremail,userpassword)
        # cur.execute(sql)
        # data=cur.fetchall()
        # db.commit()
        x=pd.read_sql_query(sql,db)
        print(x)
        print('########################')
        count=x.values[0][0]

        if count==0:
            msg="user Credentials Are not valid"
            return render_template("login.html",name=msg)
        else:
            s="select * from user where Email='%s' and Password='%s'"%(useremail,userpassword)
            z=pd.read_sql_query(s,db)
            session['email']=useremail
            pno=str(z.values[0][4])
            print(pno)
            name=str(z.values[0][1])
            print(name)
            session['pno']=pno
            session['name']=name
            return render_template("userhome.html",myname=name)
    return render_template('login.html')

@app.route('/registration',methods=["POST","GET"])
def registration():
    if request.method=='POST':
        username=request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        conpassword = request.form['conpassword']
        Age = request.form['Age']
        
        contact = request.form['contact']
        if userpassword == conpassword:
            sql="select * from user where Email='%s' and Password='%s'"%(useremail,userpassword)
            cur.execute(sql)
            data=cur.fetchall()
            db.commit()
            print(data)
            if data==[]:
                
                sql = "insert into user(Name,Email,Password,Age,Mob)values(%s,%s,%s,%s,%s)"
                val=(username,useremail,userpassword,Age,contact)
                cur.execute(sql,val)
                db.commit()
                msg="Registered successfully","success"
                return render_template("login.html",msg=msg)
            else:
                msg="Details are invalid","warning"
                return render_template("registration.html",msg=msg)
        else:
            msg="Password doesn't match", "warning"
            return render_template("registration.html",msg=msg)
    return render_template('registration.html')


@app.route('/view data',methods = ["POST","GET"])
def view_data():
    df = pd.read_csv('final_data.csv')
    df1 =df.head(100)
    return render_template('view data.html',col_name = df1.columns,row_val = list(df1.values.tolist()))



if __name__=="__main__":
    app.run(debug=True)