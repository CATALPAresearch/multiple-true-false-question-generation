
from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import pipeline
import random
import spacy 
import nltk
nlp = spacy.load("de_core_news_lg")

inputPath = './'
outputPath = './output'

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


def generate_question(text, answer_options, similarity, filename=False):
    pipe = pipeline(
        'text-generation', 
        model="dbmdz/german-gpt2",
        tokenizer="dbmdz/german-gpt2"
        )

    text = text.replace(';','.')
    text = text.replace('•', '')
    text = text.replace('z. B.', 'zum Beispiel')
    doc= nlp(text)
    
    textsummary  = []
    b = answer_options   #int(input("Anzahl der Falschaussagen z.B. 3: "))
    z = similarity       #float(input("wähle einen Anteil des Satzes, der erhalten bleiben soll, 0.1 - 0.99: "))
    for sentence in doc.sents:
        words = len(sentence)* z 
        print (words) 
        sentenceshort = sentence[0:words]
        i=0
        for  i in range(b):
            if(words > 3):
                    output_max_len = 75
                    if(words/z > 37):
                        output_max_len = (words/z)*2

                    textsent = pipe(str(sentenceshort), max_length= output_max_len) [0]["generated_text"]
                    
                    textsent = textsent.replace('\n', ' ')
                    textsent = textsent.replace(r'\s+',' ')
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
                    textsent = textsent.replace('ff.', 'folgende')
                    textsent = textsent.replace('f.', 'folgend')

                    text_token = nlp(textsent) 
                    doc_sents = [sent.text for sent in text_token.sents] 
                    textsent = doc_sents[0]
                    if(len(doc_sents[0].replace(" ","")) == 0 ):
                        textsent = doc_sents[1]
                    textsent = textsent.replace('\n', ' ')
                    textsent = textsent.replace(';', '.')
                    
                    sentence2 = str(sentence).replace('\n', ' ')
                    sentence2 = sentence2[:1].upper() + sentence2[1:]
                    textsent = str(textsent)[:1].upper() + str(textsent)[1:]
                    textsummary.append([sentence2, str(textsent)])
                    i = i+1
    print(textsummary)
    
    print(len(textsummary))
    return textsummary

# Additional possibilities to generate false sentences 
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
        else:
            i=0
            for word in sent: 
                if word.tag_ in ['VB', 'VVFIN']:
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
                    if word.text == "sich":   #####TODO: Das gleiche mit man , es etc.
                            changedSentence.pop()
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
                            changedSentence.append(' nicht ')
                    else:
                            changedword = word.text_with_ws
                            changedSentence.append(changedword) 
        text = ''.join([i for i in changedSentence])
        textsummary.append([sent.text_with_ws, text])
        print(changedSentence)
        textsummary = []
        changedSentence = []