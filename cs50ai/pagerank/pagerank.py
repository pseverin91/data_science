import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Compute probability distributions
    transitions = dict()
    for link in corpus:
        transitions[link] = round((1 - damping_factor) / len(corpus), 4)
        if link in corpus[page]:
            transitions[link] += round(damping_factor / len(corpus[page]), 4)
    return transitions


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initiate page rank dictionary
    page_rank = dict()
    for key in corpus:
        page_rank[key] = 0
    
    # Select start page and transition n times from there
    page = random.choice(tuple(corpus.keys()))
    for sample in range(n):
        page_rank[page] += 1
        transitions = transition_model(corpus, page, damping_factor)
        page = random.choices(tuple(transitions.keys()), weights = transitions.values())[0]
    
    # Compute probability distribution for all page visits
    for key in page_rank:
        page_rank[key] = page_rank[key] / n
    return(page_rank)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initiage page rank dictionary
    page_rank = dict()
    for key in corpus:
        page_rank[key] = 1 / len(corpus)
    page_rank_temp = copy.deepcopy(page_rank)
    
    # Compute conditional probability distribution
    while True:
        for key in page_rank:
            i = 0
            page_rank_temp[key] = (1 - damping_factor) / len(corpus)
            for values in corpus.values():
                if key in values:
                    page_rank_temp[key] += damping_factor * list(page_rank.values())[i] / len(list(corpus.values())[i])
                i += 1
        
        # Define breaking point for minor improvements
        count = 0
        for key in page_rank:
            if page_rank[key] - page_rank_temp[key] < 0.00001 and page_rank[key] - page_rank_temp[key] > -0.00001:
                count += 1
        if count == 4:
            break
        
        # Update probability distribution
        page_rank = copy.deepcopy(page_rank_temp)

    # Return probability distribution
    return page_rank


if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
