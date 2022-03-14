from distutils.log import ERROR
from tkinter import filedialog
from transformers import AutoTokenizer, AutoModelWithLMHead
import csv
from transformers import pipeline
from essential_generators import DocumentGenerator
import random
import spacy 
import nltk
import tkinter as tk
from nltk import Tree
nlp = spacy.load("de_core_news_lg")

#gen = DocumentGenerator()
#template = {"text": "abc"}
#gen.set_template(template)
#part one generating random Sentences 
#print(gen.sentence())
#print(gen.documents(10))

np_list = []
vp_list = []
negations = ['nein', 'kein', 'keine', 'keiner', 'keinem', 'keines', 'keinen', 'nicht', 'niemals', 'niemand']
grammar = r"""
        NP: {<DT|PP>?<JJ.*>*<NN.*>}
            {<NNP>+}
        VP: {<JJ.*>?<RB>?<VB+><NN.*>*}
        """

tokenizer = AutoTokenizer.from_pretrained("dbmdz/german-gpt2")
model = AutoModelWithLMHead.from_pretrained("dbmdz/german-gpt2")


def save(textsummary):
    with open('questionsentencesnegations.csv', 'a') as f:
        writer = csv.writer(f, delimiter = ';', quotechar= '"', quoting=csv.QUOTE_MINIMAL)
        for i in textsummary:
            writer.writerow(i)
        #writer.close() 

def generate_question(text):
    pipe = pipeline('text-generation', model="dbmdz/german-gpt2",
                 tokenizer="dbmdz/german-gpt2")

    text = text.replace(';',':')
    text = text.replace('•', '')
    doc= nlp(text)
    
    textsummary  = []
    b = int(input("Anzahl der Falschaussagen z.B. 3: "))
    z = float(input("wähle einen Anteil des Satzes, der erhalten bleiben soll, 0.1 - 0.99: "))
    for sentence in doc.sents:
        words = len(sentence)* z 
        print (words) 
        #words = words * 2 / 3
        sentenceshort = sentence[0:words]
        #print (sentence)
        
        #textsent = pipe(str(sentence), max_length=100)[0]["generated_text"]
       
        i=0
        for  i in range(b):
            if(words > 3):
               # try:
                   # textsent = pipe(str(sentenceshort), max_length=len(sentence)*2)[0]["generated_text"]
                    textsent = pipe(str(sentenceshort), max_length= 75) [0]["generated_text"]

                    textsent = textsent.replace('z.B.', 'zum Beispiel')
                    textsent = textsent.replace('ca.', 'circa')
                    textsent = textsent.replace('d.h.', 'das heißt')
                    textsent = textsent.replace('vgl.', 'vergleich')
                    textsent = textsent.replace('z.T.', 'zum Teil')
                    textsent = textsent.replace('usw.', 'und so weiter')
                    textsent = textsent.replace('zzgl.', 'zuzüglich')
                    textsent = textsent.replace('bzw.', 'beziehungsweise')
                    textsent = textsent.replace('s.o.', 'siehe oben')
                    textsent = textsent.replace('u.a.', 'unter anderem')
                    textsent = textsent.replace('v.Chr.', 'vor Christus')
                    textsent = textsent.replace('n.Chr.', 'nach Christus')
                    textsent = textsent.replace('Nr.', 'Nummer')
                    textsent = textsent.replace('Abb.', 'Abbildung')
                    textsent = textsent.replace('etc.', 'et cetera')
                    textsent = textsent.replace('S.', 'Seite')

                    textsent =  textsent + " ---- ende ---"
                    textsentlist= textsent.split('.')  
                    textsent = textsent.replace(textsentlist[len(textsentlist)-1], '')
                    textsent = textsent.replace('\n', ' ')
                    sentence2 = str(sentence).replace('\n', ' ')
                    textsummary.append([sentence2, str(textsent)])
                    #save (sentence, str(textsent))
                    i = i+1
                #except:
                #    print (ERROR)
                #    print (i)
                #    i= i+1
                #    break
                
            
    save(textsummary)
    #print(str(textsent))
    #for sentence in text:
     #   return sentence


def new_sentence(sentence):
    sentence = nlp(sentence)
    cp = nltk.RegexpParser(grammar)
    parsed_sent = cp.parse(sentence)
    print(sentence.sents)
    print(parsed_sent.subtrees())

    for word in parsed_sent.subtrees():
        npword = ""
        print(word)
        if word.lable() == 'NP':
            yield npword.join(element for element, tag in word.leaves())
        np_list.append(npword)
        vp_list.append(word.text_with_ws)
    np = random.coice(np_list)
    vp = [vp_element for vp_element in vp_list]
    newSentence = np + vp
    return print(sentence)


def delete_negation(sentence):
    changedSentence = ""
    for word in sentence.split():
        if word in negations:
            changedSentence = changedSentence + ''
            
        else:
            changedSentence = changedSentence + ' ' + word 
    return changedSentence


def add_negation(sentence):
    changedSentence = []
    textsummary = []
    doc = nlp(sentence)
    for sent in doc.sents:
        if any(word in sent.text_with_ws for word in negations):
            print (sent)
            continue
            #return sent
        else:
            #sentence = nlp(sentence)
            i=0
            for word in sent: #sentence:
                #print (word)
                if word.tag_ in ['VB', 'VVFIN']:
                    #print (word.tag_)
                    if i < 1:
                        changedword = word.text_with_ws
                        changedSentence.append(changedword) 
                        changedSentence.append(' nicht ')
                        i+=1
                    else:
                        if word.text == "sich":
                            changedSentence.pop()
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
                            changedSentence.append(' nicht ')
                        else:
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
                    
                else:
                    if word.text == "sich":   ##### Das gleiche mit man , es 
                            changedSentence.pop()
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
                            changedSentence.append(' nicht ')
                    else:
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
        text = ''.join([i for i in changedSentence])
        textsummary.append([sent.text_with_ws, text])
        #save(textsummary)
        print(changedSentence)
        textsummary = []
        changedSentence = []
    
    #return changedSentence

def get_file():
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    return (root.filename)

def read_file():
    filename = get_file()
    if filename.endswith('.txt'):
        textFileObj = open(filename, 'r', encoding="utf-8")
        content = textFileObj.read()
        return  content


#generate_question(read_file())
#print(delete_negation("Die Sonne kreist nicht um die Erde"))
#add_negation('Die Erde dreht sich um die Sonne')
