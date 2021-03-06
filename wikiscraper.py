import concurrent.futures
from bs4 import BeautifulSoup
import requests
import multiprocessing
import random
import os
import re

def download(url, dir_name="files"):
    """
    crawls page located at root url and extracts links (i.e. "branches") from page
    randomly selects k of these branches
    creates a directory for the tree
    makes a [root url].txt file inside the directory 
    iterates through the k urls of root's branch nodes
    writes branch url to the [root url].txt file if it links to 
    another wiki page
    """
    output = []
    title = url.split("wiki/")[1]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(id="bodyContent").find_all("a")
    links = [f"http://wikipedia.org/{link.get('href')}" for link in data]
    links = random.choices(links, k=10)
    if not os.path.isdir(f"{dir_name}"):
        os.mkdir(f"{dir_name}")
    with open(f"files/{title}.txt", "w") as f:
        for i in links:
            if re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$", i):
                output.append(i)
                f.write(i+"\n"+"\n")
    return output
    """
    I'll probably change this^ function later so that k is passed as an argument
    and the regex-based filter condition is included in the list comprehension rather 
    than applied to the iteration through the list that follows.
    """

def extract_citations(url):
    """
    crawls wikipedia page for citations, writes citations to
    *.txt file
    """
    citations = []
    response = requests.get(url)
    bs = BeautifulSoup(response.content, features="html.parser")
    title = bs.find(id="firstHeading").text
    bs = [i.text for i in bs.find_all("span", "reference-text")]
    bs = [str(i).split("^") for i in bs]
    for i in bs:
        for j in i:
            if len(j) > 1: citations.append(j)
    if not os.path.isdir("references"): os.mkdir("references")
    with open(f"references/{title}.txt", "w", encoding='utf-8') as fh:
        for i in sorted(citations):
            if len(i) > 1: fh.write(i+"\n\n")

def pool(urls):
    """
    threading to improve performance
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, urls)

def main(url, count, crawl_depth):
    """
    construct k-ary tree of depth n using
    recursion and multiprocessing
    """
    links = download(url)
    if count > crawl_depth:
        return
    for i in links:
        p = multiprocessing.Process(target=main, args=(i, count + 1, crawl_depth))
        p.start()
    pool(links)

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Brain"
    main(url, 0, 2)
