import os
import sys
import re
from collections import Counter

def generate_stopwords(text, num_stopwords=100):
  words = re.findall(r'\w+', text.lower().replace('\n', ' '))
  word_freq = Counter(words)
  stpwrds = [word for word, _ in word_freq.most_common(num_stopwords)]
  return stpwrds

data_files = set(sys.argv[1:])
texts = []

print('input entries', data_files)

for t in data_files:
  if os.path.isfile(t):
    texts.append(t)
  elif os.path.isdir(t):
    for (root,dirs,files) in os.walk('test_dir', topdown=True):
      for name in files:
        texts.append(os.path.join(root, name))

print('input files:', texts)

stopwords = []

for text in texts:
  stopwords.append(generate_stopwords(open(text).read()))

# Find overlapping stopwords
overlapping_stopwords = set(stopwords[0])
for lst in stopwords[1:]:
  overlapping_stopwords.intersection_update(lst)

# save stopwords
with open('data/generated_stopwords.txt', 'w') as f:
  f.write('\n'.join(overlapping_stopwords))

print('stopwords saved to data/generated_stopwords.txt')