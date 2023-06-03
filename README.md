# Semantic Relatedness Finder

This Python script find semantically related sentences in a given text. It uses lexical overlap as a measure of semantic relatedness. The script can be customized to remove stopwords, clean sentences by removing special characters, and limit the number of matches per sentence.

## Features

- Finds semantically related sentences based on lexical overlap.
- Option to remove stopwords.
- Option to clean sentences by removing special characters.
- Option to limit the number of matches per sentence.
- Outputs a CSV file containing pairs of semantically related sentences.

## Requirements

- Python 3
- pandas

## Usage

The script can be run from the command line with the following arguments:

```
python semantic_relatedness.py -i <input_file> -s <stopwords_file> -o <output_directory> -m <maximum_matches> --remove_stopwords --clean_sentences
```

- `-i, --input`: (Required) Path to the input file containing the sentences.
- `-s, --stopwords`: Path to the stopwords file. This is required if the `--remove_stopwords` option is used.
- `-o, --output`: Path to save the semantically-related sentences. If the directory does not exist, it will be created.
- `-m, --maximum_matches`: Maximum number of matches per sentence. Default is 2.
- `--remove_stopwords`: Use this option to remove stopwords.
- `--clean_sentences`: Use this option to remove special characters.

## Example

```
python semantic_relatedness.py -i sentences.txt -s stopwords.csv -o output -m 2 --remove_stopwords --clean_sentences
```

This will find semantically related sentences in the `sentences.txt` file, remove stopwords using the `stopwords.csv` file, clean the sentences by removing special characters, limit the number of matches per sentence to 2, and save the output to the `output` directory.

## Output

The output is a CSV file named `output.csv` containing pairs of semantically related sentences. Each row represents a pair of sentences, with the first sentence in the "Sentence 1" column and the second sentence in the "Sentence 2" column.

## Note

The stopwords file should be in CSV or TXT format. If it is a CSV file, it should have a column named 'stopwords' containing the stopwords. If it is a TXT file, it should contain one stopword per line.

## Data Sources

The following table provides number of sentence-pair and domain for different languages:

| Language | Twitter | News | Facebook |
|----------|---------|------|----------|
| Hausa  |             |   |       |
| Yoruba       |         |         |      |
| Igbo       |         |         |      |
| -       |         |         |      |

