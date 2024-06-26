from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db
from werkzeug import exceptions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/ochemto')
def about():
    return render_template('about.html')
@app.route('/zal')
def concert():
    return render_template('concert.html')
@app.route('/festivals')
def fest():
    return render_template('fest.html')
@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/stand')
def stand():
    return render_template('stand.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 

@app.route('/404') 
def error404(): 
        return render_template('404.html')

@app.errorhandler(403)
def not_correct(e):
    return render_template('403.html'), 403 

@app.route('/403') 
def error403(): 
        return render_template('403.html')
    
@app.errorhandler(401)
def not_correct(e):
    return render_template('401.html'), 401 

@app.route('/401') 
def error401(): 
        return render_template('401.html')
    
@app.route('/402') 
def error402(): 
        return render_template('402.html')


class Except402 (exceptions.HTTPException):
     code = 402
     description = 'Что то 402'

def handle_402(e):
    return render_template('402.html')

app.register_error_handler(Except402, handle_402)

@app.errorhandler(400)
def not_correct(e):
    return render_template('400.html'), 400 

@app.route('/400') 
def error400(): 
        return render_template('400.html')
    
@app.errorhandler(405)
def not_correct(e):
    return render_template('405.html'), 405 

@app.route('/405') 
def error405(): 
        return render_template('405.html')
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)