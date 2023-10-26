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
   # print(corpus)
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
    
    links=set(corpus[page])
    N=len(links)
    if N==0:
        N=1
    M=len(corpus)
    prob_all=(1-damping_factor)*1/M
    prob_links=prob_all+damping_factor/N
    pages=set(corpus.keys())
    
    res={}
    if links=={}:
        for i in pages:
            res[i]=1/M
    else:
        for i in pages:
            if i in links:
                res[i]=prob_links
            else:
                res[i]=prob_all
    return res


            
    
    
    
    
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys=set(corpus.keys())
    dico={}
    for i in keys:
        dico[i]=0
    page=random.choice(list(keys))
    dico[page]+=1
    for i in range(n-1):
        transition=transition_model(corpus,page,damping_factor)
        key=list(transition.keys())
        prob=list(transition.values())
        page=random.choices(key,prob)[0]
        dico[page]+=1
    #a=0
    for j in list(dico.keys()):
        dico[j]=dico[j]/n
    #    a+=dico[j]
   # print(a)
   # print(list(dico.keys()))
    return dico

def maxdif(l1,l2,corpus):
    maxi=0
    for r in corpus:
        if abs(l1[r]-l2[r])>maxi:
            maxi=abs(l1[r]-l2[r])
    return maxi



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    '''
    pages=set(corpus.keys())
    
    #for i in corpus:
     #   if len(corpus[i])==0:
      #      corpus[i]=pages
    

    
   # print(corpus)
    n=len(pages)
    dico={}
    dicopy={}
    d=(1-damping_factor)/n
    for i in pages:
        dico[i]=1/n
        dicopy[i]=100
   # print(dico)

     
    while True:#maxdif(dico,dicopy,corpus)>0.001:
       # for k in pages:
        #    dicopy[k]=dico[k]
        dicopy=dico.copy()
        for i in corpus:
            links=corpus[i]
            a=0
            for j in links:
                if len(corpus[j])==0:
                    a+=dicopy[j]/n
                else:
                    a+=dicopy[j]/len(corpus[j])
            dico[i]=d+damping_factor*a
            
    #normalisation
            total=sum(dico.values())
            for m in dico:
                dico[m]=dico[m]/total
        if all(abs(dico[p]-dicopy[p])<0.001 for p in corpus):
            break
            
    return dico
    '''

   
    N = len(corpus)

   
    pagerank = {page: 1 / N for page in corpus}
 
    epsilon = 0.001

    while True:
     
        prev_pagerank = pagerank.copy()

        for page in corpus:
            new_pagerank = (1 - damping_factor) / N

            linking_pagerank_sum = sum(pagerank[link] / len(corpus[link]) for link in corpus if page in corpus[link])

            pagerank[page] = new_pagerank + damping_factor * linking_pagerank_sum

        convergence = all(abs(prev_pagerank[page] - pagerank[page]) < epsilon for page in corpus)

        if convergence:
            break

    total_pagerank = sum(pagerank.values())
    pagerank = {page: rank / total_pagerank for page, rank in pagerank.items()}

    return pagerank

if __name__ == "__main__":
    main()
