#Importing Required Python Libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date, timedelta, timezone
from collections import defaultdict


app = Flask(__name__)

# Configuration for Security
app.secret_key = "AbelMengesha"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

# Creating SQLAlchemy to manage the database and starting bcrypt for hashing user password for security 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Models for The user and for the web app data
#User Database Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
#Web app database model
class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return f"<Expense {self.category} - {self.amount}>"

class Income(db.Model):
    __tablename__ = 'income' 
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('incomes', lazy=True))

    def __repr__(self):
        return f"<Income {self.reason} - {self.amount}>"

#Creating the database which is the model given above
with app.app_context():
    db.create_all()

#Connecting the templates route

#Home Page
@app.route('/')
def home():
    return render_template('home.html')

#Registration Page
#sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':#Getting input Variables from the user
        full_name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')#Encrypting the user password by bcrypt

        new_user = User(full_name=full_name, username=username, password=hashed_password)#Assigning session for the user to send it to the database
        
        try:
            db.session.add(new_user)#adding the user data to the database table
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except Exception as e:#Chceck if the username is on the database
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e):
                flash("Username already exists", "error")
            else:#Used to Handle any other error if occured 
                flash("An error occurred while creating the account", "error")
    return render_template('signup.html')
#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Please fill out both fields", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()# Checks the database

        if user and bcrypt.check_password_hash(user.password, password):#Conditions if the user is on the database and redirect him/or to the dashboard
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:#If the there is mismatch of username and password prints the flash message
            flash("Invalid credentials", "error")
    return render_template('login.html')
#The Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session: #It handles if the user not logged in (it will not be able to access the page)
        flash("Please log in to access the dashboard", "error")
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()#Matches the username from database to access the page

    #Used to get expense and income from the database to display in the dashboard
    incomes = Income.query.filter_by(user_id=user.id).all()
    expenses = Expense.query.filter_by(user_id=user.id).all()

    # Calculates the sums of the variables given and used to represent the data as a chart using javascript
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    overall = total_income - total_expense

    # Calculate data for the week by getting dates and amount for expense and income
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Used to start the week from Monday

    #Creating empty listto store
    weekly_labels = []
    weekly_income = []
    weekly_expense = []
    weekly_overall = []

    for i in range(7):  # For loop to start from Monday to Sunday each by each
        current_day = start_of_week + timedelta(days=i)
        daily_income = sum(
            income.amount for income in incomes if income.date.date() == current_day
        )
        daily_expense = sum(
            expense.amount for expense in expenses if expense.date.date() == current_day
        )
        daily_overall = (daily_income - daily_expense)
        
        weekly_labels.append(current_day.strftime('%A'))  # Add day name
        weekly_income.append(daily_income)
        weekly_expense.append(daily_expense)
        weekly_overall.append(daily_overall)
  
    

    #Used to Pass the data to the template
    return render_template(
        'dashboard.html',
        username=username,
        total_income=total_income,
        total_expense=total_expense,
        incomes=incomes,
        expenses=expenses,
        overall=overall,
        weekly_labels=weekly_labels,
        weekly_income=weekly_income,
        weekly_expense=weekly_expense,
        weekly_overall=weekly_overall,
        
    )
#Expense Calculator Page
@app.route('/expense', methods=['GET', 'POST'])
def expense():
    if 'username' not in session:
        flash("Please log in to access this page", "error")
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        try:
            category = request.form['category']
            type_ = request.form['type']
            amount = float(request.form['amount']) 
            date = datetime.strptime(request.form['date'], '%Y-%m-%d') 

            new_expense = Expense(category=category, type=type_, amount=amount, date=date, user_id=user.id)

            db.session.add(new_expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")

    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    return render_template('expense.html', username=username, expenses=expenses)
#Income Calculator Page
@app.route('/income', methods=['GET', 'POST'])
def income():
    if 'username' not in session:
        flash("Please log in to access this page", "error")
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        try:
            reason = request.form['reason']
            amount = float(request.form['amount'])  # Convert to float
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')  # Parse date

            new_income = Income(reason=reason, amount=amount, date=date, user_id=user.id)

            db.session.add(new_income)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")

    incomes = Income.query.filter_by(user_id=user.id).order_by(Income.date.desc()).all()
    return render_template('income.html', username=username, income=incomes)
#Overview Data monitoring page
@app.route('/overview')
def overview():
    if 'username' not in session:
        flash("Please log in to access this page", "error")
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    expenses = Expense.query.filter_by(user_id=user.id).all()
    incomes = Income.query.filter_by(user_id=user.id).all()

    expense_totals = defaultdict(float)
    for expense in expenses:
        expense_totals[expense.category] += expense.amount


    income_totals = defaultdict(float)
    for income in incomes:
        income_totals[income.reason] += income.amount

    expense_labels = list(expense_totals.keys())
    expense_values = list(expense_totals.values())

    income_labels = list(income_totals.keys())
    income_values = list(income_totals.values())

    return render_template(
        'overview.html',
        username=username,
        expense_labels=expense_labels,
        expense_values=expense_values,
        income_labels=income_labels,
        income_values=income_values
    )
#Logout Button to exit the user session 
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

#End of the Code