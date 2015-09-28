# Python script generates sentence lyrics using Markov chain algorithm
import re
from random import choice
from random import randint
from sys import argv
from sys import exit


class Markov(object):
    def __init__(self, file_names=None):
        self.words = []
        self.m_chains = {}

        if file_names:
            self.read_texts(file_names)
            self.make_chains()

    def read_texts(self, file_names):
        for fn in file_names:
            if fn.endswith('.txt'):
                with open(fn, 'r') as f:
                    for line in f.readlines():
                        self.words.extend(line.rstrip().split())

    def triples(self):
        for i in range(0, len(self.words) - 2):
            w1 = self.words[i]
            w2 = self.words[i + 1]
            w3 = self.words[i + 2]
            yield (w1, w2, w3)

    def make_chains(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.m_chains:
                self.m_chains[key].append(w3)
            else:
                self.m_chains[key] = [w3]

    def make_sentence(self, length=20):
        w1 = " "
        w2 = " "
        while not w1[0].isupper():
            i = randint(0, len(self.words) - 1)
            w1 = self.words[i]
            w2 = self.words[i + 1]
        end_sentence = re.compile(".*[\.\!\?]")
        sentence = []
        while True:
            sentence.append(w1)
            if ((end_sentence.match(w1)) and
                (len(sentence) >= length)):
                break

            w3 = choice(self.m_chains[(w1, w2)])
            w1 = w2
            w2 = w3

        return " ".join(sentence)

if len(argv) > 2:
    m = Markov(argv[2:])
    print(m.make_sentence(length=int(argv[1])))
else:
    print("Usage: python markov.py <minimum_sentence_length> <text files 1...n>")
    exit(1)
