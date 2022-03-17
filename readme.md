This project provides a Natural Language Pipeline for processing German Textbook sections as an input generating Multiple True-False Question using GPT2.

**Todo**

- [ ] write readme.md
- [ ] text pipeline with one text
- [ ] collect all input texts
- [ ] run pipe line with all texts
- [ ] render output measures for publication

# Features

# Setup

## Getting startet

1. After installation you need to run the following command to start the program: `python3.9 main.py 'answer-options' 'similarity'`
For "answer-options" you should enter an integer value for the number of expected answer options per MTF question.
For 'similarity' you should enter a float value between 0 and 1 for the percentage of similarity between the answer choices. This specifies the percentage of the sentence that remains unchanged.
2. Select a text files as an input for the question generation.

## Installation

* Create a new environment: `conda create -n mtfenv python=3.9`
* Activate the environment: `conda activate mtfenv`
* Install dependencies using anaconda: 
```
conda install -y -c conda-forge pdfplumber
conda install -y -c conda-forge nltk
conda install -y -c conda-forge pypdf2
conda install -y -c conda-forge pylatexenc
conda install -y -c conda-forge packaging
conda install -y -c conda-forge transformers
conda install -y -c conda-forge essential_generators
```
* Download spacy: `python3.9 -m spacy download de_core_news_lg`

# Roadmap

