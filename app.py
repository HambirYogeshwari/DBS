from flask import Flask,render_template,redirect,request
from flask import jsonify
from flask.helpers import url_for
from datetime import *
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone 
from sqlalchemy.orm import defaultload
import psycopg2

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:gopireddy@localhost/hacks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisismykey'
db = SQLAlchemy(app)


#-------------------------------DATABASE CREATION------------------------------------------------
#-------------------------------TABLE CREATION---------------------------------------------------
class Stocks(db.Model):
    __tablename__='stocks'
    s_no = db.Column(db.Integer)
    stock_name = db.Column(db.String(40),primary_key = True)
    ordered_qty=db.Column(db.Integer)
    stock_cost = db.Column(db.Integer)
    ordered_type=db.Column(db.String(40))
    ordered_status=db.Column(db.String(40),default = 'PLACED')
    ordered_date = db.Column(db.Date,default = date.today(),nullable=False)
    
@app.route("/")
def entry():
    return render_template("cu.html")
@app.route("/", methods=["POST"])
def workersnewdata():
    stock_name=request.form.get("stock_name")
    order_quant=request.form.get("order_quant")
    price=request.form.get('price')
    order_type=request.form.get('order_type')
    
    pro=Stocks(stock_name =stock_name,ordered_qty=order_quant,stock_cost =price,ordered_type=order_type)
    db.session.add(pro)
    db.session.commit()
    return render_template("cu.html",msg="data added successfully..!!")

@app.route("/admin")
def basic_admin():
    data = Stocks.query.all()
    return render_template("ad.html",data=data)
@app.route("/admin",methods=["POST"])
def stocks_info():
    stock_name=request.form.get('name')
    data = Stocks.query.filter_by(order_status=stock_name).all()

    return render_template("ad.html",data=data)


if __name__=='__main__' :
    db.create_all()
    app.run(debug=True)