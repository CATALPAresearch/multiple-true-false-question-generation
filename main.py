import argparse
from collections import Counter
from itertools import count
import pdfplumber
import PyPDF2
from pylatexenc.latex2text import LatexNodes2Text
from nltk.corpus import stopwords
#import pdfplumber
from numpy.lib.function_base import average
stoplist = set(stopwords.words("german"))
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import tkinter as tk
from tkinter import filedialog
#from spacy.tokenizer import Tokenizer
#nlp = spacy.load("de_core_news_lg")
from spacy.lang.de.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

from nltk.corpus import stopwords
import numpy as np
from scipy.spatial.distance import cosine
import os

import question_generation as qg

inputPath = './data'
outputPath = './output'



def get_file():
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(
        initialdir="./", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    return (root.filename)


def read_file():
    filename = get_file()
    if filename.endswith(".tex"):
        texFileObj = open(os.path.join(inputPath, filename), 'r', encoding="utf-8")
        content = texFileObj.read()
        return  LatexNodes2Text().latex_to_text(content)

    elif filename.endswith('.pdf'):
        with pdfplumber.open(os.path.join(inputPath,filename)) as pdf:
            text = ""
            for i in pdf.pages:
                text += " " + str(i.extract_text()) 

        #pdfFileObj = pdfplumber.open(filename)  #open(filename, 'rb')  #
        #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        #pages = pdfReader.numPages
        #content = ""
        #for i in range(pages):
        #    pageObj = pdfReader.getPage(i) 
        #    text = pageObj #.extractText()
        #    content += " " + text.extractText() + " " #text.extract_text()
            #print (text)
            return text

    elif filename.endswith('.txt'):
        textFileObj = open(os.path.join(inputPath, filename), 'r', encoding="utf-8")
        content = textFileObj.read()
        return  content 

    else:
        print('Dieser Datentyp wird leider nicht unterstützt')


# get Extract of the Text
def summarize_text(text): #(text, per):
    summary = print("Start summarization")

    text = text.replace('- ', '')
    text = text.replace('-\n', '')

    nlp = spacy.load("de_core_news_lg")
    doc= nlp(text)
   # tokens=[token.text for token in doc]
   #len(list(doc.sents))
    keyword = []
    stopwords = list(STOP_WORDS)
    #stopwords.extend([])
    pos_tag = ['PROPN','ADJ', 'NOUN', 'VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            keyword.append(token.text)
    freq_word = Counter(keyword)
    #freq_word.most_common(5)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]

    summary_sentences = nlargest(round(len([[token.text for token in sent] for sent in doc.sents]) * 20 / 100), sent_strength, key=sent_strength.get)
    fin_summary= [w.text for w in summary_sentences]
    summary = ' '.join(fin_summary)

    """word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)"""
    print(summary)
    return summary



def save(textsummary):
    with open(os.path.join(outputPath,'summarized.txt'), 'w') as f:
        f.write(textsummary)
        f.close() 


def main():
    print ("PROZESS START ...")
    text = read_file()
    #save (text)
    #summarize_text(text, 0.30)
   # clean_sentences = clean_text(text)
   # words = []
   
  #  for sent in clean_sentences:
   #     words.append(nlkt_word_tokenize(sent))
    #    model = Word2Vec(words, min_count=1, sg = 1)
     #   print (sent)
    summerized_text = summarize_text(text) #summarize_text(text, 0.30) #summarize_text(text, model)
    save(summerized_text)
    print ("... ENDE SUMMARIZATION!")
    return summerized_text
    


if __name__ == '__main__':
    #main()
    #print ("... ENDE SUMMARIZATION!")

    parser = argparse.ArgumentParser(description='')  #formatter_class=argparse.RawDescriptionHelpFormatter,
    parser.add_argument('a',  type = int, help='Expected number of answer options', default=3) #'--answer-options',
    parser.add_argument('sim',   type = float, help='Similarity of answer options', default=0.5)   #action = 'store',    '--answer-options-similarity',
    args = parser.parse_args()
    answer_options  =  args.a    #parser.parse_args('-a')
    similarity = args.sim        #parser.parse_args('-sim')
    print(answer_options, similarity)

    qg.generate_question(main(), answer_options, similarity)
    print ("FINISHED ! ")

