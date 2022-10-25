This project provides a Natural Language Pipeline for processing German Textbook sections as an input generating Multiple True-False Question using GPT2.


# Features
- generation of false statements
- automatic selection of true statements 
- selection of an arbitrary similarity for true and false statements as well as the number of false statements

# Setup

## Getting startet

1. After installation you need to execute the run.sh script by e.g. running `bash run.sh` in the terminal


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
[click here to see the roadmap](https://gitlab.pi6.fernuni-hagen.de/la-diva/adaptive-assessment/generationofmultipletruefalsequestions/-/blob/master/MTF-generation_Roadmap.png)

# License

Distributed under the MIT License. See [LICENSE.txt](https://gitlab.pi6.fernuni-hagen.de/la-diva/adaptive-assessment/generationofmultipletruefalsequestions/-/blob/master/LICENSE.txt) for more information.

# Contact
- Regina Kasakowskij (M.A.) - regina.kasakowskij@fernuni-hagen.de
- Dr. Niels Seidel - niels.seidel@fernuni-hagen.de

Project Link: 

# Acknowledgments

This research was supported by CATALPA – Center of Advanced Technology for Assisted Learning and Predictive Analytics of the FernUniversität in Hagen, Germany.
