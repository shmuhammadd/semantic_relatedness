import re
import os
import sys
import pandas as pd
from collections import defaultdict
import string

import argparse

def load_stopwords(stopwords_file):
  if stopwords_file.endswith('.csv'):
    stopwords_df = pd.read_csv(stopwords_file)
    stopwords = set(stopwords_df['stopwords'].values)
  elif stopwords_file.endswith('.txt'):
    with open(stopwords_file, 'r') as file:
      stopwords = set(file.read().splitlines())
  else:
    print("Stopwords file format not supported. Provide a CSV or TXT file.")
    sys.exit(-1)
  return stopwords

def remove_tabs(text):
  return text.replace('\t', '')

def clean_sentence(sentence):
  # Lowercase the sentence
  sentence = sentence.lower()
  # Remove any special characters
  sentence = ''.join(c for c in sentence if ord(c) < 128)
  return sentence

def find_lexical_overlap(text, stopwords_file, maximum_matches, remove_stopwords=False, clean_sentences=False):

  # Split the text into sentences
  sentences = text.splitlines()

  # Load stopwords from CSV file
  if remove_stopwords:
    stopwords = load_stopwords(stopwords_file)

  # List to store sentence pairs with lexical overlap
  sentence_pairs = []

  # Dictionary to store sentence occurrence count
  sentence_counts = defaultdict(int)

  # preprocess cleaning sentences
  if clean_sentences:
    sentences_cleaned = [clean_sentence(sentence) for sentence in sentences]
  else:
    sentences_cleaned = sentences
  
  # preprocess getting set of words
  if remove_stopwords:
    sentences_words = [set(sentence.split()).difference(stopwords) for sentence in sentences_cleaned]
  else:
    sentences_words = [set(sentence.split()) for sentence in sentences_cleaned]

  # preprocess computing sentence length
  sentence_length = [len(sentence.split()) for sentence in sentences_cleaned]

  # Iterate over sentences to find pairs with lexical overlap
  for i in range(len(sentences)):
    related = []
    selected = []
    print('Sentence', i + 1)
    sentence1 = sentences_cleaned[i]

    # Check if sentence length is between 5 and 25 words
    if 5 <= sentence_length[i] <= 25:
      for j in range(i+1, len(sentences)):

        sentence2 = sentences_cleaned[j]

        if sentences[i].lower() == sentences[j].lower():
          print('Sentences', i, 'and', j, 'are the same, skipping...')
          continue

        # Check if sentence length is between 5 and 25 words
        if 5 <= sentence_length[j] <= 25:

            # Check overlap if neither sentence has appeared more than twice
            if sentence_counts[sentences[i]] < maximum_matches and sentence_counts[sentences[j]] < maximum_matches:
              words1 = sentences_words[i]
              words2 = sentences_words[j]
              
              overlap = words1.intersection(words2)

              if len(overlap) >= 5:  # Choose the lexical overlap
                sentence_pairs.append((sentences[i], sentences[j]))
                
                # Increase count for each sentence
                sentence_counts[sentences[i]] += 1
                sentence_counts[sentences[j]] += 1
                related.append(j)

      if related:
        print('\tRelated:', related)
      else:
        print('\tRelated: None')
    else:
      print('\tShort sentence.')

    print()

  return sentence_pairs

parser = argparse.ArgumentParser(description='Crawl articles from Premium Times Hausa website.')
parser.add_argument('-i', '--input', required=True, type=str, help='file containing the sentences.')
parser.add_argument('-s', '--stopwords', type=str, help="stopwords file. required if '--remove_stopwords' option is used.")
parser.add_argument('-o', '--output', default='', type=str, help='path to save the semantically-related sentences.')
parser.add_argument('-m', '--maximum_matches', default=2, type=int, help='maximum number of matches per sentence.')
parser.add_argument('--remove_stopwords', action='store_true', help='use to remove stopwords.')
parser.add_argument('--clean_sentences', action='store_true', help='use to remove special characters.')

args = parser.parse_args()

if args.remove_stopwords:
  if not os.path.exists(args.stopwords):
    print("Stopwords file not found.")
    sys.exit(-1)

if not os.path.exists(args.output):
  os.makedirs(args.output)

# Read the text file
with open(args.input, 'r') as file:
  text = file.read()

s_p = find_lexical_overlap(text, args.stopwords, args.maximum_matches, args.remove_stopwords, args.clean_sentences)
df = pd.DataFrame(s_p, columns=["Sentence 1", "Sentence 2"])

# Save the semantically-related sentences
df.to_csv(os.path.join(args.output, 'output.csv'), index=False)

print('Saved the semantically-related sentences to', os.path.join(args.output, 'output.csv'), 'successfully.')