from flask import Flask, render_template, request, redirect, session
from database import get_db, init_db
import random

app = Flask(__name__)

# needed for sessions to work
app.secret_key = "supersecretkey123"  # TODO: change this before submitting lol

# create the database tables when app starts
init_db()

# home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


# signup

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']

    # basic validation
    if not firstname or not email or not password:
        return render_template('signup.html', error="Please fill in all the fields")

    if password != confirmpassword:
        return render_template('signup.html', error="Passwords don't match!")

    if len(password) < 8:
        return render_template('signup.html', error="Password needs to be at least 8 characters")

    # save to database
    # should probably hash the password but will do that later
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (firstname, lastname, email, password) VALUES (?, ?, ?, ?)",
            (firstname, lastname, email, password)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return render_template('signup.html', error="Email already exists! Try logging in.")

    return redirect('/login?success=1')


# Login

@app.route('/login')
def login():
    success = request.args.get('success')
    return render_template('login.html', success=success)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return render_template('login.html', error="Please enter your email and password")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    ).fetchone()
    conn.close()

    if user is None:
        return render_template('login.html', error="Wrong email or password!")

    # save user in session
    session['user_email'] = user['email']
    session['user_name'] = user['firstname']

    return redirect('/')


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Zoo booking

@app.route('/zoobooking')
def zoobooking():
    return render_template('zoobooking.html')

@app.route('/zoobooking', methods=['POST'])
def zoobooking_post():
    visit_date = request.form['date']
    adults = int(request.form['adults'])
    children = int(request.form['children'])
    addon = request.form['addon']
    notes = request.form['notes']

    # calculate total
    addon_prices = {'none': 0, 'safari': 8, 'penguins': 12}
    total = (adults * 18) + (children * 10) + (addon_prices.get(addon, 0) * (adults + children))

    booking_ref = "ZOO" + str(random.randint(10000, 99999))

    # get user email if logged in
    user_email = session.get('user_email', 'guest')

    conn = get_db()
    conn.execute(
        "INSERT INTO zoo_bookings (user_email, visit_date, adults, children, addon, notes, total, booking_ref) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_email, visit_date, adults, children, addon, notes, total, booking_ref)
    )
    conn.commit()
    conn.close()

    return render_template('zoobooking.html', booking_ref=booking_ref, total=total, visit_date=visit_date, adults=adults, children=children, addon=addon)


# Hotel booking

@app.route('/hotelbooking')
def hotelbooking():
    return render_template('hotelbooking.html')

@app.route('/hotelbooking', methods=['POST'])
def hotelbooking_post():
    hotel_name = request.form['hotel_name']
    hotel_price = float(request.form['hotel_price'])
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    guests = request.form['guests']
    roomtype = request.form['roomtype']
    guestname = request.form['guestname']
    guestemail = request.form['guestemail']

    # work out number of nights and total
    from datetime import datetime
    checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
    checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
    nights = (checkout_date - checkin_date).days

    total = nights * hotel_price

    booking_ref = "HTL" + str(random.randint(10000, 99999))

    conn = get_db()
    conn.execute(
        "INSERT INTO hotel_bookings (guest_name, guest_email, hotel_name, room_type, checkin_date, checkout_date, guests, total, booking_ref) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (guestname, guestemail, hotel_name, roomtype, checkin, checkout, guests, total, booking_ref)
    )
    conn.commit()
    conn.close()

    return render_template('hotelbooking.html', booking_ref=booking_ref, total=total, hotel_name=hotel_name, checkin=checkin, checkout=checkout, nights=nights)


# add 404 page later
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


app.run(debug=True)
