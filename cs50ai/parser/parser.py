import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP | NP VP Conj NP VP
NP -> N | P NP | Det N | Det AP N | AP NP | NP PP | NP Adv
VP -> V | V NP | V Adv
AP -> Adj | Adj AP
PP -> P NP
"""



grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize input sentence
    words = nltk.word_tokenize(sentence)
    
    for i in range(len(words)):
        
        # Put words to lowercase
        words[i] = words[i].lower()
        
        # Remove non-alphabetic words
        count = 0
        for j in words[i]:
            if j.isalpha():
                count += 1
        if count == 0:
            words.remove(words[i])
        
    # Output list of words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Look through all subtrees to find noun-phrases
    global noun_phrases
    noun_phrases = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            noun_phrases.append(subtree)
    
    # Remove noun-phrases that are subtrees
    global sub_noun_phrases
    sub_noun_phrases = []
    for i in range(len(noun_phrases)):
        for j in range(len(noun_phrases)):
            if i != j and noun_phrases[i] in noun_phrases[j].subtrees():
                sub_noun_phrases.append(noun_phrases[i])
    for np in sub_noun_phrases:
        try:
            noun_phrases.remove(np)
        except:
            continue
    
    # Return list of noun-phrases
    return noun_phrases
    

if __name__ == "__main__":
    main()










