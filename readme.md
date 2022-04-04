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

1. After installation you need to run the following command to start the program: 

`python3.9 main.py --answers 3 --similarity 0.7 --input ./data/1801_Prozesse.txt`

For "answers" you should enter an integer value for the number of expected answer options per MTF question.
For 'similarity' you should enter a float value between 0 and 1 for the percentage of similarity between the answer choices. This specifies the percentage of the sentence that remains unchanged.
2. Select a text files as an input for the question generation.
3. As output you get a text summary (.txt) of your selected source text and a csv file (delimiter " ; ") with different answer options.

## Installation

1. Create a new environment: `conda create -n mtfenv python=3.9`
2. Activate the environment: `conda activate mtfenv`
3. Install dependencies using anaconda: 
```
conda install -y -c conda-forge pdfplumber
conda install -y -c conda-forge nltk
conda install -y -c conda-forge pypdf2
conda install -y -c conda-forge pylatexenc
conda install -y -c conda-forge packaging
conda install -y -c conda-forge transformers
conda install -y -c conda-forge essential_generators
conda install -y -c conda-forge xlsxwriter
```
3. Download spacy: `python3.9 -m spacy download de_core_news_lg`

# Roadmap


# License

Distributed under the MIT License. See [LICENSE.txt](https://gitlab.pi6.fernuni-hagen.de/la-diva/adaptive-assessment/generationofmultipletruefalsequestions/-/blob/master/LICENSE.txt) for more information.

# Contact
Regina Kasakowskij - e-mail
Niels Seidel - e-mail

Project Link: 

# Acknowledgments

This research was supported by the Research Cluster Digitalization, Diversity and Lifelong Learning – Consequences for Higher Education (D²L²) of the FernUniversität in Hagen, Germany.
