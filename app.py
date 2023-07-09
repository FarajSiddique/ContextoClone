from flask import Flask, render_template, request, session
from pattern.text.en import singularize
import torch
import torchtext
import math
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Authenticate session per user to ensure security

target_word = "helicopter"
glove = torchtext.vocab.GloVe(name="6B", dim=100)

dist = torch.norm(glove.vectors - glove[target_word], dim=1)  # Similarity score of all words compared to target word
lst = sorted(enumerate(dist.numpy()), key=lambda x: x[1])  # sort by distance


@app.route('/', methods=["GET", "POST"])
def getSimScore():
    if 'counter' not in session:
        session['counter'] = 0
        session['guesses'] = {}
        sim_score = 0
        sorted_guesses = {}
    if request.method == "POST":
        session['counter'] += 1
        text = singularize(request.form.get("word"))
        for i, idx in enumerate(lst):
            if glove.itos[idx[0]] == text:
                sim_score = i
                break
        bar_width = getBarWidth(sim_score)
        bar_color = getBarColor(sim_score)
        session['guesses'][text] = {'sim_score': sim_score, 'bar_width': bar_width, 'bar_color': bar_color}
        sorted_guesses = dict(sorted(session['guesses'].items(), key=lambda x: x[1]['sim_score']))
    return render_template('homepage.html', messageText='sample text', gameNum=1, guessNum=session['counter'],
                           guesses=sorted_guesses)


def getBarWidth(distance):
    total = 40000
    startX = 0
    endX = 100
    startY = pdf(startX)
    endY = pdf(endX)

    x = (distance / total) * (endX - startX)
    result = ((pdf(x) - endY) / (startY - endY)) * 100

    if result < 1:
        result = 1
    return result


def getBarColor(distance):
    if distance < 1000:
        return 'var(--green)'
    elif distance < 3000:
        return 'var(--yellow)'
    return 'var(--red)'


def pdf(x):
    lmbda = 0.5
    return lmbda * math.exp(-lmbda * x)


if __name__ == '__main__':
    app.run()
