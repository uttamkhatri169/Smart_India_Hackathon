from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, User, RawData, OutputData, ComparisonData
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists with this email.', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('index'))  # Redirect to the data route
            else:
                flash('Wrong password. Please try again.', 'danger')
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/data')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    raw_data = RawData.query.paginate(page=page, per_page=10)
    output_data = OutputData.query.all()
    comparison_data = ComparisonData.query.all()
    return render_template('rawdata.html', raw_data=raw_data, output_data=output_data, comparison_data=comparison_data)

@app.route('/graph')
@login_required
def graph():
    # Load the CSV file
    df = pd.read_csv('final_data.csv')
    
    # Ensure 'datetime' column is in the correct datetime format
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d-%m-%Y %H:%M')
    
    # Create figures for each region
    regions = ['DELHI', 'BRPL', 'BYPL', 'NDMC', 'MES']
    graphs = {}
    
    for region in regions:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['datetime'], y=df[region], name=region))
        fig.update_layout(
            title=f'Megawatt Usage Over Time in {region}',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        graphs[region] = pio.to_html(fig, full_html=False)
    
    return render_template('model.html', graphs=graphs)

if __name__ == '__main__':
    app.run(debug=True)
