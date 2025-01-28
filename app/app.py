from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date, timedelta, timezone

app = Flask(__name__)

# Configuration
app.secret_key = "Abegamer"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

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

# Initialize database
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(full_name=full_name, username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e):
                flash("Username already exists", "error")
            else:
                flash("An error occurred while creating the account", "error")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Please fill out both fields", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in to access the dashboard", "error")
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    # Fetch incomes and expenses for the logged-in user
    incomes = Income.query.filter_by(user_id=user.id).all()
    expenses = Expense.query.filter_by(user_id=user.id).all()

    # Calculate total income and expense
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    overall = total_income - total_expense

    #Group expenses by catagory and calculate total 
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    categories = list(category_totals.keys())
    category_values = list(category_totals.values())

    # Calculate data for the current week
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week

    weekly_labels = []
    weekly_income = []
    weekly_expense = []
    weekly_overall = []

    for i in range(7):  # For each day of the week
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
  
    

    # Pass the data to the template
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
        categories=categories,
        category_values=category_values,
    )

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
            amount = float(request.form['amount'])  # Convert to float
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')  # Parse date

            new_expense = Expense(category=category, type=type_, amount=amount, date=date, user_id=user.id)

            db.session.add(new_expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")

    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    return render_template('expense.html', username=username, expenses=expenses)

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

@app.route('/overview')
def overview():
    if 'username' not in session:
        flash("Please log in to access this page", "error")
        return redirect(url_for('login'))

    return render_template('overview.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
