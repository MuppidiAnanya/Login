from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginpage.db'


db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique = True)
    password = db.Column(db.String(600), nullable=False)
    fullname =  db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False, unique = True)
    pincode = db.Column(db.String(20),nullable = False)



with app.app_context():
    db.create_all()





@app.route('/')
def index():
  return ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            flash('Please fill all fields')
            return redirect(url_for('login'))


        user = Customer.query.filter_by(username=username).first()
        if user:
            if user.password != password:
                flash('Incorrect password')
                return redirect(url_for('login'))
            
            else:
                session['id'] = user.id
                return redirect(url_for('index'))

      


@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname').title()
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        if username=='' or password =='' or fullname=='' or address=='' or pincode=='':
            flash('Please fill all fields')
            return redirect(url_for('register'))
        if Customer.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        user = Customer(username=username,password=password,fullname=fullname,address=address,pincode=pincode)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    return render_template('createAccount.html')
