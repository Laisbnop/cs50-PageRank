import os
import random
import re
import sys

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

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

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
    """
    all_pages = list(corpus.keys())
    n = len(all_pages)
    distribution = {}

    base_prob = (1 - damping_factor) / n
    links = corpus[page]

    if not links:
        for p in all_pages:
            distribution[p] = 1 / n
        return distribution

    link_prob = damping_factor / len(links)

    for p in all_pages:
        distribution[p] = base_prob
        if p in links:
            distribution[p] += link_prob

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    all_pages = list(corpus.keys())
    counts = {page: 0 for page in all_pages}

    current = random.choice(all_pages)
    counts[current] += 1

    for _ in range(n - 1):
        model = transition_model(corpus, current, damping_factor)
        pages = list(model.keys())
        weights = list(model.values())
        current = random.choices(pages, weights=weights, k=1)[0]
        counts[current] += 1

    ranks = {page: counts[page] / n for page in all_pages}
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    all_pages = list(corpus.keys())
    n = len(all_pages)
    ranks = {page: 1 / n for page in all_pages}

    while True:
        new_ranks = {}

        for page in all_pages:
            new_rank = (1 - damping_factor) / n
            link_sum = 0

            for other in all_pages:
                links = corpus[other]
                if not links:
                    link_sum += ranks[other] / n
                elif page in links:
                    link_sum += ranks[other] / len(links)

            new_rank += damping_factor * link_sum
            new_ranks[page] = new_rank

        converged = all(
            abs(new_ranks[page] - ranks[page]) <= 0.001
            for page in all_pages
        )

        ranks = new_ranks

        if converged:
            break

    return ranks


if __name__ == "__main__":
    main()