# Step 1: Data Preprocessing
import re  # regular expression
from collections import Counter
import numpy as np
import pandas as pd


# Implement the function process_data which
# 1) Reads in a corpus (text file)  #2) Changes everything to lowercase  3) Returns a list of words.


words = []
with open('sample.txt','r',encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    words = re.findall('\w+', file_name_data)


vocab = set(words)
print(f"The first ten words in the text are: \n{words[0:10]}")
print(f"There are {len(vocab)} unique words in the vocabulary.")


# a get_count functio that returns a dictionary of word vs frequency
def get_count(words):
    word_count_dict = {}
    for word in words:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1
    return word_count_dict


word_count_dict = get_count(words)
print(f"There are {len(word_count_dict)} key values pairs")



# Compute the probability that each word will appear if randomly selected from the corpus of words.
# implement get_probs function

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


# Now we implement 4 edit word functions
# delete_letter: given a word, it returns all the possible strings that have one character removed.
# switch_letter: given a word, it returns all the possible strings that have two adjacent letters switched.
# replace_letter: given a word, it returns all the possible strings that have one character replaced by another different letter.
# insert_letter: given a word, it returns all the possible strings that have an additional character inserted.

def delete_letter(word):
    delete_l = []
    split_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    for a, b in split_l:
        delete_l.append(a + b[1:])
    return delete_l


delete_word_l = delete_letter(word="cans")


def switch_letter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l


switch_word_l = switch_letter(word="eta")


def replace_letter(word):
    split_l = []
    replace_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters]
    return replace_l


replace_l = replace_letter(word='can')


def insert_letter(word):
    split_l = []
    insert_l = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = [a + l + b for a, b in split_l for l in letters]
    # print(split_l)
    return insert_l



# combining the edits
# switch operation optional
def edit_one_letter(word, allow_switches=True):
    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))
    return edit_one_set



# edit two letters
def edit_two_letters(word, allow_switches=True):
    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_two_set.update(edit_two)
    return edit_two_set



# get corrected word
def get_corrections(word, probs, vocab, n=2):
    suggestions = []
    n_best = []
    suggestions = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab))
    n_best = [[s, probs[s]] for s in list(reversed(suggestions))]
    return n_best


my_word = input("Enter a word:")
probs = get_probs(word_count_dict)
tmp_corrections = get_corrections(my_word, probs, vocab, 2)
for i, word_prob in enumerate(tmp_corrections):
    print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")