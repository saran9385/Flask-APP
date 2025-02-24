from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Inquiry, Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/', methods=['GET', 'POST']) 
def home():
    if request.method == 'POST':
        name = request.form['name']
        phone=request.form['phone']
        email = request.form['email']
        message = request.form['message']
        new_inquiry = Inquiry(name=name,phone=phone, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()

        flash("We will reach out to you shortly for further steps")
        return redirect(url_for('home'))
        # return render_template('home.html')

    return render_template('home.html')

@app.route('/contactform', methods=['POST']) 
def contactform():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not email or not message:
        return jsonify({'error': 'Please fill all the fields!'}), 400  # Return JSON error

    new_inquiry = Inquiry(name=name, phone=phone, email=email, message=message)
    db.session.add(new_inquiry)
    db.session.commit()

    return jsonify({'success': 'We will reach out to you shortly for further steps!'}), 200  # Return JSON success

@app.route('/enquiry_form', methods=['GET', 'POST'])
def enquiry_form():
    if request.method == 'POST':
        name = request.form['name']
        phone=request.form['phone']
        email = request.form['email']
        message = request.form['message']
        if not name or not phone or not email or not message:
            return jsonify({'error': 'Please fill all the fields!'}), 400
        new_inquiry = Inquiry(name=name,phone=phone, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()
        return jsonify({'message': 'We will reach out to you shortly for further steps'})
        # flash("Inquiry submitted successfully!", "success")
        # return redirect(url_for('enquiry_form'))
    # return render_template('inquiry_form.html')

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
    return render_template('admin_panel.html', inquiries=inquiries)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        
        flash("Invalid credentials!", "danger")

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/home')
def home1():
    return render_template('home.html')
@app.route('/facilities')
def facilities():
    return render_template('facilities.html')
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')
@app.route('/events')
def events():
    return render_template('events.html')
@app.route('/travel')
def travel():
    return render_template('travel.html')
@app.route('/attraction')
def attraction():
    return render_template('attraction.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/termsandcondition')
def termsandcondition():
    return render_template('termsandcondition.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
