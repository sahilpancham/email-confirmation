from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Sahilpancham10@gmail.com'
app.config['MAIL_PASSWORD'] = 'rvaq giys egyr lynt'

mail = Mail(app)

# Temporary storage for user data
users = {}

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Generate confirmation token
        confirmation_token = secrets.token_urlsafe(16)
        
        # Store user data temporarily
        users[email] = {'username': username, 'password': password, 'confirmed': False, 'confirmation_token': confirmation_token}

        # Send confirmation email
        msg = Message('Confirm Your Email', sender='your_email@example.com', recipients=[email])
        msg.body = f'Click the link to confirm your email: {url_for("confirm_email", token=confirmation_token, _external=True)}'
        mail.send(msg)

        flash('A confirmation email has been sent to your email address. Please confirm your email before logging in.', 'success')
        return redirect(url_for('confirm_email.html'))
    return render_template('register.html', form=form)

# Email confirmation route
@app.route('/confirm_email')
def confirm_email(token):
    for email, user_data in users.items():
        if user_data['confirmation_token'] == token:
            user_data['confirmed'] = True
            flash('Your email has been confirmed. You can now log in.', 'success')
            return redirect(url_for('login'))
    flash('Invalid confirmation token.', 'error')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
