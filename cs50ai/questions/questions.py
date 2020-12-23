import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Generate dictionary of files
    files = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding = 'utf-8') as file_read:
            text = file_read.read()
        files[file] = text
    
    # Output dictionary
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize text and open list
    tokens = nltk.word_tokenize(document)
    words = list()
    
    # Select words from text for word list
    for i in range(len(tokens)):
        if tokens[i] not in string.punctuation and tokens[i] not in nltk.corpus.stopwords.words("english"):
            words.append(tokens[i].lower())
    
    # Output list of words
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Open set of unique words
    unique_words = set()
    for file in documents:
        for word in documents[file]:
            unique_words.add(word)
    
    # Compute inverse document frequencies for all words
    idfs = dict()
    for word in unique_words:
        idfs[word] = 0
        for file in documents:
            if word in documents[file]:
                idfs[word] += 1
        idfs[word] = math.log(len(documents) / idfs[word])

    # Output dictionary of inverse document frequencies    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Open ranking dictionary
    ranking = dict()
    
    # Compute tf-idf values for all files
    for file in files:
        ranking[file] = 0
        for word in query:
            try:
                ranking[file] += files[file].count(word) * idfs[word]
            except:
                continue
    
    # Sort ranking dictionary
    top_files = [x for x in sorted(ranking, key = ranking.get, reverse = True)]
    
    # Output list of top files for search
    return top_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Open ranking dictionaries
    ranking_idf = dict()
    ranking_qtd = dict()
    
    # Compute cumulative idf values for all sentences
    for sentence in sentences:
        ranking_idf[sentence] = 0
        ranking_qtd[sentence] = 0
        for word in query:
            if word in sentences[sentence]:
                ranking_idf[sentence] += idfs[word]
                ranking_qtd[sentence] += 1
        ranking_qtd[sentence] /= len(sentences[sentence])
    
    # Sort ranking dictionary
    top_sent = [x for x in sorted(ranking_idf, key = lambda x: (ranking_idf.get(x), ranking_qtd.get(x)), reverse = True)]
    
    # Output list of top sentences
    return top_sent[:n]


if __name__ == "__main__":
    main()






