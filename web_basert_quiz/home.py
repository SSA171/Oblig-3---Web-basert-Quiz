from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('quiz'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('home.html', the_title='Home Page')

if __name__ == "__main__":
    app.run()