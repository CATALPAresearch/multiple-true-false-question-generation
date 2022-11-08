This project provides a Natural Language Pipeline for processing German Textbook sections as an input generating Multiple True-False Question using GPT2.

Assessments are an important part of the learning cycle and enable the development and promotion of competencies. However, the manual creation of assessments is very time-consuming. Therefore, the number of tasks in learning systems is often limited. In this repository, we provide an algorithm that can automatically generate an arbitrary number of German True False statements from a textbook using the GPT-2 model. The algorithm was evaluated with a selection of textbook chapters from four different academic disciplines (see `data` folder) and rated by individual domain experts. One-third of the generated MTF Questions are suitable for learning. The algorithm provides instructors with an easier way to create assessments on chapters of textbooks to test factual knowledge.


As a type of Multiple-Choice question, Multiple True False (MTF) Questions are, among other question types, a simple and efficient way to objectively test factual knowledge. The learner is challenged to distinguish between true and false statements. MTF questions can be presented differently, e.g. by locating a true statement from a series of false statements, identifying false statements among a list of true statements, or separately evaluating each statement as either true or false. Learners must evaluate each statement individually because a question stem can contain both incorrect and correct statements. Thus, MTF Questions as a machine gradable format have the potential to identify learners’ misconceptions and knowledge gaps.

Example MTF question:

> Check the correct statements:
> * [ ] All trees have green leafs.
> * [ ] Trees grow towards the sky.
> * [ ] Leafes can fall from a tree.


# Features
- generation of false statements
- automatic selection of true statements 
- selection of an arbitrary similarity for true and false statements as well as the number of false statements
- generating false statements by adding or deleting negations as well as using a german gpt2

# Setup

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

## Getting startet

After installation you can execute the bash script `bash run.sh` in the terminal to compile MTF questions for the provided textbook chapters. 
To create MTF questions for your own texts use the followiing command:

`python3 main.py --answers 1 --similarity 0.66 --input ./<path>/<to>/<your>/<textbook>.txt` 

The parameter `answers` indicates how many false answers should be generated. 
By configuring the parameter `similarity` you can determine what portion of a sentence should remain the same. The remaining portion will be extrcated and used for generation of a false part of the sentence. 


## History and roadmap 
* Outlook third iteration: Automatic augmentation of text chapters with generated questions
* Second iteration: Generation of multiple true false questions with improved text summmarizer and German GPT2 sentence generator
* First iteration: Generation of multiple true false question in the Bachelor thesis of Mirjam Wiemeler


# Publications, citation, license

**Publications**

* Kasakowskij, R., Kasakowskij, T. & Seidel, N., (2022). Generation of Multiple True False Questions. In: Henning, P. A., Striewe, M. & Wölfel, M. (Hrsg.), 20. Fachtagung Bildungstechnologien (DELFI). Bonn: Gesellschaft für Informatik e.V.. (S. 147-152). DOI: [10.18420/delfi2022-026](https://dl.gi.de/handle/20.500.12116/38826)

**Citation of the Dataset**

* xxx

The source code and data are maintained at GitHub: https://github.com/D2L2/multiple-true-false-question-generation

**Contact**

- Regina Kasakowskij (M.A.) - regina.kasakowskij@fernuni-hagen.de
- Dr. Niels Seidel - niels.seidel@fernuni-hagen.de

**License**

Distributed under the MIT License. See [LICENSE.txt](https://gitlab.pi6.fernuni-hagen.de/la-diva/adaptive-assessment/generationofmultipletruefalsequestions/-/blob/master/LICENSE.txt) for more information.


**Acknowledgments** This research was supported by CATALPA - Center of Advanced Technology for Assisted Learning and Predictive Analytics of the FernUniversität in Hagen, Germany. 
This project was carried out as part of research in the CATALPA project [LA DIVA](https://www.fernuni-hagen.de/forschung/schwerpunkte/catalpa/forschung/projekte/la-diva.shtml)