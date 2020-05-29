#!./venv python
# -*- coding: utf-8 -*-
"""
evaluation.py: evaluating WISE online service against QALD-6 benchmark
"""
__author__ = "Mohamed Eldesouki"
__copyright__ = "Copyright 2020, CODS Lab, GINA CODY SCHOOL OF ENGINEERING AND COMPUTER SCIENCE, CONCORDIA UNIVERSITY"
__credits__ = ["Mohamed Eldesouki"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "CODS Lab"
__email__ = "mohamed@eldesouki.ca"
__status__ = "debug"
__created__ = "2020-03-11"


import json
import time
from wise import Wise
from termcolor import colored, cprint
from itertools import count
import xml.etree.ElementTree as Et


the_39_question_ids = (1, 3, 8, 9, 11, 13, 14, 15, 16, 17, 21, 23, 24, 26, 27, 28, 30, 31, 33, 35, 37, 39, 40, 41, 43,
                       47, 54, 56, 61, 62, 64, 68, 75, 83, 85, 92, 93, 96, 99)
file_name = r"/home/disooqi/projects/wise/evaluation/qald6/qald-6-test-multilingual.json"

# word_vectors = api.load("wiki-news-300d-1m")  # load pre-trained word-vectors from gensim-data


if __name__ == '__main__':
    root_element = Et.Element('dataset')
    root_element.set('id', 'dbpedia-test')
    author_comment = Et.Comment(f'created by mohamed@eldesouki.ca')
    root_element.append(author_comment)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    the_39_questions = list()

    with open(file_name) as f:
        qald6_testset = json.load(f)
    dataset_id = qald6_testset['dataset']['id']
    WISE = Wise()
    counter = count(1)
    wise_qald6 = {"dataset": {"id": "qald-6-test-multilingual"}, "questions": []}
    for i, question in enumerate(qald6_testset['questions']):
        # if question['id'] not in the_39_question_ids:
        #     continue

        qc = next(counter)
        if question["id"] != 8:
            continue

        # question_text = ''
        for language_variant_question in question['question']:
            if language_variant_question['language'] == 'en':
                question_text = language_variant_question['string'].strip()
                text = colored(f"[PROCESSING: ] Question count: {qc}, ID {question['id']}  >>> {question_text}", 'blue',
                               attrs=['reverse', 'blink'])
                cprint(f"== {text}  ")
                break

        st = time.time()
        # question_text = 'Which movies starring Brad Pitt were directed by Guy Ritchie?'
        # question_text = 'When did the Boston Tea Party take place and led by whom?'
        answers = WISE.ask(question_id=question["id"], question_text=question_text, answer_type=question['answertype'],
                           n_max_answers=5, merge_answers=True)
        if answers:
            wise_qald6["questions"].append(answers)

        et = time.time()
        text = colored(f'[DONE!! in {et-st:.2f} SECs]', 'green', attrs=['bold', 'reverse', 'blink', 'dark'])
        cprint(f"== {text} ==")

    with open(f'output/WISE_result_{timestr}.json', encoding='utf-8', mode='w') as rfobj:
        json.dump(wise_qald6, rfobj)
        rfobj.write('\n')

