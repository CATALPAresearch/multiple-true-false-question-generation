import spacy
from heapq import nlargest
from string import punctuation
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter
from nltk.corpus import stopwords
stoplist = set(stopwords.words("german"))

#from ast import Str
#from scipy.spatial.distance import cosine
#import numpy as np
#from nltk.tokenize import sent_tokenize, word_tokenize
#from itertools import count
#from numpy.lib.function_base import average

class TextSummarizer:
    
    def __init__(self):
        pass
    
    """
    Summarize a given text and return the summary
    """
    def summarize_text(self, text):  # (text, per):
        summary = ''

        text = text.replace('- ', '')
        text = text.replace(';', ',')
        text = text.replace('-\n', '')             
        text = text.replace('z.B.', 'zum Beispiel')
        text = text.replace('ca.', 'circa')
        text = text.replace('d.h.', 'das heißt')
        text = text.replace('u.v.a.', 'und vor allem')

        nlp = spacy.load("de_core_news_lg")
        doc = nlp(text)
    # tokens=[token.text for token in doc]
    # len(list(doc.sents))
        keyword = []
        stopwords = list(STOP_WORDS)
        # stopwords.extend([])
        pos_tag = [ 'ADJ', 'NOUN', 'VERB'] #'PROPN',
        for token in doc:
            if(token.text in stopwords or token.text in punctuation):
                continue
            if (token.pos_ in pos_tag):
                keyword.append(token.text)
        freq_word = Counter(keyword)
        # freq_word.most_common(5)
        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)

        sent_strength = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += freq_word[word.text]
                    else:
                        sent_strength[sent] = freq_word[word.text]
        #TODO exclude sentences referring to a context (e.g. "Dieser", "Somit", ...)
        summary_sentences = nlargest(round(len(
            [[token.text for token in sent] for sent in doc.sents]) * 0.1), sent_strength, key=sent_strength.get)
        fin_summary = [w.text for w in summary_sentences]
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
