from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('homepage.html', messageText='sample text', gameNum=1, guessNum=1, wordAccuracy=999)


if __name__ == '__main__':
    app.run()
