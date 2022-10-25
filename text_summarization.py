import spacy
from heapq import nlargest
from string import punctuation
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter
from nltk.corpus import stopwords
stoplist = set(stopwords.words("german"))

class TextSummarizer:
    
    def __init__(self):
        pass
    
    """
    Summarize a given text and return the summary
    """
    def summarize_text(self, text):  # (text, per):
        summary = ''

        text = text.replace('und', ' und')
        text = text.replace('- ', '')
        text = text.replace('ff.', 'folgende')
        text = text.replace('f.', 'folgend')
        text = text.replace('-\n', '')             
        text = text.replace('z.B.', 'zum Beispiel')
        text = text.replace('ca.', 'circa')
        text = text.replace('d.h.', 'das heißt')
        text = text.replace('d. h.', 'das heißt')
        text = text.replace('u.v.a.', 'und vor allem')

        nlp = spacy.load("de_core_news_lg")
        doc = nlp(text)
    
        keyword = []
        delete_kontext = ['Damit', 'damit', 'Dies', 'dies', 'also','Abbildung', '§','§§','Abb.', 'Abschnitt', 'Abschnitte', 'So', 'Somit', 'zum Beispiel', 'dann', 'nun', 'Beispiel', 'Daraus', 'Hierbei', 'zuvor','Dieser', 'Dieses', 'Diesem', 'fassen', 'zusammen', 'zusammenfassend', 'Dort', 'dort'] #could be made easier and maybe needs additions
        stopwords = list(STOP_WORDS)
        pos_tag = [ 'ADJ', 'NOUN', 'VERB'] #'PROPN',
        for token in doc:
            if(token.text in stopwords or token.text in punctuation or token.text in delete_kontext):
                continue
            if (token.pos_ in pos_tag):
                keyword.append(token.text)
        freq_word = Counter(keyword)
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

        print(summary)
        return summary
