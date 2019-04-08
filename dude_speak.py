import nltk
import random

#INPUT: a dict w/ normalized probabilities as vals
#OUTPUT: a key chosen randomly according to the probability vals
def weighted_random_by_dct(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


# INPUT: a list of words; the corpus
# OUTPUT: a dictionary where d[w1...wn-1][wn] = p(wn | w1...wn-1)
def ngram_model(w, n):
    d = {}

    for i in range(len(w)-n):
        state = tuple(w[i:i+(n-1)])
        if state not in d:
            d[state] = {}
        if w[i+n-1] not in d[state]:
            d[state][w[i+n-1]] = 1
        else:
            d[state][w[i+n-1]] += 1

    for state in d:
        total = 0.0
        for wn in d[state]:
            total += d[state][wn]

        for wn in d[state]:
            d[state][wn] /= total

    return d


def generate_line(model):
    start = ('-', '-')

    while start[0] != '.':
        start = random.choice(list(model.keys()))

    out = list(start)[1:]
    done = False
    curr = start
    while not done:
        new = weighted_random_by_dct(model[curr])
        out.append(new)
        if new == '.':
            done = True
        curr = tuple(list(curr[1:]) + [new])

    out = ' '.join(out)
    out = out.replace(' \'', '\'')
    out = out.replace(' n\'', 'n\'')

    return out




words = nltk.tokenize.word_tokenize(open('dude_lines.txt', 'r').read().lower())
m = ngram_model(words, 2)

f = open('spoken_by_dude.txt', 'a')

dude_line = generate_line(m)
f.write(dude_line + '\n\n')

f.close()

print "The dude says: " + dude_line



