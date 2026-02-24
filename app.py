from flask import Flask, render_template

app = Flask(__name__)

@app.route ('/')
def home():
    return render_template('home.html')

@app.route ("/about")
def about():
    return render_template("about.html")

@app.route ('/log')
def log():
    return render_template('log.html')


@app.route ('/signup')
def signup():
    return render_template('signup.html')


@app.route ('/zoobooking')
def zoobooking():
    return render_template('zoobooking.html')


@app.route ('/hotelbooking')
def hotelbooking():
    return render_template('hotelbooking.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500




app.run(debug=True)