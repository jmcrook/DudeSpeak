import cv2
import numpy as np
import nltk
import string
import random
from dude_speak import ngram_model, weighted_random_by_dct

words = nltk.tokenize.word_tokenize(open('dude_lines.txt', 'r').read().lower())
m = ngram_model(words, 3)


def detokenize(tokens):
    return ''.join([' ' + i if i[0] not in string.punctuation and '\'' not in i else i for i in tokens])

def word_face(model, pic_file):

    pic = cv2.imread(pic_file, cv2.IMREAD_REDUCED_GRAYSCALE_2)

    haar_cascade_face = cv2.CascadeClassifier(
            '/Users/jmcrook/Library/Python/2.7/lib/python/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    faces_rects = haar_cascade_face.detectMultiScale(pic, scaleFactor=1.2, minNeighbors=5)

    x, y, w, h = faces_rects[0]
    face = pic[y-(h/3):y+h+(h/3), x-(w/3):x+w+(w/3)]

    counter = 0
    line = ''
    word = []
    curr_state = random.choice(model.keys())
    for e in np.nditer(face):
        if counter == face.shape[1]:
            counter = 0
            print line
            line = ''

        if e < 80:
            line += ' '
        else:
            if not word:
                line += ' '
                try:  # in case curr_state is last two words of the corpus
                    curr_word = weighted_random_by_dct(model[curr_state])
                except e:
                    bad_state = curr_state
                    while curr_state == bad_state:
                        curr_state = random.choice(model.keys())
                    curr_word = weighted_random_by_dct(model[curr_state])
                curr_state = tuple([curr_state[1], curr_word])
                word = list(curr_word)
                word.reverse()
            else:
                line += word.pop()

        counter += 1

word_face(m, 'The_Dude.jpg')