from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('test.html', the_title='Login Page')


if __name__ == "__main__":
    app.run()