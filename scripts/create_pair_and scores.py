import os
import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process semantic relatedness annotations from Label Studio.')
parser.add_argument('id_to_item', required=True, type=str, help='csv or tsv file containing the mapping from item ids to item names.')
parser.add_argument('scored_annotations', required=True, type=str, help='csv or tsv file containing the scored annotations.')
parser.add_argument('-o', '--output', required=True, type=str, help='output directory for the processed annotations.')

args = parser.parse_args()
id_to_item = args.id_to_item
scored_annotations = args.scored_annotations
output_dir = args.output

# create the output directory if it does not exist
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# ensure that the input files exist and are csv or tsv files
assert os.path.exists(id_to_item), 'Input file does not exist.'
assert os.path.exists(scored_annotations), 'Input file does not exist.'
assert id_to_item.endswith('.csv') or id_to_item.endswith('.tsv'), 'Input file must be a csv or tsv file.'
assert scored_annotations.endswith('.csv') or scored_annotations.endswith('.tsv'), 'Input file must be a csv or tsv file.'

# read the id to item mapping
try:
  id_to_item = pd.read_csv(id_to_item, names=['item', 'id'])
except:
  try:
    id_to_item = pd.read_csv(id_to_item, sep='\t', names=['item', 'id'])
  except:
    sys.exit('Could not read the id to item mapping file. Please check the file format.')

# read the scored annotations
try:
  scored_annotations = pd.read_csv(scored_annotations, header=None, names=['item', 'id'])
except:
  try:
    scored_annotations = pd.read_csv(scored_annotations, sep='\t', header=None, names=['item', 'id'])
  except:
    sys.exit('Could not read the scored annotations file. Please check the file format.')

# merge the id to item mapping with the scored annotations on the item id
scored_annotations = pd.merge(scored_annotations, id_to_item, on='id')

# save the processed annotations
scored_annotations[['item', 'score']].to_csv(os.path.join(output_dir, 'scored_annotations.csv'), index=False)

print('Processed annotations saved to {}.'.format(os.path.join(output_dir, 'scored_annotations.csv')))