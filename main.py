
import os
import argparse

import utils as u
import text_summarization as ts
import question_generation as qg


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='')
    
    parser.add_argument(
        '-a', 
        '--answers',   
        type=int,
        help='Expected number of answer options', 
        default=3
        )
    parser.add_argument(
        '-s',
        '--similarity',   
        type=float,
        help='Similarity of answer options', 
        default=0.5
        )
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='path to text (.txt) or PDF file'
    )
    args = parser.parse_args()
    if args.answers and isinstance(args.answers, int):
        answer_options = args.answers  # parser.parse_args('-a')
    else:
        answer_options = 3
        
    if args.similarity and isinstance(args.similarity, float) and args.similarity > 0 and args.similarity < 1:
        similarity = args.similarity  # parser.parse_args('-sim')
    else:
        similarity = 0.3
        
    if args.input and os.path.isfile(args.input):
        filename = args.input
    else:
        filename = False
        
    print(answer_options, similarity, filename)
    
    
    inputPath = './'
    outputPath = './output'
    utils = u.Utils(inputPath, outputPath)
    
    # Step 1: Summarize text
    print("START SUMMARIZER")
    text = utils.read_file(filename=filename)
    summarizer = ts.TextSummarizer()
    summerized_text = summarizer.summarize_text(text)
    utils.save_txt(summerized_text, filename, prefix='_summarized.txt')
    print(".. END SUMMARIZER")
    print()
    
    # Step 2: Generate MTF questions
    print("START QUESTION GENERATION")
    result = qg.generate_question(summerized_text, answer_options, similarity, filename)
    utils.save_csv(summerized_text, filename, prefix='_generated.csv')
    print("end QUESTION GENERATION")
    
    # Step 3: Prepare output for evaluation
