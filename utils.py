import os
from tkinter import filedialog
import tkinter as tk
import pdfplumber
from pylatexenc.latex2text import LatexNodes2Text
import csv
#import PyPDF2
class Utils:
    
    def __init__(self, inputPath, outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath
        
    """
    Provides dialog to open a file from lokal file system
    """
    def get_file(self):
        root = tk.Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(
            initialdir="./", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
        return (root.filename)

    """
    Reads data from a give file path
    """
    def read_file(self, filename=False):
        if filename == False:
            filename = self.get_file()
        if filename.endswith(".tex"):
            texFileObj = open(os.path.join(self.inputPath, filename),
                            'r', encoding="utf-8")
            content = texFileObj.read()
            return LatexNodes2Text().latex_to_text(content)

        elif filename.endswith('.pdf'):
            with pdfplumber.open(os.path.join(self.inputPath, filename)) as pdf:
                text = ""
                for i in pdf.pages:
                    text += " " + str(i.extract_text())

            #pdfFileObj = pdfplumber.open(filename)  #open(filename, 'rb')  #
            #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            #pages = pdfReader.numPages
            #content = ""
            # for i in range(pages):
            #    pageObj = pdfReader.getPage(i)
            #    text = pageObj #.extractText()
            #    content += " " + text.extractText() + " " #text.extract_text()
                #print (text)
                return text

        elif filename.endswith('.txt'):
            textFileObj = open(os.path.join(
                self.inputPath, filename), 'r', encoding="utf-8")
            content = textFileObj.read()
            return content

        else:
            print('Dieser Datentyp wird leider nicht unterstützt')

    """
    Saves data to text file
    """
    def save_txt(self, textsummary, filename=False, prefix=''):
        outfilename = 'summarized.txt'
        if filename != False:
            outfilename = os.path.basename(filename).replace(
                '.txt', prefix
            ).replace(
                '.pdf', prefix)

        with open(os.path.join(self.outputPath, outfilename), 'w') as f:
            f.write(textsummary)
            f.close()
            
    """
    Saves data to csv file
    """
    def save_csv(self, textsummary, filename=False, prefix=''):
        outfilename = 'generated_sentences.csv'
        if filename != False:
            outfilename = os.path.basename(filename).replace(
                '.txt', prefix
            ).replace(
                '.pdf', prefix)
        with open(os.path.join(self.outputPath, outfilename), 'a') as f:
            writer = csv.writer(f, 
                                delimiter=';', 
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for i in textsummary:
                writer.writerow(i)
            
            
            
  


    
