from flask import Flask, render_template, request
from pattern.text.en import singularize
import torch
import torchtext
import math

app = Flask(__name__)
target_word = "helicopter"
glove = torchtext.vocab.GloVe(name="6B", dim=100)


# x = glove['cat']
# y = glove['lamp']
# print(torch.cosine_similarity(x.unsqueeze(0), y.unsqueeze(0)))
#
#
# def print_closest_words(vec, n=5):
#     dists = torch.norm(glove.vectors - vec, dim=1)  # compute distances to all words
#     lst = sorted(enumerate(dists.numpy()), key=lambda x: x[1])  # sort by distance
#     for idx, difference in lst[1:n + 1]:  # take the top n
#         print(glove.itos[idx], difference)
#
#
# print_closest_words(glove["helicopter"], n=100)


# def singularize_input(text):
#     newText = singularize(text)
#     return newText


@app.route('/', methods=["GET", "POST"])
def getSimScore():
    if request.method == "POST":
        text = request.form.get("word")
        new_text = singularize(text)
        #
        # # dist = torch.norm(glove[target_word].unsqueeze(0) - glove[new_text].unsqueeze(0), dim=1)
        # # sim_score = int(dist.numpy()[0] * 10)
        # # print(sim_score)
        # sim_score = ((torch.cosine_similarity(glove[target_word], glove[new_text])).numpy()[0])
        # print(sim_score)
    return render_template('homepage.html', messageText='sample text', gameNum=1, guessNum=1, wordAccuracy=999)


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


def pdf(x):
    lmbda = 0.5
    return lmbda * math.exp(-lmbda * x)


def getIdxDistance(word, target_word):
    dists = torch.norm(glove.vectors - glove[target_word], dim=1)  # compute distances to all words
    # if word == target_word:
    #     return -1
    lst = sorted(enumerate(dists.numpy()), key=lambda x: x[1])
    for idx, i in enumerate(lst):
        if glove.itos[idx] == word:
            return idx,i


print(getIdxDistance('helicopter', 'helicopter'))

if __name__ == '__main__':
    app.run()
